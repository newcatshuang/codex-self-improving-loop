# Codex Self-Improving Loop

**给 Codex 增加一套本地、可审查、可持续升级的自改进闭环。**

Codex Self-Improving Loop 可以帮助 Codex 跨会话回忆、沉淀稳定偏好、提出可复用技能、扫描不安全候选，并通过一套受控的学习流程持续演进。

它适合希望 Codex 越用越贴合自己工程习惯的开发者，同时避免让 Agent 不受控制地改写自己的长期行为。

[English README](./README.md)

## 你会得到什么

| 能力         | 作用                                                            | 默认输出                                |
| ------------ | --------------------------------------------------------------- | --------------------------------------- |
| 跨会话检索   | 搜索历史 Codex 会话，返回短片段并脱敏                           | 终端输出                                |
| 记忆候选     | 提取稳定偏好、安全修正和长期经验                                | `$HOME/.codex/memories/inbox`           |
| 记忆晋升     | 将一条已审查记忆写入全局 `USER.md`                              | `$HOME/.codex/memories/USER.md`         |
| 候选评分     | 找出重复、短小、安全的记忆候选                                  | 终端或 JSON 报告                        |
| 技能候选     | 捕获未来可能变成 skill 的复用流程                               | `$HOME/.codex/skill-candidates/inbox`   |
| 技能补丁候选 | 捕获已有 skill 需要升级的证据                                   | `$HOME/.codex/skill-candidates/patches` |
| 安全扫描     | 标记密钥、私有 URL、脱敏值、prompt injection 文本和原始转录痕迹 | 终端或 Markdown 报告                    |
| 任务结束提醒 | 在任务交付前运行 review-mode 学习闭环                           | `$HOME/.codex/nudge-reports`            |
| 使用元数据   | 记录 skill 的 `use_count`、`last_used` 和失败次数               | `$HOME/.codex/skill-usage.json`         |
| 学习报告     | 生成技能索引和学习 inbox 汇总                                   | `$HOME/.codex/*.md`                     |

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

生成维护报告：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/generate_skills_index.py"
python "$HOME/.agents/skills/memory-capture/scripts/summarize_learning_inbox.py"
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
| `summarize_learning_inbox.py`      | 汇总记忆、技能、补丁、扫描和 usage 信号 |
| `codex_memory_nudge.py`            | 运行完整 review-mode 学习闭环           |

## 仓库结构

```text
codex-self-improving-loop/
├─ README.md
├─ README.zh-CN.md
├─ LICENSE
├─ install.py
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
         └─ scripts/
            ├─ codex_memory_nudge.py
            ├─ compact_user_memory.py
            ├─ extract_memory.py
            ├─ extract_skill_candidate.py
            ├─ extract_skill_patch_candidate.py
            ├─ generate_skills_index.py
            ├─ learning_loop_common.py
            ├─ promote_candidates.py
            ├─ promote_memory.py
            ├─ record_skill_usage.py
            ├─ scan_skill_candidates.py
            ├─ show_skill_usage.py
            └─ summarize_learning_inbox.py
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
├─ nudge-reports/
├─ skill-usage.json
├─ skills-index.md
└─ learning-inbox-summary.md
```

这些是本地运行状态，不应提交，除非你已经人工整理并确认。

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
```

运行语法检查：

```bash
python -m compileall agents install.py tests
```

## 灵感来源

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)：围绕 memory、skill creation、skill evolution、session search 和 learning nudge 构建的 self-improving agent loop。

## License

MIT
