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

安装每天 12:00 执行的系统调度：

```bash
python install_watcher_schedule.py
```

Windows 下如果希望计划任务执行完成后终端窗口停留，方便查看本次摘要：

```bash
python install_watcher_schedule.py --pause-on-exit
```

## 查看结果

每日 Review Digest 是主要查看入口：

```text
$HOME/.codex/daily-digests/YYYY/MM/DD/review-digest.md
$HOME/.codex/learning-inbox-summary.md
```

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
