# Quickstart

Codex Self-Improving Loop v3 是一个只面向本机的 SQLite + WebUI 自改进控制台。
安装后会在 `$HOME/.agents/codex-self-improving-loop` 保留一份运行副本，供定时任务、桌面快捷方式和 skills 稳定调用。
WebUI 按 `总览 / 审阅工作流 / 运维与历史` 三个工作区组织。Codex 可以提取、分析并提出候选建议，但所有晋升都必须人工确认，不做自动晋升。

```bash
python install.py
python "$HOME/.agents/codex-self-improving-loop/sil.py" doctor
python "$HOME/.agents/codex-self-improving-loop/sil.py" rebuild --backup
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open
```

日常审阅路径：

1. 在 `总览` 查看下一步建议、digest、优先审阅候选和失败运行。
2. 在 `审阅工作流` 核对候选证据、LLM 分析、建议文本和晋升 diff。
3. 只在 `人工审批操作台` 点击晋升按钮，并通过确认弹窗后才写入 `USER.md`、`AGENTS.md`、skill 或 skill patch。
4. 在 `运维与历史` 查看调度、Skill 健康、运行日志、审计、晋升历史和回滚预览。

运行时文件统一位于：

```text
$HOME/.codex/self-improving-loop/
```

每日扫描：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" scan --once
```

安装每天 03:00 的扫描入口：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" schedule install
```

Windows 会安装计划任务，macOS 会安装 LaunchAgent，Linux 会安装 `systemd --user` timer。

安装桌面一键启动入口：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" shortcut install
```
