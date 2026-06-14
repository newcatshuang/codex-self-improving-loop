# Codex Self-Improving Loop

**一个只面向本机的 Codex 自改进 SQLite + WebUI 控制台。**

Codex Self-Improving Loop 帮助 Codex 跨会话检索、提取长期记忆候选、识别可复用 skill 候选、提出 skill patch，并通过一个本地 WebUI 完成审阅和晋升管理。

v3 架构不再生成大量 Markdown/JSON 产物，而是使用一个 SQLite 数据库和一个临时 Python 后端。后端只绑定 `127.0.0.1`，启动时生成 token，只允许本机访问。

[English README](./README.md)

## 你会得到什么

| 能力 | v3 实现方式 |
| --- | --- |
| 跨会话检索 | `sil.py recall` 优先使用 SQLite FTS 搜索会话和候选，并返回脱敏短片段；不可用时回退到普通搜索 |
| 记忆候选 | 每日或手动扫描提取 memory candidate，写入 SQLite |
| 技能候选 | 可复用流程写入 `type=skill` 候选 |
| 技能补丁 | 已有 skill 改进建议写入 `type=skill_patch` 候选 |
| WebUI 管理 | `sil.py serve --open` 启动本地后端，并打开总览 / 审阅工作流 / 运维与历史控制台 |
| 审阅建议 | 每条候选生成确定性的审阅建议，并保留后续接入 Codex 审阅的扩展点 |
| LLM 分析包 | Codex 可分析候选证据、风险、改写质量，并在审阅工作流中展示需要人工审批的进化建议目标 |
| 候选合并 | 相似候选会聚合成合并建议；应用合并只更新状态，原始 evidence 仍保留 |
| 晋升预览 | 写入 USER.md、AGENTS.md、skill、skill patch 前先展示 diff |
| 每日 digest | scan/rebuild 后写入一条 SQLite digest，包含候选、风险、skill 使用和失败运行统计 |
| 备份迁移包 | 可导出 SQLite、记忆文件、skills、审计历史；导入前支持 dry-run 预览 |
| Skill 健康 | 基于使用记录和补丁候选生成 `active`、`cold`、`needs_patch`、`duplicate_suspected` 状态 |
| 审计与历史 | WebUI 可查看审计日志、审阅历史、晋升历史和回滚预览 |
| 每日扫描 | `sil.py schedule install` 准备每天 03:00 扫描 |
| 桌面快捷方式 | `sil.py shortcut install` 准备一键启动入口 |

## 运行时目录

本项目所有运行时文件统一放在：

```text
$HOME/.codex/self-improving-loop/
├─ self-improving-loop.sqlite
├─ codex-self-improving-loop.html
├─ self-improving-loop.log
├─ backups/
├─ exports/
├─ web/
│  ├─ styles.css
│  └─ app.js
└─ tmp/
```

v3 默认不再生成候选 Markdown、`learning-index.json`、`latest-*` 报告、usage JSON 或 watcher state。每日审阅摘要会作为一条 SQLite digest 记录保存，需要时再从 WebUI 导出 Markdown。

## 安装

```bash
git clone https://github.com/newcatshuang/codex-self-improving-loop.git
cd codex-self-improving-loop
python install.py
```

安装器会复制：

- `sil.py` 和 `src/codex_sil` 到 `$HOME/.agents/codex-self-improving-loop`。
- `session-recall` 和 `memory-capture` skills 到 `$HOME/.agents/skills`。
- `codex/memories/USER.template.md` 到 `$HOME/.codex/memories/USER.md`，仅在目标不存在时复制。

`$HOME/.agents/codex-self-improving-loop` 是安装后的运行副本，定时任务、桌面快捷方式和 skills 都指向这份副本。这样即使 Git 仓库目录被移动、改名或删除，本机循环仍能继续工作。

安装器不会再向全局 `AGENTS.md` 写入规则。如果旧版本曾向 `$HOME/.codex/AGENTS.md` 写入 `codex-self-improving-loop` 管理块，安装器会清理该块，避免普通会话被全局提示污染。

## 日常使用

启动临时本地 WebUI 后端：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open
```

WebUI 按三个工作区组织：

- `总览`：首次运行向导、统计卡片、每日 digest、下一步建议、待审阅数量、风险观察、优先审阅候选、最近晋升、最近运行和错误提示。
- `审阅工作流`：候选队列、当前步骤引导、候选证据、审阅备注、LLM 分析、建议目标、建议理由、验证步骤、候选合并、晋升 diff 预览，以及 `人工审批操作台`。
- `运维与历史`：数据库初始化/备份/重建/扫描/导出、导入预览、调度和快捷方式、Skill 健康、跨会话检索、运行日志、审计日志、审阅历史、晋升历史、回滚预览、诊断，以及失败运行和审计信号的恢复复盘队列。

在运维区，Skill 同步和 `USER.md` 模板初始化是两个独立动作：`安装 / 更新技能` 只写 `$HOME/.agents/skills`，`初始化 USER.md 模板` 只在 `$HOME/.codex/memories/USER.md` 缺失时创建该文件。

`人工审批操作台` 是唯一会触发晋升写入的位置。LLM 分析可以建议写入 `USER.md`、`AGENTS.md`、skill 或 skill patch，但归档、拒绝、保存审阅、合并和晋升仍然都必须由用户明确点击，并经过确认弹窗。

回滚只做预览，不会自动覆盖文件；页面会展示目标路径、备份路径，以及可复制的 Python 恢复命令。

扫描新增会话：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" scan --once
```

备份数据库并全量重扫历史会话：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" rebuild --backup
```

搜索历史会话：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" recall --query "previous error"
```

安装辅助入口：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" schedule install
python "$HOME/.agents/codex-self-improving-loop/sil.py" shortcut install
```

定时任务安装支持跨平台：

- Windows：创建或替换 `CodexSelfImprovingLoop` 计划任务。
- macOS：写入并加载 `~/Library/LaunchAgents/com.codex.self-improving-loop.plist`。
- Linux：写入并启用 `$XDG_CONFIG_HOME/systemd/user` 或 `~/.config/systemd/user` 下的 `systemd --user` timer。

## 提取策略

扫描优先使用 Codex CLI 做更精准的结构化提取、分析和审阅建议：

```text
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --output-schema extraction.schema.json
```

当 Codex 不存在、执行失败、超时、JSON 非法或 schema 不合法时，才回退到内置规则提取和分析助手。

LLM 分析可以提出目标位置、建议文本、理由和验证步骤，但晋升始终只能通过 WebUI 人工触发。扫描器不会自动晋升 memory、AGENTS.md 事实、skill 或 skill patch。

`--ephemeral` 用于避免自动化提取本身产生新的 session 文件，导致下一轮重复扫描。

测试或快速历史全量重建时，可以设置 `CODEX_SIL_DISABLE_CODEX=1` 强制使用确定性 fallback 提取器。每日定时扫描默认不设置该变量，因此仍会优先尝试 Codex。

## 本地服务边界

- 后端只绑定 `127.0.0.1`。
- 不支持公网访问，不支持局域网访问。
- 每次 `serve` 启动都会生成 token，API 请求必须携带 token。
- 每日扫描不依赖后端常驻。
- WebUI 是日常审阅和晋升入口；正常流程不需要复制命令手动晋升。

## API 能力

除已有 scan、rebuild、schedule、review、promotion 接口外，WebUI 还使用这些仅本机可访问的 JSON API：

- `GET /api/setup/status`
- `GET /api/recommendations`
- `POST /api/candidates/{id}/recommend`
- `GET /api/candidates/{id}/analysis`
- `GET /api/merge-suggestions`
- `POST /api/merge-suggestions/refresh`
- `POST /api/merge-suggestions/{id}/apply`
- `GET /api/candidates/{id}/promotion-preview?target=user|agents|skill|patch`
- `GET /api/digests/latest`
- `GET /api/skills/health`
- `POST /api/export/bundle`
- `POST /api/import/preview`

## 验证

```bash
python tests/verify-v2-core.py --work-root ./tmp/v2-core
python tests/verify-codex-runner.py --work-root ./tmp/codex-runner
python tests/verify-v2-recall.py --work-root ./tmp/v2-recall
python tests/verify-v2-session-filter.py --work-root ./tmp/v2-filter
python tests/verify-v2-promotion.py --work-root ./tmp/v2-promotion
python tests/verify-v2-scheduler.py --work-root ./tmp/v2-scheduler
python tests/verify-webui-browser.py --work-root ./tmp/webui-browser
python tests/verify-v3-migration.py --work-root ./tmp/v3-migration
python tests/verify-v3-intelligence.py --work-root ./tmp/v3-intelligence
python tests/verify-v2-install.py --codex-root ./tmp/codex-v2 --agents-root ./tmp/agents-v2
python tests/verify-install.py --codex-root ./tmp/install-codex --agents-root ./tmp/install-agents
python -m compileall src sil.py install.py tests
```
