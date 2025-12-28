# Fork Terminal Skill

A Claude Code skill that enables forking terminal sessions to run CLI commands or launch new agentic coding tools with conversation context.

## Features

- **New Terminal Windows**: Open fresh terminal instances on macOS (osascript) or Windows (PowerShell)
- **Raw CLI Commands**: Execute any CLI command (ffmpeg, curl, etc.) in new terminals
- **Agentic Tools**: Launch Gemini CLI, Claude Code, or Codex CLI with forked context
- **Conversation Forking**: Summarize current conversation and pass to new agent
- **Progressive Disclosure**: Uses cookbook pattern for context-aware instructions

## Installation

1. Copy the `fork-terminal` directory to your Claude Code skills location:
   ```bash
   cp -r .claude/skills/fork-terminal ~/.claude/skills/
   ```

2. Make the Python script executable:
   ```bash
   chmod +x ~/.claude/skills/fork-terminal/tools/fork_terminal.py
   ```

3. Ensure Astral UV is installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## Usage

### Fork with Raw CLI Command
```
fork terminal run ffmpeg -i video.mp4
```

### Fork with Agentic Tool (Fast Model)
```
fork terminal use claude code fast model to refactor this function
```

### Fork with Summary (Pass Conversation Context)
```
fork session codex cli summarize work done - understand this codebase and write tests
```

## Project Structure

```
.claude/skills/fork-terminal/
├── SKILL.md                          # Main skill definition
├── tools/
│   └── fork_terminal.py              # Terminal forking script
├── prompts/
│   └── fork-summary-user-prompt.md   # Template for forked conversations
└── cookbook/
    ├── cli-command.md                # Raw CLI execution guide
    ├── gemini-cli.md                 # Gemini CLI integration
    ├── codex-cli.md                  # Codex CLI integration
    └── claude-code.md                # Claude Code integration
```

## Configuration

Edit `SKILL.md` to enable/disable features:

```yaml
variables:
  enable_gemini_cli: true
  enable_codex_cli: true
  enable_claude_code: true
  enable_raw_cli_commands: true
```

## Model Selection

- **Fast**: Haiku (Claude), Flash (Gemini), Mini (Codex)
- **Base/Default**: Sonnet (Claude), Pro (Gemini), Standard (Codex)
- **Heavy**: Opus (Claude), Ultra (Gemini), Max (Codex)

## Examples

1. **Quick CLI task in new window:**
   ```
   fork terminal curl https://api.example.com/data
   ```

2. **Parallel agent work:**
   ```
   fork session gemini cli fast - summarize file1.md
   fork session codex cli fast - summarize file2.md
   fork session claude code fast - summarize file3.md
   ```

3. **Context-aware fork:**
   ```
   # After working with agent on feature...
   fork session claude code summarize work - now implement the tests
   ```

## Video Tutorial

Based on [RAW Agentic Coding: ZERO to Agent SKILL](https://www.youtube.com/watch?v=X2ciJedw2vU) by IndyDevDan

## License

MIT
