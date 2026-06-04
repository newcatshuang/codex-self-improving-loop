# Quickstart

Codex Self-Improving Loop v2 是一个只面向本机的 SQLite + WebUI 自改进控制台。

```bash
python install.py
python "$HOME/.agents/codex-self-improving-loop/sil.py" doctor
python "$HOME/.agents/codex-self-improving-loop/sil.py" rebuild --backup
python "$HOME/.agents/codex-self-improving-loop/sil.py" serve --open
```

运行时文件统一位于：

```text
$HOME/.codex/self-improving-loop/
```

每日扫描：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" scan --once
```

安装每天 12:00 的扫描入口：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" schedule install
```

安装桌面一键启动入口：

```bash
python "$HOME/.agents/codex-self-improving-loop/sil.py" shortcut install
```
