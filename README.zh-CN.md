# Codex Self-Improving Loop

**给 Codex 增加一套本地、可审查、可持续升级的自改进闭环。**

Codex Self-Improving Loop 可以帮助 Codex 跨会话回忆、沉淀稳定偏好、提出可复用技能、扫描不安全候选，并通过一套受控的学习流程持续演进。

它适合希望 Codex 越用越贴合自己工程习惯的开发者，同时避免让 Agent 不受控制地改写自己的长期行为。

[English README](./README.md)

![Codex Self-Improving Loop WebUI Dashboard](docs/assets/webui-dashboard.png)

## 你会得到什么

| 能力         | 作用                                                            | 默认输出                                 |
| ------------ | --------------------------------------------------------------- | ---------------------------------------- |
| 跨会话检索   | 搜索历史 Codex 会话，返回短片段并脱敏                           | 终端输出                                 |
| 记忆候选     | 提取稳定偏好、安全修正和长期经验                                | `$HOME/.codex/memories/inbox`            |
| 记忆晋升     | 将一条已审查记忆写入全局 `USER.md`                              | `$HOME/.codex/memories/USER.md`          |
| 候选评分     | 找出重复、短小、安全的记忆候选                                  | 终端或 JSON 报告                         |
| 技能候选     | 捕获未来可能变成 skill 的复用流程                               | `$HOME/.codex/skill-candidates/inbox`    |
| 技能补丁候选 | 捕获已有 skill 需要升级的证据                                   | `$HOME/.codex/skill-candidates/patches`  |
| 安全扫描     | 标记密钥、私有 URL、脱敏值、prompt injection 文本和原始转录痕迹 | 终端或 Markdown 报告                     |
| 任务结束提醒 | 在任务交付前运行 review-mode 学习闭环                           | `$HOME/.codex/nudge-reports`             |
| 会话监听器   | 轮询 Codex 会话文件，并在空闲后自动运行 nudge                   | `$HOME/.codex/memory-watcher-state.json` |
| 使用元数据   | 记录 skill 的 `use_count`、`last_used` 和失败次数               | `$HOME/.codex/skill-usage.json`          |
| 学习报告     | 生成技能索引和学习 inbox 汇总                                   | `$HOME/.codex/*.md`                      |
| 本地 Dashboard | 生成只读单 HTML 页面，用于查看今日记录、历史记录、全量汇总和复制命令 | `$HOME/.codex/codex-self-improving-loop-dashboard.html` |

## 为什么需要它

很多 AI 编程 Agent 在单次会话里表现很好，但跨会话后容易丢失协作上下文。用户需要反复说明偏好、项目规则、验证习惯和之前踩过的坑。

本项目把会话经验转化为可治理的资产：

```text
任务经验
  -> 可审查候选
  -> 安全扫描和评分
  -> 显式晋升或归档
  -> 未来会话回忆和技能演进
```

它不是把所有聊天记录塞进长期记忆，而是建立干净的学习闭环：

- 稳定用户偏好进入全局记忆。
- 项目事实留在项目级 `AGENTS.md`。
- 可复用流程进入 skill candidate。
- 有风险或含糊的内容停留在 review。
- 密钥和脱敏值被阻断。

## 设计原则

本项目借鉴 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的 self-improving loop 思路：记忆、可复用技能、会话检索，以及提醒 Agent 主动保存经验的 nudge 机制。

Codex Self-Improving Loop 将这个思路适配成一个更轻量的 Codex 本地工具：

| 原则         | 实现                                                         |
| ------------ | ------------------------------------------------------------ |
| 本地优先     | 文件保存在 `$HOME/.codex` 和 `$HOME/.agents`，不依赖托管服务 |
| 先审查后晋升 | 自动化只生成候选，长期行为变更必须显式确认                   |
| 跨平台       | 只使用 Python 标准库，不依赖特定 shell                       |
| Agent 可读   | skill 是普通 `SKILL.md`，脚本小而清晰                        |
| 复制式安装   | `install.py` 复制仓库文件，不内嵌大段生成内容                |
| 默认安全     | 疑似密钥和脱敏值会阻止晋升                                   |

## 它不是什么

- 不是 Codex 的替代品。
- 不是向量数据库或托管记忆服务。
- 不会自动修改业务代码。
- 不会自动启用新生成的 skill。
- 不会让不安全的记忆变安全；它只负责发现、标记和隔离风险。

## 环境要求

- Python 3.10 或更高版本。
- Codex 能从 `$HOME/.agents/skills` 发现 skills。

不需要任何第三方 Python 包。

## 快速开始

```bash
git clone https://github.com/newcatshuang/codex-self-improving-loop.git
cd codex-self-improving-loop
python install.py
```

安装后重启 Codex 或打开新会话，让 skill discovery 重新加载文件。

用临时目录验证安装：

```bash
python tests/verify-install.py --codex-root /tmp/codex-sil --agents-root /tmp/agents-sil
```

Windows 用户也可以使用任意临时路径：

```bash
python tests/verify-install.py --codex-root C:/Temp/codex-sil --agents-root C:/Temp/agents-sil
```

## 安装细节

自定义安装目录：

```bash
python install.py --codex-root /tmp/codex-test --agents-root /tmp/agents-test --force
```

安装器会：

- 将 `agents/skills/session-recall` 复制到 `$HOME/.agents/skills/session-recall`。
- 将 `agents/skills/memory-capture` 复制到 `$HOME/.agents/skills/memory-capture`。
- 在 `$HOME/.codex` 下创建学习 inbox 目录。
- 仅在 `USER.md` 不存在时，将 `codex/memories/USER.template.md` 复制过去。
- 用幂等 marker 将 `codex/AGENTS.learning-block.md` 追加到 `$HOME/.codex/AGENTS.md`。

## 日常使用

搜索历史会话：

```bash
python "$HOME/.agents/skills/session-recall/scripts/search_sessions.py" --query "previous error" --max-results 10
```

从最近会话提取记忆候选：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/extract_memory.py" --max-messages 40
```

晋升一条已审查记忆：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/promote_memory.py" \
  --text "Prefer concise engineering handoffs with verification and residual risk." \
  --approved
```

运行任务结束自改进闭环：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_memory_nudge.py"
```

打开本地 review dashboard：

```text
$HOME/.codex/codex-self-improving-loop-dashboard.html
```

Dashboard 默认展示当天记录，也可以直接在页面里切换历史日期，不需要手动选择候选文件。页面包含当前所有记录的汇总，并且只提供复制建议命令或改写文本，不会写入文件或执行脚本。

## WebUI Dashboard

Dashboard 是一个本地只读的学习候选审阅界面。它读取共享的 `$HOME/.codex/learning-index.json` 快照，并把这份数据嵌入到一个单 HTML 文件中，因此不需要启动 Web 服务，直接用浏览器打开即可。

它适合用来：

- 默认查看当天生成的 memory、skill、skill patch 候选。
- 在页面中切换历史日期，不需要手动定位候选文件。
- 通过彩色汇总卡片区分全局记忆、项目 `AGENTS.md`、skill candidate、skill patch、manual review 和 blocked review。
- 在右侧审阅栏查看候选内容、改写建议、来源文件和可复制的晋升命令。
- 只复制建议命令或改写文本；页面本身不会写入文件，也不会执行脚本。

手动生成或刷新：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/build_learning_index.py"
python "$HOME/.agents/skills/memory-capture/scripts/render_dashboard.py"
```

每日 watcher 和 `codex_memory_nudge.py` 也会自动刷新：

```text
$HOME/.codex/codex-self-improving-loop-dashboard.html
```

运行自动会话监听器。长期运行模式下，默认每天轮询一次，并处理至少空闲 10 分钟的会话文件：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py"
```

测试一次监听器扫描：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once --dry-run
```

如果使用 cron、launchd、systemd timer 或 Windows Task Scheduler 等系统调度器，建议每天 12:00 调度一次真实扫描。默认会静默运行，并刷新 WebUI Dashboard 供你审阅：

```bash
python install_watcher_schedule.py
```

Windows 下只有在排查问题、需要终端窗口停留查看摘要时，才使用 `--pause-on-exit`：

```bash
python install_watcher_schedule.py --pause-on-exit
```

生成维护报告：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/generate_skills_index.py"
python "$HOME/.agents/skills/memory-capture/scripts/summarize_learning_inbox.py"
python "$HOME/.agents/skills/memory-capture/scripts/render_dashboard.py"
python "$HOME/.agents/skills/memory-capture/scripts/show_skill_usage.py"
```

## 命令索引

| 脚本                               | 作用                                    |
| ---------------------------------- | --------------------------------------- |
| `search_sessions.py`               | 搜索本地 Codex 会话并脱敏输出           |
| `extract_memory.py`                | 从最近会话生成记忆候选                  |
| `promote_memory.py`                | 将一条已审查记忆写入 `USER.md`          |
| `promote_candidates.py`            | 评分、可选自动晋升、归档已处理记忆候选  |
| `compact_user_memory.py`           | 检查全局记忆预算、重复、冲突和安全风险  |
| `extract_skill_candidate.py`       | 生成 review-only 技能候选               |
| `extract_skill_patch_candidate.py` | 生成 review-only 技能补丁候选           |
| `scan_skill_candidates.py`         | 扫描技能候选和补丁候选的安全风险        |
| `record_skill_usage.py`            | 记录 skill 使用元数据                   |
| `show_skill_usage.py`              | 展示 skill 使用元数据                   |
| `generate_skills_index.py`         | 根据已安装 `SKILL.md` 生成技能索引      |
| `build_learning_index.py`          | 生成 digest 和 Dashboard 共用的 `learning-index.json` |
| `summarize_learning_inbox.py`      | 生成 Review Digest，汇总记忆、技能、补丁、归属、改写建议和晋升选项 |
| `render_dashboard.py`              | 生成只读本地 HTML Dashboard，支持今日/历史切换和复制命令 |
| `codex_memory_nudge.py`            | 运行完整 review-mode 学习闭环           |
| `codex_session_watcher.py`         | 监听会话文件，并在空闲后自动运行 nudge  |
| `install_watcher_schedule.py`      | 为已安装 watcher 配置每天 12:00 系统调度 |

## 仓库结构

```text
codex-self-improving-loop/
├─ README.md
├─ README.zh-CN.md
├─ LICENSE
├─ install.py
├─ install_watcher_schedule.py
├─ tests/
│  └─ verify-install.py
├─ codex/
│  ├─ AGENTS.learning-block.md
│  └─ memories/
│     └─ USER.template.md
└─ agents/
   └─ skills/
      ├─ session-recall/
      │  ├─ SKILL.md
      │  └─ scripts/
      │     └─ search_sessions.py
      └─ memory-capture/
         ├─ SKILL.md
         ├─ scripts/
         │  ├─ codex_memory_nudge.py
         │  ├─ codex_session_watcher.py
         │  ├─ compact_user_memory.py
         │  ├─ extract_memory.py
         │  ├─ extract_skill_candidate.py
         │  ├─ extract_skill_patch_candidate.py
         │  ├─ generate_skills_index.py
         │  ├─ build_learning_index.py
         │  ├─ learning_loop_common.py
         │  ├─ promote_candidates.py
         │  ├─ promote_memory.py
         │  ├─ record_skill_usage.py
         │  ├─ render_dashboard.py
         │  ├─ scan_skill_candidates.py
         │  ├─ show_skill_usage.py
         │  └─ summarize_learning_inbox.py
         └─ templates/
            └─ dashboard.html
```

## 运行时输出

默认运行时输出位于 `$HOME/.codex`：

```text
.codex/
├─ memories/
│  ├─ USER.md
│  ├─ inbox/
│  └─ archive/
├─ skill-candidates/
│  ├─ inbox/
│  ├─ patches/
│  └─ archive/
├─ daily-digests/
├─ nudge-reports/
├─ latest-skill-candidate-security-scan.md
├─ latest-user-memory-budget.md
├─ learning-index.json
├─ codex-self-improving-loop-dashboard.html
├─ memory-watcher-state.json
├─ skill-usage.json
├─ skills-index.md
└─ learning-inbox-summary.md
```

生成的候选文件会按日期分目录保存，例如 `$HOME/.codex/memories/inbox/YYYY/MM/DD/*.md`，但默认不会写入空候选报告。`$HOME/.codex/learning-index.json` 每次运行覆盖写入，作为 Dashboard 和轻量每日 Digest 共用的数据层。每日 Markdown 主入口是 `$HOME/.codex/daily-digests/YYYY/MM/DD/review-digest.md`，可视化 review 主入口是 `$HOME/.codex/codex-self-improving-loop-dashboard.html`。安全扫描和记忆预算报告会覆盖写入 `latest-*` 路径，减少文件数量。详细 nudge 报告只在发现候选或步骤失败时写入。

## 自动会话监听器

不同 Codex 运行环境不一定都有可靠的 session-end hook。监听器提供一个轻量外部触发方式：

```text
轮询 $HOME/.codex/sessions
  -> 找到空闲且未处理的 session 文件
  -> 运行 codex_memory_nudge.py --session-file <file>
  -> 写入每日 digest、latest 报告、必要时的 nudge report 和 watcher state
```

默认参数：

| 参数                     | 默认值 |
| ------------------------ | -----: |
| `--interval-seconds`     | `86400` |
| `--idle-seconds`         |  `600` |
| `--max-sessions-per-run` |    `0` |

`--max-sessions-per-run 0` 表示当前轮次处理全部 ready session。它是默认值，因为 watcher 主要是本地 I/O 操作，并且通过锁文件和 processed-session state 避免重复处理。

默认情况下，首次运行会处理所有已经空闲、且未标记为 processed 的历史 session。只有需要限制处理窗口时，才显式传入 `--since-date YYYY-MM-DD`。

监听器仍然是 review-first：它会自动生成候选报告，但不会执行 `promote_memory.py --approved`，不会应用 skill patch，也不会把候选自动晋升到 `USER.md`。

每次真实 watcher 执行完成后，nudge 会在终端输出 Review Digest 摘要，并写入 `$HOME/.codex/learning-index.json`、`$HOME/.codex/learning-inbox-summary.md`、`$HOME/.codex/daily-digests/YYYY/MM/DD/review-digest.md` 和 `$HOME/.codex/codex-self-improving-loop-dashboard.html`。Dashboard 是主要审阅入口。每日 Digest 会保持轻量：指向 Dashboard 和共享索引，并列出紧凑的待处理队列。归属会区分全局 `USER.md`、项目级 `AGENTS.md`、skill candidate、skill patch、blocked review 和 manual review。记忆候选会用改写建议生成显式的 `promote_memory.py --approved` 命令；技能和补丁仍保持 review-only，需要先扫描并人工检查目标 skill 后再应用。

候选抽取会同时读取用户指令和 assistant 的最终结论，更偏向根因、修复方案、验证结果、可复用流程、稳定偏好和安全修正。一类一次性任务请求，例如“帮我查 X”“列出 Y”“只返回 Z”，会被视为当前工作项，而不是长期记忆。

示例：

```bash
# 长期运行
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py"

# 只扫描一次，不写报告
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once --dry-run

# 真实执行一次
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once

# 只处理指定日期之后的 session
python "$HOME/.agents/skills/memory-capture/scripts/codex_session_watcher.py" --once --since-date 2026-05-01

# 重新生成只读本地 Dashboard
python "$HOME/.agents/skills/memory-capture/scripts/build_learning_index.py"
python "$HOME/.agents/skills/memory-capture/scripts/render_dashboard.py"

# 安装每天 12:00 执行的系统调度，实际运行 $HOME/.agents 下已安装的 watcher
python install_watcher_schedule.py

# 仅 Windows 调试：执行完成后保留终端窗口，方便查看摘要
python install_watcher_schedule.py --pause-on-exit
```

对个人工作站来说，用系统调度器在每天 12:00 运行一次 `--once` 通常比长期占用一个终端进程更可靠。Windows 默认调度会尽量使用无窗口的 Python 运行器；结果从 WebUI Dashboard 审阅，不再依赖暂停的终端窗口。已有进程管理器时，也可以直接使用长期运行模式。

调度安装脚本后端：

| 平台    | 后端                                |
| ------- | ----------------------------------- |
| Windows | Task Scheduler，通过 `schtasks.exe /SC DAILY /ST 12:00` |
| Linux   | systemd user timer，使用 `OnCalendar=*-*-* 12:00:00` |
| macOS   | `launchd` LaunchAgent，使用 `Hour=12`、`Minute=0` |

## 安全模型

本项目刻意把“发现”和“晋升”分开。

| 阶段    | 行为                                                              |
| ------- | ----------------------------------------------------------------- |
| Capture | 写入 review-only 候选文件                                         |
| Scan    | 标记密钥、脱敏值、prompt injection 文本、私有 URL 和转录痕迹      |
| Score   | 找出重复、短小、安全的偏好候选                                    |
| Promote | 默认需要显式 `--approved`，仅保留保守的 `--auto-promote` 候选流程 |
| Archive | 只移动已处理候选，未解决 review 项继续留在 inbox                  |

硬规则：

- 不在记忆文件中存储原始密钥。
- 不还原 `[REDACTED]` 值。
- `conflict_review` 是自动晋升的硬停止条件。
- 项目事实写入项目级 `AGENTS.md`，不要写进全局 `USER.md`。
- 技能候选必须审查和扫描后才能变成真实 skill。

## 开发

运行本地验证：

```bash
python tests/verify-install.py --codex-root ./tmp/codex --agents-root ./tmp/agents
python tests/verify-learning-extraction.py --work-root ./tmp/learning
```

运行语法检查：

```bash
python -m compileall agents install.py install_watcher_schedule.py tests
```

## 灵感来源

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)：围绕 memory、skill creation、skill evolution、session search 和 learning nudge 构建的 self-improving agent loop。

## License

MIT
