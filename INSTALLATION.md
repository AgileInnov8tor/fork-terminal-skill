# Installation Guide

## Prerequisites

### System Requirements
- **macOS**: 10.14 (Mojave) or later
- **Windows**: Windows 10 or later with PowerShell
- **Linux**: Any modern distribution with terminal emulator (gnome-terminal, konsole, or xterm)

### Required Software
- **Python 3.8+**: Required for fork_terminal.py script
- **Claude Code CLI** (optional): For Claude Code integration
  ```bash
  # Installation instructions at: https://github.com/anthropics/claude-code
  npm install -g @anthropics/claude-code
  ```
- **Gemini CLI** (optional): For Gemini integration
  ```bash
  pip install gemini-cli
  ```
- **Codex CLI** (optional): For Codex integration
  ```bash
  # Follow your Codex provider's installation instructions
  ```

## Installation Steps

### 1. Clone or Copy Project

```bash
# Navigate to your Claude Code skills directory
cd ~/.claude/skills/

# Copy the fork-terminal skill
cp -r /path/to/fork-terminal-skill ./fork-terminal
```

### 2. Make Scripts Executable

```bash
cd ~/.claude/skills/fork-terminal
chmod +x tools/fork_terminal.py
```

### 3. Configure Environment Variables

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Required API keys:
- **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com/
- **GOOGLE_API_KEY**: Get from https://makersuite.google.com/app/apikey
- **CODEX_API_KEY**: From your Codex CLI provider

### 4. Verify Installation

Test that the fork_terminal.py script works:

```bash
# Test with a simple command
python3 tools/fork_terminal.py "echo 'Fork terminal working!'"
```

You should see a new terminal window open with the message.

### 5. Enable Skill in Claude Code

The skill is automatically available once placed in `~/.claude/skills/fork-terminal/`.

Verify by asking Claude Code:
```
"List available skills"
```

## Platform-Specific Notes

### macOS
- Uses AppleScript via `osascript` to control Terminal.app
- Requires Terminal.app to be available (default on macOS)
- May prompt for accessibility permissions on first run

### Windows
- Uses PowerShell to launch new terminal windows
- Requires PowerShell 5.0+ (default on Windows 10+)
- May need to adjust execution policy:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Linux
- Attempts to use terminal emulators in order: gnome-terminal → konsole → xterm
- Install at least one supported terminal emulator:
  ```bash
  # Ubuntu/Debian
  sudo apt install gnome-terminal

  # Fedora
  sudo dnf install gnome-terminal

  # Arch
  sudo pacman -S gnome-terminal
  ```

## Troubleshooting

### "Command not found: claude"
Claude Code CLI is not installed or not in PATH. Install via:
```bash
npm install -g @anthropics/claude-code
```

### "No supported terminal emulator found" (Linux)
Install a supported terminal emulator:
```bash
sudo apt install gnome-terminal  # or konsole, or xterm
```

### "Permission denied" when running fork_terminal.py
Make the script executable:
```bash
chmod +x ~/.claude/skills/fork-terminal/tools/fork_terminal.py
```

### API key errors
Verify your .env file contains valid API keys:
```bash
cat ~/.claude/skills/fork-terminal/.env
```

### Terminal doesn't open in correct directory
The script uses `os.getcwd()` to capture the current directory. Ensure you're running from the intended working directory.

## Updating

To update the skill:

```bash
cd ~/.claude/skills/fork-terminal
git pull  # if using git
# or manually copy updated files
```

## Uninstallation

To remove the skill:

```bash
rm -rf ~/.claude/skills/fork-terminal
```

This will remove the skill from Claude Code's available skills.

## Getting Help

- Check the [README.md](README.md) for usage examples
- Review [cookbook files](.claude/skills/fork-terminal/cookbook/) for specific tool integration guides
- Report issues at: [project repository URL]
