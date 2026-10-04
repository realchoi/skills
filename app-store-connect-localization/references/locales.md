# 语种参考

开始翻译前读一遍。包含两部分：

1. 小节标题对照表：「此版本的新增内容」里每个小节的标题，每个语种固定用这一套词。
2. 各语种要点：引号、称呼、拼写、地区差异等容易出错的地方。

## 1. 小节标题对照表

校验脚本 `scripts/asc_check.py` 按这张表识别小节（可用 `python3 scripts/asc_check.py headings` 打印）。小节标题必须逐字使用表中的词，不加冒号、序号或符号；想改某个词时，脚本里的 `LOCALES` 和这张表一起改。

「优化」一栏：英语用 Changed、日语用 変更、简体中文用 优化；其他语种取「改进 / Improvements」义，这是这类说明在 App Store 上最常见、也最贴合中文原意的说法。

| ASC 名称 | 代码 | 新增 | 优化 | 修复 | 性能 | 安全 | 移除 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 英语（美国） | en-US | Added | Changed | Fixed | Performance | Security | Removed |
| 阿拉伯语 | ar-SA | جديد | تحسينات | إصلاحات | الأداء | الأمان | ما تمت إزالته |
| 北印度语 | hi | नया | सुधार | बग फ़िक्स | परफ़ॉर्मेंस | सुरक्षा | हटाया गया |
| 波兰语 | pl | Nowości | Ulepszenia | Poprawki | Wydajność | Bezpieczeństwo | Usunięte |
| 丹麦语 | da | Nyt | Forbedringer | Rettelser | Ydeevne | Sikkerhed | Fjernet |
| 德语 | de-DE | Neu | Verbesserungen | Fehlerbehebungen | Leistung | Sicherheit | Entfernt |
| 俄语 | ru | Новое | Улучшения | Исправления | Производительность | Безопасность | Удалено |
| 法语 | fr-FR | Nouveautés | Améliorations | Corrections | Performances | Sécurité | Suppressions |
| 法语（加拿大） | fr-CA | Nouveautés | Améliorations | Corrections | Performances | Sécurité | Suppressions |
| 繁体中文 | zh-Hant | 新增 | 改進 | 修正 | 效能 | 安全性 | 移除 |
| 芬兰语 | fi | Uutta | Parannukset | Korjaukset | Suorituskyky | Tietoturva | Poistettu |
| 韩语 | ko | 추가 | 개선 | 수정 | 성능 | 보안 | 제거 |
| 荷兰语 | nl-NL | Nieuw | Verbeteringen | Opgelost | Prestaties | Beveiliging | Verwijderd |
| 加泰罗尼亚语 | ca | Novetats | Millores | Correccions | Rendiment | Seguretat | Eliminat |
| 简体中文 | zh-Hans | 新增 | 优化 | 修复 | 性能 | 安全 | 移除 |
| 捷克语 | cs | Novinky | Vylepšení | Opravy | Výkon | Zabezpečení | Odstraněno |
| 克罗地亚语 | hr | Novo | Poboljšanja | Ispravci | Performanse | Sigurnost | Uklonjeno |
| 罗马尼亚语 | ro | Noutăți | Îmbunătățiri | Remedieri | Performanță | Securitate | Eliminate |
| 马来语 | ms | Baharu | Penambahbaikan | Pembetulan | Prestasi | Keselamatan | Dialih keluar |
| 挪威语 | no | Nytt | Forbedringer | Rettelser | Ytelse | Sikkerhet | Fjernet |
| 葡萄牙语（巴西） | pt-BR | Novidades | Melhorias | Correções | Desempenho | Segurança | Removido |
| 葡萄牙语（葡萄牙） | pt-PT | Novidades | Melhorias | Correções | Desempenho | Segurança | Removido |
| 日语 | ja | 追加 | 変更 | 修正 | パフォーマンス | セキュリティ | 削除 |
| 瑞典语 | sv | Nytt | Förbättringar | Åtgärdat | Prestanda | Säkerhet | Borttaget |
| 斯洛伐克语 | sk | Novinky | Vylepšenia | Opravy | Výkon | Zabezpečenie | Odstránené |
| 泰语 | th | ใหม่ | ปรับปรุง | แก้ไข | ประสิทธิภาพ | ความปลอดภัย | นำออก |
| 土耳其语 | tr | Yeni | İyileştirmeler | Düzeltmeler | Performans | Güvenlik | Kaldırılanlar |
| 乌克兰语 | uk | Нове | Покращення | Виправлення | Продуктивність | Безпека | Вилучено |
| 西班牙语（墨西哥） | es-MX | Novedades | Mejoras | Correcciones | Rendimiento | Seguridad | Eliminado |
| 西班牙语（西班牙） | es-ES | Novedades | Mejoras | Correcciones | Rendimiento | Seguridad | Eliminado |
| 希伯来语 | he | חדש | שיפורים | תיקונים | ביצועים | אבטחה | הוסר |
| 希腊语 | el | Νέα | Βελτιώσεις | Διορθώσεις | Απόδοση | Ασφάλεια | Καταργήθηκαν |
| 匈牙利语 | hu | Újdonságok | Fejlesztések | Javítások | Teljesítmény | Biztonság | Eltávolítva |
| 意大利语 | it | Novità | Miglioramenti | Correzioni | Prestazioni | Sicurezza | Rimozioni |
| 印度尼西亚语 | id | Baru | Peningkatan | Perbaikan | Performa | Keamanan | Dihapus |
| 英语（澳大利亚） | en-AU | Added | Changed | Fixed | Performance | Security | Removed |
| 英语（加拿大） | en-CA | Added | Changed | Fixed | Performance | Security | Removed |
| 英语（英国） | en-GB | Added | Changed | Fixed | Performance | Security | Removed |
| 越南语 | vi | Mới | Cải tiến | Sửa lỗi | Hiệu năng | Bảo mật | Đã loại bỏ |

## 2. 各语种要点

所有语种通用：品牌和产品名（App 名、Pro、Mac、macOS）、按键（P、⌘、Esc）、文件扩展名（.jxl）、版本号保持原样；Apple 的系统功能与界面名词（废纸篓、程序坞、访达、旁白、液态玻璃等）用 Apple 在该语种的官方译名，没有把握时保留英文原名（Dock、Finder 在多数语言里本就不译）。同一语种内称呼方式前后一致，跨版本也保持一致。

字符数相对英文的大致倍数写在括号里（按 ASC 计数口径），用于预估长度：德语、法语、俄语等通常比英文长 20%–40%，是 4000 / 170 上限最先撞线的语种。

### 英语（美国）en-US（1.0×）
- 美式拼写。新增条目以 "Added …" 开头；修复条目用 "Fixed an issue where …" 或 "Fixed … not …"；优化与性能条目用现在时描述新行为（"X now …"）。
- 界面文字用 App 中的实际英文字符串，以 "…" 引用，大小写照抄。
- 付费功能标注如 "(requires Pro)"。

### 阿拉伯语 ar-SA（≈1.0×）
- 现代标准阿拉伯语，从右到左书写；逗号用「،」，问号用「؟」。
- 拉丁字母的名称与按键直接嵌入，不要音译；引号用 «…» 或 "…"。
- 按逻辑顺序书写：`.tif` 这类以标点开头的拉丁片段照原样写在它在句中的位置，不要因为显示方向把标点挪到另一侧；也不要插入 LRM / RLM 等不可见方向控制符。

### 北印度语 hi（≈1.1×）
- 天城文书写，句末用「।」；用尊称 आप。
- 技术词沿用 Apple 印地语界面里常见的英语借词（ऐप、सेटिंग्स、फ़ोल्डर、फ़ोटो），不要硬造梵语化生词。

### 波兰语 pl（≈1.2×）
- 引号 „…”；App 名不变格，需要变格时借助 aplikacja 等名词承担词尾。

### 丹麦语 da（≈1.1×）
- 称呼用 du；复合词合写。

### 德语 de-DE（≈1.3×）
- 引号 „…“；名词首字母大写；复合词合写或用连字符（JPEG-XL-Bilder）。
- 称呼用 du（Apple 德语营销文案的用法，小写）。
- 长度最容易超限，推广文本尤其要精简改写，而不是逐词直译。

### 俄语 ru（≈1.2×）
- 引号 «…»；称呼用 вы（小写）。

### 法语 fr-FR（≈1.3×）
- 引号 « … »，内侧留空格；: ; ! ? 前留空格。这些空格最好是不换行空格（U+00A0），避免标点单独折到下一行；直接输出不可见字符容易出错，可以先写普通空格，写完后用脚本统一替换。
- 称呼用 vous。

### 法语（加拿大）fr-CA（≈1.3×）
- 魁北克用词习惯（courriel 等），不要直接复制法国版。
- 冒号前加空格，; ! ? 前不加空格；称呼用 vous；引号 « … »，空格处理同法语（法国）。

### 繁体中文 zh-Hant（≈0.35×）
- 面向台湾用户，用台湾用语与 macOS 繁体中文的官方译名：檔案、資料夾、設定、視窗、選單、快速鍵、縮圖、匯出、裁切、預設、支援、效能、介面、垃圾桶。
- 引号用「」，标点全角。不能只做简繁字形转换。

### 芬兰语 fi（≈1.3×）
- 引号 ”…”（两侧同形）；称呼用 sinä 的动词形式。

### 韩语 ko（≈0.5×）
- 用 합니다체：新增「…을/를 추가했습니다.」，修复「… 문제를 수정했습니다.」。
- 按韩语习惯分写（띄어쓰기）；引号 '…' 或 "…"。

### 荷兰语 nl-NL（≈1.2×）
- 称呼用 je / jij；引号 '…' 或 "…"。

### 加泰罗尼亚语 ca（≈1.2×）
- 引号 «…»；中间点用 l·l。

### 简体中文 zh-Hans（≈0.35×）
- 源文本是简体中文时，这里放定稿后的母版，不另行改写。
- 写法见 `references/format.md` 第 5 节。

### 捷克语 cs（≈1.2×）
- 引号 „…“。

### 克罗地亚语 hr（≈1.2×）
- 引号 „…“ 或 »…«，全文统一一种。

### 罗马尼亚语 ro（≈1.3×）
- 用逗号下加符的 ș ț，不要用软音符的 ş ţ；引号 „…”。

### 马来语 ms（≈1.3×）
- 马来西亚标准马来语，和印尼语区分：fail（文件）、tetapan（设置）、aplikasi、muat turun。

### 挪威语 no（≈1.1×）
- 书面挪威语（Bokmål）；引号 «…»；称呼用 du。

### 葡萄牙语（巴西）pt-BR（≈1.2×）
- 巴西用词：arquivo、tela、usuário、salvar、configurações；称呼用 você。

### 葡萄牙语（葡萄牙）pt-PT（≈1.2×）
- 欧洲葡萄牙语用词：ficheiro、ecrã、utilizador、guardar、definições；不要直接复用巴西版。

### 日语 ja（≈0.55×）
- 每条以小节名加全角冒号开头（追加：／変更：／修正：／パフォーマンス：／セキュリティ：／削除：），以「〜しました。」「〜を修正しました。」结句。
- 日文与拉丁字母、数字之间不加空格（Pで採用、macOS 26では）；界面文字用 App 日语界面的实际字符串，以「」引用。
- 付费功能标注如「（Proが必要）」。

### 瑞典语 sv（≈1.1×）
- 引号 ”…”（两侧同形）；称呼用 du。

### 斯洛伐克语 sk（≈1.2×）
- 引号 „…“。

### 泰语 th（≈1.0×）
- 词与词之间不加空格，用空格分隔分句和句子；句末不用句号。
- 拉丁字母的名称前后各留一个空格。

### 土耳其语 tr（≈1.2×）
- 注意 İ/i 与 I/ı 的大小写对应（大写 i 是 İ）。

### 乌克兰语 uk（≈1.2×）
- 引号 «…»；不要混入俄语词汇和字母（ы、э、ъ、ё 不属于乌克兰语）。

### 西班牙语（墨西哥）es-MX（≈1.2×）
- 拉美用词：computadora、celular、archivo；称呼用 tú，复数用 ustedes，不用 vosotros。

### 西班牙语（西班牙）es-ES（≈1.2×）
- 西班牙用词：ordenador、móvil；称呼用 tú；引号 «…»。

### 希伯来语 he（≈0.9×）
- 从右到左书写；拉丁字母的名称与按键直接嵌入，前缀字母与拉丁词之间用连字符（ב-Mac、ו-HEIF）。
- 按逻辑顺序书写：`.tif` 这类以标点开头的拉丁片段照原样写，不要把点挪到词尾；不插入 LRM / RLM 等不可见字符。

### 希腊语 el（≈1.3×）
- 引号 «…»；问号写作「;」（希腊问号）。

### 匈牙利语 hu（≈1.3×）
- 引号 „…”。

### 意大利语 it（≈1.2×）
- 称呼用 tu；引号 «…» 或 "…"，全文统一。

### 印度尼西亚语 id（≈1.2×）
- 印尼用词：berkas / file、pengaturan（设置）、unduh；和马来语区分。

### 英语（澳大利亚）en-AU（1.0×）
- 在 en-US 基础上改为英式拼写：colour、organise、centre、licence（名词）。
- 指 macOS 的系统废纸篓时写 Bin；引用 App 界面文字时仍照抄 App 实际字符串。

### 英语（加拿大）en-CA（1.0×）
- 加拿大拼写：colour、centre、licence（名词），但动词用 -ize（organize、customize）。

### 英语（英国）en-GB（1.0×）
- 英式拼写：colour、organise、centre、licence（名词）；指系统废纸篓时写 Bin。

### 越南语 vi（≈1.2×）
- 声调用预组合字符（NFC），校验脚本会对非 NFC 文本发出警告。
