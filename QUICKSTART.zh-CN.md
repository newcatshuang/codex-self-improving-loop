# Codex Self-Improving Loop 快速使用

Codex Self-Improving Loop 是一套本地化的 Codex 自改进工具，用于跨会话检索、自动生成记忆/技能候选，并通过定时任务持续整理可复用经验。

## 安装

进入仓库目录：

```bash
cd codex-self-improving-loop
```

安装到默认位置：

```bash
python install.py --force
```

默认安装位置：

```text
$HOME/.agents/skills
$HOME/.codex
```

安装完成后，重启 Codex 或开启一个新会话，让 skill 列表重新加载。

## 验证安装

Windows：

```bash
python tests/verify-install.py --codex-root C:/Temp/codex-sil --agents-root C:/Temp/agents-sil
python tests/verify-learning-extraction.py --work-root C:/Temp/codex-sil-learning
python -m compileall agents install.py install_watcher_schedule.py tests
```

## 启用定时任务

安装每天 12:00 执行的系统调度。默认会静默运行，并刷新本地 Dashboard：

```bash
python install_watcher_schedule.py
```

Windows 下只有在排查问题、需要终端窗口停留查看摘要时，才使用：

```bash
python install_watcher_schedule.py --pause-on-exit
```

## 查看结果

本地 Dashboard 是最方便的查看入口，默认展示当天记录，也可以在页面中切换历史日期：

```text
$HOME/.codex/codex-self-improving-loop-dashboard.html
```

Dashboard 只用于查看和复制建议命令，不会写入文件或执行脚本。需要手动刷新时运行：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/build_learning_index.py"
python "$HOME/.agents/skills/memory-capture/scripts/render_dashboard.py"
```

每日 Review Digest 是 Markdown 查看入口：

```text
$HOME/.codex/learning-index.json
$HOME/.codex/daily-digests/YYYY/MM/DD/review-digest.md
$HOME/.codex/learning-inbox-summary.md
```

`learning-index.json` 是 Dashboard 和轻量每日 Digest 共用的数据层。Digest 会给候选标出建议归属和改写建议：全局偏好进 `USER.md`，项目事实进项目 `AGENTS.md`，复用流程保留为 skill candidate，已有技能改进进入 skill patch。

只有检测到候选时，才会写入候选文件：

```text
$HOME/.codex/memories/inbox/YYYY/MM/DD
$HOME/.codex/skill-candidates/inbox/YYYY/MM/DD
$HOME/.codex/skill-candidates/patches/YYYY/MM/DD
```

已晋升的全局记忆：

```text
$HOME/.codex/memories/USER.md
```

技能候选：

```text
$HOME/.codex/skill-candidates/inbox
```

技能补丁候选：

```text
$HOME/.codex/skill-candidates/patches
```

覆盖式维护报告：

```text
$HOME/.codex/latest-skill-candidate-security-scan.md
$HOME/.codex/latest-user-memory-budget.md
```

技能索引：

```text
$HOME/.codex/skills-index.md
```

## 晋升记忆

把一条确认过的候选写入 `USER.md`：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/promote_memory.py" \
  --text "这里写入确认后的记忆内容" \
  --approved
```

查看候选评分，不写入 `USER.md`：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/promote_candidates.py"
```

自动晋升安全、短小、重复出现的偏好候选：

```bash
python "$HOME/.agents/skills/memory-capture/scripts/promote_candidates.py" --auto-promote
```

## Windows 查看定时任务

```powershell
schtasks.exe /Query /TN CodexSelfImprovingLoopWatcher /V /FO LIST
```

手动触发一次：

```powershell
schtasks.exe /Run /TN CodexSelfImprovingLoopWatcher
```

删除定时任务：

```powershell
schtasks.exe /Delete /TN CodexSelfImprovingLoopWatcher /F
```
