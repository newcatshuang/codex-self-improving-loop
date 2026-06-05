# Codex Self-Improving Loop

**一个只面向本机的 Codex 自改进 SQLite + WebUI 控制台。**

Codex Self-Improving Loop 帮助 Codex 跨会话检索、提取长期记忆候选、识别可复用 skill 候选、提出 skill patch，并通过一个本地 WebUI 完成审阅和晋升管理。

v2 架构不再生成大量 Markdown/JSON 产物，而是使用一个 SQLite 数据库和一个临时 Python 后端。后端只绑定 `127.0.0.1`，启动时生成 token，只允许本机访问。

[English README](./README.md)

## 你会得到什么

| 能力 | v2 实现方式 |
| --- | --- |
| 跨会话检索 | `sil.py recall` 搜索 SQLite 入库会话，并返回脱敏短片段 |
| 记忆候选 | 每日或手动扫描提取 memory candidate，写入 SQLite |
| 技能候选 | 可复用流程写入 `type=skill` 候选 |
| 技能补丁 | 已有 skill 改进建议写入 `type=skill_patch` 候选 |
| WebUI 管理 | `sil.py serve --open` 启动本地后端并打开控制台 |
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
└─ tmp/
```

v2 默认不再生成候选 Markdown、daily digest、`learning-index.json`、`latest-*` 报告、usage JSON 或 watcher state。

## 安装

```bash
git clone https://github.com/newcatshuang/codex-self-improving-loop.git
cd codex-self-improving-loop
python install.py
```

安装器会复制：

- `sil.py` 和 `src/codex_sil` 到 `$HOME/.agents/codex-self-improving-loop`。
- `session-recall` 和 `memory-capture` skills 到 `$HOME/.agents/skills`。
- `codex/AGENTS.learning-block.md` 到 `$HOME/.codex/AGENTS.md`。
- `codex/memories/USER.template.md` 到 `$HOME/.codex/memories/USER.md`，仅在目标不存在时复制。

`$HOME/.agents/codex-self-improving-loop` 是安装后的运行副本，定时任务、桌面快捷方式和 skills 都指向这份副本。这样即使 Git 仓库目录被移动、改名或删除，本机循环仍能继续工作。

## 日常使用

启动临时本地 WebUI 后端：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open
```

在 WebUI 中可以初始化数据库、清空当前 SQLite 数据并全量重扫历史会话、扫描会话、安装或移除每日定时任务、安装桌面快捷方式、导出审阅数据、归档或拒绝候选，并将确认后的候选晋升到 `USER.md`、项目 `AGENTS.md`、相互独立的 learned skills 或 skill patch 产物。

WebUI 还包含治理视图：审计日志、审阅历史、晋升历史和回滚预览。回滚只做预览，不会自动覆盖文件；页面会展示目标路径、备份路径，以及可复制的 Python 恢复命令。

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

扫描优先使用 Codex CLI 做更精准的结构化提取：

```text
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --output-schema extraction.schema.json
```

当 Codex 不存在、执行失败、超时、JSON 非法或 schema 不合法时，才回退到内置规则提取器。

`--ephemeral` 用于避免自动化提取本身产生新的 session 文件，导致下一轮重复扫描。

测试或快速历史全量重建时，可以设置 `CODEX_SIL_DISABLE_CODEX=1` 强制使用确定性 fallback 提取器。每日定时扫描默认不设置该变量，因此仍会优先尝试 Codex。

## 本地服务边界

- 后端只绑定 `127.0.0.1`。
- 不支持公网访问，不支持局域网访问。
- 每次 `serve` 启动都会生成 token，API 请求必须携带 token。
- 每日扫描不依赖后端常驻。
- WebUI 是日常审阅和晋升入口；正常流程不需要复制命令手动晋升。

## 验证

```bash
python tests/verify-v2-core.py --work-root ./tmp/v2-core
python tests/verify-codex-runner.py --work-root ./tmp/codex-runner
python tests/verify-v2-recall.py --work-root ./tmp/v2-recall
python tests/verify-v2-session-filter.py --work-root ./tmp/v2-filter
python tests/verify-v2-promotion.py --work-root ./tmp/v2-promotion
python tests/verify-v2-scheduler.py --work-root ./tmp/v2-scheduler
python tests/verify-v2-install.py --codex-root ./tmp/codex-v2 --agents-root ./tmp/agents-v2
python tests/verify-install.py --codex-root ./tmp/install-codex --agents-root ./tmp/install-agents
python -m compileall src sil.py install.py tests
```
