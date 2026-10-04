#!/usr/bin/env python3
"""App Store Connect 文案校验工具（仅用标准库）。

本文件在 app-store-connect-copywriting 与 app-store-connect-localization 两个 skill 中各有一份，
内容相同；修改时两边同步。

子命令：
  check <文件.md> [--allow-subset]   校验整份多语种 Markdown 文件，不通过时退出码为 1
  count [文件] [--limit N]           统计一段纯文本的字符数，省略文件时读标准输入
  headings                           打印各语种的小节标题对照表（Markdown 表格）

计数口径：按 App Store Connect 可能采用的最严格方式计数，即 UTF-16 码元数，
换行按 CRLF 计 2 个字符。emoji 等辅助平面字符计 2。这样算出的数不会小于 ASC 的实际计数。
"""

import argparse
import re
import sys
import unicodedata

PROMO = "推广文本"
NOTES = "此版本的新增内容"
FIELD_ORDER = [PROMO, NOTES]
LIMITS = {PROMO: 170, NOTES: 4000}
BULLET = "• "

# 小节的固定顺序，键名取简体中文。
SECTION_KEYS = ["新增", "优化", "修复", "性能", "安全", "移除"]

# ASC 中文界面里的语种名（即 Markdown 的二级标题）、locale 代码、各小节标题。
# 顺序就是输出顺序。修改小节标题时同步 localization skill 的 references/locales.md。
LOCALES = [
    ("英语（美国）", "en-US", ("Added", "Changed", "Fixed", "Performance", "Security", "Removed")),
    ("阿拉伯语", "ar-SA", ("جديد", "تحسينات", "إصلاحات", "الأداء", "الأمان", "ما تمت إزالته")),
    ("北印度语", "hi", ("नया", "सुधार", "बग फ़िक्स", "परफ़ॉर्मेंस", "सुरक्षा", "हटाया गया")),
    ("波兰语", "pl", ("Nowości", "Ulepszenia", "Poprawki", "Wydajność", "Bezpieczeństwo", "Usunięte")),
    ("丹麦语", "da", ("Nyt", "Forbedringer", "Rettelser", "Ydeevne", "Sikkerhed", "Fjernet")),
    ("德语", "de-DE", ("Neu", "Verbesserungen", "Fehlerbehebungen", "Leistung", "Sicherheit", "Entfernt")),
    ("俄语", "ru", ("Новое", "Улучшения", "Исправления", "Производительность", "Безопасность", "Удалено")),
    ("法语", "fr-FR", ("Nouveautés", "Améliorations", "Corrections", "Performances", "Sécurité", "Suppressions")),
    ("法语（加拿大）", "fr-CA", ("Nouveautés", "Améliorations", "Corrections", "Performances", "Sécurité", "Suppressions")),
    ("繁体中文", "zh-Hant", ("新增", "改進", "修正", "效能", "安全性", "移除")),
    ("芬兰语", "fi", ("Uutta", "Parannukset", "Korjaukset", "Suorituskyky", "Tietoturva", "Poistettu")),
    ("韩语", "ko", ("추가", "개선", "수정", "성능", "보안", "제거")),
    ("荷兰语", "nl-NL", ("Nieuw", "Verbeteringen", "Opgelost", "Prestaties", "Beveiliging", "Verwijderd")),
    ("加泰罗尼亚语", "ca", ("Novetats", "Millores", "Correccions", "Rendiment", "Seguretat", "Eliminat")),
    ("简体中文", "zh-Hans", ("新增", "优化", "修复", "性能", "安全", "移除")),
    ("捷克语", "cs", ("Novinky", "Vylepšení", "Opravy", "Výkon", "Zabezpečení", "Odstraněno")),
    ("克罗地亚语", "hr", ("Novo", "Poboljšanja", "Ispravci", "Performanse", "Sigurnost", "Uklonjeno")),
    ("罗马尼亚语", "ro", ("Noutăți", "Îmbunătățiri", "Remedieri", "Performanță", "Securitate", "Eliminate")),
    ("马来语", "ms", ("Baharu", "Penambahbaikan", "Pembetulan", "Prestasi", "Keselamatan", "Dialih keluar")),
    ("挪威语", "no", ("Nytt", "Forbedringer", "Rettelser", "Ytelse", "Sikkerhet", "Fjernet")),
    ("葡萄牙语（巴西）", "pt-BR", ("Novidades", "Melhorias", "Correções", "Desempenho", "Segurança", "Removido")),
    ("葡萄牙语（葡萄牙）", "pt-PT", ("Novidades", "Melhorias", "Correções", "Desempenho", "Segurança", "Removido")),
    ("日语", "ja", ("追加", "変更", "修正", "パフォーマンス", "セキュリティ", "削除")),
    ("瑞典语", "sv", ("Nytt", "Förbättringar", "Åtgärdat", "Prestanda", "Säkerhet", "Borttaget")),
    ("斯洛伐克语", "sk", ("Novinky", "Vylepšenia", "Opravy", "Výkon", "Zabezpečenie", "Odstránené")),
    ("泰语", "th", ("ใหม่", "ปรับปรุง", "แก้ไข", "ประสิทธิภาพ", "ความปลอดภัย", "นำออก")),
    ("土耳其语", "tr", ("Yeni", "İyileştirmeler", "Düzeltmeler", "Performans", "Güvenlik", "Kaldırılanlar")),
    ("乌克兰语", "uk", ("Нове", "Покращення", "Виправлення", "Продуктивність", "Безпека", "Вилучено")),
    ("西班牙语（墨西哥）", "es-MX", ("Novedades", "Mejoras", "Correcciones", "Rendimiento", "Seguridad", "Eliminado")),
    ("西班牙语（西班牙）", "es-ES", ("Novedades", "Mejoras", "Correcciones", "Rendimiento", "Seguridad", "Eliminado")),
    ("希伯来语", "he", ("חדש", "שיפורים", "תיקונים", "ביצועים", "אבטחה", "הוסר")),
    ("希腊语", "el", ("Νέα", "Βελτιώσεις", "Διορθώσεις", "Απόδοση", "Ασφάλεια", "Καταργήθηκαν")),
    ("匈牙利语", "hu", ("Újdonságok", "Fejlesztések", "Javítások", "Teljesítmény", "Biztonság", "Eltávolítva")),
    ("意大利语", "it", ("Novità", "Miglioramenti", "Correzioni", "Prestazioni", "Sicurezza", "Rimozioni")),
    ("印度尼西亚语", "id", ("Baru", "Peningkatan", "Perbaikan", "Performa", "Keamanan", "Dihapus")),
    ("英语（澳大利亚）", "en-AU", ("Added", "Changed", "Fixed", "Performance", "Security", "Removed")),
    ("英语（加拿大）", "en-CA", ("Added", "Changed", "Fixed", "Performance", "Security", "Removed")),
    ("英语（英国）", "en-GB", ("Added", "Changed", "Fixed", "Performance", "Security", "Removed")),
    ("越南语", "vi", ("Mới", "Cải tiến", "Sửa lỗi", "Hiệu năng", "Bảo mật", "Đã loại bỏ")),
]

LOCALE_NAMES = [name for name, _, _ in LOCALES]
LOCALE_INDEX = {name: i for i, name in enumerate(LOCALE_NAMES)}
LOCALE_CODE = {name: code for name, code, _ in LOCALES}
LOCALE_HEADERS = {name: headers for name, _, headers in LOCALES}

# 常见的其他叫法，仅用于报错时提示正确名称。
ALIASES = {
    "英语": "英语（美国）",
    "英文": "英语（美国）",
    "中文（简体）": "简体中文",
    "简中": "简体中文",
    "中文（繁体）": "繁体中文",
    "繁體中文": "繁体中文",
    "繁中": "繁体中文",
    "印地语": "北印度语",
    "印尼语": "印度尼西亚语",
    "马来西亚语": "马来语",
    "书面挪威语": "挪威语",
    "希伯莱语": "希伯来语",
    "法语（法国）": "法语",
    "德语（德国）": "德语",
}

for _name, _code, _headers in LOCALES:
    assert len(_headers) == len(SECTION_KEYS) and len(set(_headers)) == len(_headers), _name

FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
H1_RE = re.compile(r"^#\s")
H2_RE = re.compile(r"^##\s+(.+?)\s*#*\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*#*\s*$")
MARKDOWN_LINE_RE = re.compile(r"^(#{1,6}\s|[-*+]\s|\*\*|>\s?|\d+\.\s)")


def asc_len(text):
    """ASC 计数口径：UTF-16 码元数，换行按 CRLF 计 2。"""
    text = text.replace("\r\n", "\n")
    return len(text.encode("utf-16-le")) // 2 + text.count("\n")


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text, width):
    return text + " " * max(0, width - display_width(text))


def parse_markdown(source):
    """返回 (locales, errors)。locales 为 [{name, line, fields: [{name, line, blocks}]}]。"""
    locales = []
    errors = []
    fence = None
    fence_line = 0
    buffer = []
    current_locale = None
    current_field = None

    for lineno, line in enumerate(source.splitlines(), 1):
        if fence:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                block = "\n".join(buffer).strip("\n")
                if current_field is not None:
                    current_field["blocks"].append(block)
                elif current_locale is not None:
                    errors.append(f"第 {fence_line} 行：「{current_locale['name']}」下的代码块不属于任何字段（缺少 ### 标题）")
                fence = None
                buffer = []
            else:
                buffer.append(line)
            continue

        match = FENCE_RE.match(line)
        if match:
            fence = match.group(1)
            fence_line = lineno
            continue

        match = H2_RE.match(line)
        if match and not line.startswith("###"):
            current_locale = {"name": match.group(1), "line": lineno, "fields": []}
            current_field = None
            locales.append(current_locale)
            continue

        match = H3_RE.match(line)
        if match and not line.startswith("####"):
            if current_locale is None:
                errors.append(f"第 {lineno} 行：字段标题「{match.group(1)}」出现在任何语种标题之前")
                continue
            current_field = {"name": match.group(1), "line": lineno, "blocks": []}
            current_locale["fields"].append(current_field)
            continue

        if H1_RE.match(line):
            current_field = None

    if fence:
        errors.append(f"第 {fence_line} 行：代码块没有闭合")
    return locales, errors


def analyze_notes(text, headers):
    """解析「此版本的新增内容」的结构，返回 (signature, errors)。

    signature 为 [(小节序号, 条目数), ...]，用于跨语种比对。
    """
    signature = []
    errors = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line in headers:
            index = headers.index(line)
            if signature and index <= signature[-1][0]:
                errors.append(f"小节「{line}」顺序不对或重复，应为：{' → '.join(headers)}")
            signature.append([index, 0])
            continue
        if raw.startswith(BULLET):
            if not signature:
                errors.append("列表项出现在第一个小节标题之前")
            elif not raw[len(BULLET):].strip():
                errors.append("存在空列表项")
            else:
                signature[-1][1] += 1
            continue
        if not signature:
            if MARKDOWN_LINE_RE.match(line):
                errors.append(f"摘要行含 Markdown 标记（ASC 不渲染 Markdown）：{line[:40]}")
            continue
        errors.append(
            f"无法识别的行（小节标题须与本语种标题表完全一致、不带冒号；列表项须以「{BULLET}」开头）：{line[:40]}"
        )

    if not signature:
        errors.append(f"没有找到小节标题，本语种应使用：{' / '.join(headers)}")
    for index, count in signature:
        if count == 0:
            errors.append(f"小节「{headers[index]}」下没有列表项")
    return [tuple(item) for item in signature], errors


def suggest_locale(name):
    if name in ALIASES:
        return ALIASES[name]
    chars = set(name)
    scored = [(len(chars & set(known)) / len(chars | set(known)), known) for known in LOCALE_NAMES]
    score, best = max(scored)
    return best if score >= 0.4 else None


def describe_signature(signature):
    return "、".join(f"{SECTION_KEYS[index]}×{count}" for index, count in signature) or "（空）"


def check_file(path, allow_subset):
    with open(path, encoding="utf-8") as handle:
        source = handle.read()

    locales, errors = parse_markdown(source)
    warnings = []
    rows = []
    reference_fields = None
    reference_signature = None

    if not locales:
        errors.append("没有找到任何语种标题（## 语种名）")

    seen = {}
    last_index = -1
    for locale in locales:
        name = locale["name"]
        where = f"第 {locale['line']} 行「{name}」"
        if name not in LOCALE_INDEX:
            hint = suggest_locale(name)
            suffix = f"，是否应为「{hint}」？" if hint else ""
            errors.append(f"{where}：不是可识别的语种名称{suffix}")
            continue
        if name in seen:
            errors.append(f"{where}：与第 {seen[name]} 行重复")
            continue
        seen[name] = locale["line"]
        index = LOCALE_INDEX[name]
        if index < last_index:
            errors.append(f"{where}：顺序不对，应排在「{LOCALE_NAMES[last_index]}」之前")
        last_index = max(last_index, index)

        counts = {}
        seen_fields = set()
        field_names = [field["name"] for field in locale["fields"]]
        if not field_names:
            errors.append(f"{where}：没有任何字段（### {PROMO} / ### {NOTES}）")
        for field in locale["fields"]:
            label = f"{name} · {field['name']}"
            if field["name"] not in LIMITS:
                errors.append(f"第 {field['line']} 行：字段标题「{field['name']}」无法识别，只能是「{PROMO}」或「{NOTES}」")
                continue
            if field["name"] in seen_fields:
                errors.append(f"{label}：字段重复")
                continue
            seen_fields.add(field["name"])
            blocks = field["blocks"]
            if len(blocks) != 1:
                errors.append(f"{label}：应恰好包含 1 个代码块，实际为 {len(blocks)} 个")
                if not blocks:
                    continue
            text = blocks[0]
            if not text.strip():
                errors.append(f"{label}：内容为空")
                continue

            length = asc_len(text)
            limit = LIMITS[field["name"]]
            counts[field["name"]] = length
            if length > limit:
                errors.append(f"{label}：{length} 字符，超过上限 {limit}（至少再删 {length - limit} 字符）")
            if unicodedata.normalize("NFC", text) != text:
                warnings.append(f"{label}：文本不是 NFC 规范化形式（多见于越南语、泰语等组合字符），粘贴后计数可能偏高")
            if any(line != line.rstrip() for line in text.split("\n")):
                warnings.append(f"{label}：有行尾空白")

            if field["name"] == NOTES:
                signature, notes_errors = analyze_notes(text, LOCALE_HEADERS[name])
                errors.extend(f"{label}：{message}" for message in notes_errors)
                if not notes_errors:
                    if reference_signature is None:
                        reference_signature = (name, signature)
                    elif signature != reference_signature[1]:
                        errors.append(
                            f"{label}：小节与条目数（{describe_signature(signature)}）"
                            f"与「{reference_signature[0]}」（{describe_signature(reference_signature[1])}）不一致"
                        )

        known = list(dict.fromkeys(field for field in field_names if field in LIMITS))
        if known != sorted(known, key=FIELD_ORDER.index):
            errors.append(f"{where}：字段顺序应为「{PROMO}」在前、「{NOTES}」在后")
        if reference_fields is None and known:
            reference_fields = (name, set(known))
        elif known and set(known) != reference_fields[1]:
            errors.append(
                f"{where}：字段（{'、'.join(known)}）"
                f"与「{reference_fields[0]}」（{'、'.join(sorted(reference_fields[1], key=FIELD_ORDER.index))}）不一致"
            )
        rows.append((name, counts))

    if not allow_subset:
        missing = [name for name in LOCALE_NAMES if name not in seen]
        if missing:
            errors.append(f"缺少 {len(missing)} 个语种：{'、'.join(missing)}（只需部分语种时加 --allow-subset）")

    print_report(rows, errors, warnings)
    return 0 if not errors else 1


def print_report(rows, errors, warnings):
    if rows:
        width = max(display_width(name) for name, _ in rows) + 2
        print(pad("语种", width) + pad("代码", 9) + pad(PROMO, 14) + NOTES)
        for name, counts in rows:
            cells = []
            for field in FIELD_ORDER:
                if field in counts:
                    mark = " ✗" if counts[field] > LIMITS[field] else ""
                    cells.append(f"{counts[field]}/{LIMITS[field]}{mark}")
                else:
                    cells.append("—")
            print(pad(name, width) + pad(LOCALE_CODE.get(name, "?"), 9) + pad(cells[0], 14) + cells[1])
        for field in FIELD_ORDER:
            values = [(counts[field], name) for name, counts in rows if field in counts]
            if values:
                longest = max(values)
                print(f"{field}最长：{longest[1]} {longest[0]}/{LIMITS[field]}")
        print()

    if warnings:
        print(f"警告（{len(warnings)}）：")
        for message in warnings:
            print(f"  - {message}")
    if errors:
        print(f"错误（{len(errors)}）：")
        for message in errors:
            print(f"  - {message}")
        print(f"\n结果：未通过（{len(rows)} 个语种）")
    else:
        print(f"结果：通过（{len(rows)} 个语种）")


def count_text(path, limit):
    if path and path != "-":
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()
    text = text.strip("\n")
    length = asc_len(text)
    print(f"ASC 计数：{length}（码点 {len(text)}，换行 {text.count(chr(10))}）")
    if limit is not None:
        if length > limit:
            print(f"超过上限 {limit}，至少再删 {length - limit} 字符")
            return 1
        print(f"未超过上限 {limit}，余 {limit - length}")
    return 0


def print_headings():
    print("| ASC 名称 | 代码 | " + " | ".join(SECTION_KEYS) + " |")
    print("| --- | --- | " + " | ".join("---" for _ in SECTION_KEYS) + " |")
    for name, code, headers in LOCALES:
        print(f"| {name} | {code} | " + " | ".join(headers) + " |")
    return 0


def main():
    parser = argparse.ArgumentParser(description="App Store Connect 本地化文案校验工具")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="校验多语种 Markdown 文件")
    check.add_argument("path")
    check.add_argument("--allow-subset", action="store_true", help="允许只包含部分语种（仍检查顺序）")

    count = sub.add_parser("count", help="统计纯文本字符数")
    count.add_argument("path", nargs="?", help="文本文件，省略或为 - 时读标准输入")
    count.add_argument("--limit", type=int, help="同时检查是否超过该上限")

    sub.add_parser("headings", help="打印小节标题对照表")

    args = parser.parse_args()
    if args.command == "check":
        return check_file(args.path, args.allow_subset)
    if args.command == "count":
        return count_text(args.path, args.limit)
    return print_headings()


if __name__ == "__main__":
    sys.exit(main())
