# CLAUDE.md

个人常用的 AI Agent Skills 仓库。每个顶层目录是一个独立的 skill，目录名就是 skill 名。`~/.claude/skills/` 下对应的是指向这些目录的软链接，所以仓库就是 skill 的唯一来源。

现有哪些 skill、各自做什么，以各目录 `SKILL.md` 的 `description` 为准，这里不另列清单，以免两处对不上。

## 目录结构

```text
<skill-name>/
├── SKILL.md          # 必需：YAML front matter（name、description）+ 正文工作流程
├── references/       # 可选：按需读取的参考文档，由 SKILL.md 指明何时读
└── scripts/          # 可选：skill 运行时调用的脚本
```

仓库根目录下的 `README.md`、`CLAUDE.md`、`.gitignore`，以及 skill-creator 评测时生成的 `<skill-name>-workspace/`（已被忽略），都不是 skill。

## 编写约定

- **语言**：SKILL.md、references 和脚本里的提示信息都用简体中文。中文与英文、数字之间加空格，标点用全角，引用界面文字用「」。
- **front matter**：`name` 用小写短横线格式，与目录名一致。`description` 是模型决定是否使用该 skill 的唯一依据，按这个顺序写：
  1. 做什么；
  2. 什么时候用，包括用户的典型说法；
  3. 边界：不做什么，相近的请求应该交给哪个 skill；
  4. 最后用一句 `Also use ...` 的英文补充触发场景。
- **SKILL.md 正文**：按编号步骤写工作流程，说明每一步为什么这样做。篇幅长的细节（格式规范、对照表、示例）放进 `references/`，正文里写明什么时候读哪个文件。用 `<skill>` 指代 skill 所在目录，例如 `python3 <skill>/scripts/xxx.py`。
- **脚本**：只用 Python 标准库，并兼容 macOS 自带的 `python3`（3.9），所以不用 `match` 语句和 `X | Y` 类型注解等 3.10+ 语法。输出中文，失败时退出码为 1。
- **可以机械判断的硬性条件**（字符上限、格式、完整性）写成脚本让模型实测，不在正文里要求模型凭感觉判断。
- **skill 之间的引用**：上下游或职责相近的 skill，在双方的 `description` 和正文里写明分工和衔接方式，避免两个 skill 抢同一类请求。

## 新增、改名与删除 skill

新增：

1. 建目录 `<skill-name>/`，写好 `SKILL.md`。
2. 如果和已有 skill 职责相近或有上下游关系，同步修改对方的 `description`，写清边界。
3. 如果有需要跨文件保持一致的内容，在下面的「各 skill 的维护说明」里加一节。
4. 建软链接并确认新会话能加载到：

   ```bash
   ln -s "$PWD/<skill-name>" ~/.claude/skills/<skill-name>
   claude -p "Without using any tools, list the names of the skills available to you. Output only the names, one per line."
   ```

改名：同时改目录名和 front matter 中的 `name`；用 `grep -rn '<旧名>' .` 找出其他 skill 里的引用一并更新；再删掉旧软链接（`rm ~/.claude/skills/<旧名>`，只删链接，不影响仓库）并按新名建一个。

删除：先用同样的 `grep` 确认没有其他 skill 引用它，再删目录和软链接。

## 安装与生效

- `~/.claude/skills/<skill-name>` 是指向本仓库对应目录的软链接，在仓库里的改动对新会话立即生效，改到一半的状态也会被加载。主工作区切换分支同样会改变生效的 skill，所以改动较大时在 `git worktree` 里改好再合并。
- `~/.claude/skills/synced/` 由 Claude 应用同步管理，与本仓库无关，不要改动。
- 用 `ls -l ~/.claude/skills` 查看现有链接；仓库里每个 skill 目录都应该有一条对应的链接。

## 各 skill 的维护说明

这里只记录读一遍代码不容易发现、改错了会出问题的约束。新增的 skill 有这类约束时，照下面的格式加一节，并附上检查命令。

### App Store Connect 系列

包括 `app-store-connect-copywriting`（根据代码变更撰写简体中文文案）和 `app-store-connect-localization`（翻译成 39 个语种）。前者的产出文件直接交给后者翻译，两者共用一套规范，修改时按下表同步：

| 内容 | 位置 |
| --- | --- |
| 文案规范 | 两个 skill 的 `references/format.md`，内容完全相同 |
| 校验脚本 | 两个 skill 的 `scripts/asc_check.py`，内容完全相同 |
| 各语种的小节标题 | `asc_check.py` 的 `LOCALES` 与 localization 的 `references/locales.md` 第 1 节表格 |
| 语种顺序（39 个） | `LOCALES` 的顺序、`locales.md` 表格的行序、localization `SKILL.md` 的「语种顺序」列表 |

改完后在仓库根目录运行，没有输出 diff 即为一致：

```bash
diff app-store-connect-{copywriting,localization}/references/format.md
diff app-store-connect-{copywriting,localization}/scripts/asc_check.py
diff <(python3 app-store-connect-localization/scripts/asc_check.py headings) \
     <(grep '^| ' app-store-connect-localization/references/locales.md)
diff <(python3 app-store-connect-localization/scripts/asc_check.py headings | awk -F' \\| ' 'NR>2{sub(/^\| /,"",$1); print NR-2". "$1}') \
     <(grep -E '^[0-9]+\. ' app-store-connect-localization/SKILL.md)
```

第三条比对小节标题表，第四条比对 SKILL.md 中的语种顺序列表。

这两个 skill 生成的文案文件（`asc-*.md`）按规范写到仓库根目录的上一级，不进版本库；在本仓库里测试时如果写到了仓库内，`.gitignore` 也会忽略它们。
