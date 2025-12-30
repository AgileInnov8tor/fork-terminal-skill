---
name: fork-terminal
description: Fork terminal sessions to run CLI commands or launch agentic coding tools with conversation context
version: 1.0.0
author: IndyDevDan
triggers:
  - fork terminal
  - fork session
  - new terminal
  - spawn terminal
  - run in new window
  - parallel agent
---

# Fork Terminal Skill

Open new terminal instances to run CLI commands or launch agentic coding tools (Gemini CLI, Claude Code, Codex CLI) with optional conversation context.

## Variables

```yaml
variables:
  enable_gemini_cli: true
  enable_codex_cli: true
  enable_claude_code: true
  enable_raw_cli_commands: true
```

## Purpose

This skill allows you to:
1. **Fork terminal with raw CLI commands**: Open a new terminal window and execute any command (ffmpeg, curl, etc.)
2. **Fork with agentic coding tools**: Launch Gemini CLI, Claude Code, or Codex CLI in a new terminal
3. **Fork with conversation summary**: Pass summarized conversation context to the new agent

## Instructions

When the user requests to fork a terminal session or run commands in a new window:

1. **Determine the fork type** based on user request:
   - Raw CLI command (e.g., "fork terminal run ffmpeg -i video.mp4")
   - Agentic tool (e.g., "fork session use claude code to refactor")
   - With summary (e.g., "fork session codex cli summarize work done")

2. **Load appropriate cookbook guide**:
   {{#if enable_raw_cli_commands}}
   - For raw CLI: Include @cookbook/cli-command.md
   {{/if}}
   {{#if enable_gemini_cli}}
   - For Gemini CLI: Include @cookbook/gemini-cli.md
   {{/if}}
   {{#if enable_codex_cli}}
   - For Codex CLI: Include @cookbook/codex-cli.md
   {{/if}}
   {{#if enable_claude_code}}
   - For Claude Code: Include @cookbook/claude-code.md
   {{/if}}

3. **Detect model tier** (if applicable):
   - Fast: Haiku (Claude), Flash (Gemini), Mini (Codex)
   - Base/Default: Sonnet (Claude), Pro (Gemini), Standard (Codex)
   - Heavy: Opus (Claude), Ultra (Gemini), Max (Codex)

4. **Generate fork summary** (if "summarize" keyword present):
   - Use @prompts/fork-summary-user-prompt.md template
   - Summarize current conversation history
   - Include relevant context for new agent

5. **Execute fork** using tools/fork_terminal.py:
   - Preserve current working directory
   - Open new terminal window (osascript on macOS, PowerShell on Windows)
   - Execute command or launch tool

## Examples

### Raw CLI Command
```
User: fork terminal curl https://api.example.com/data
→ Opens new terminal, executes curl command
```

### Agentic Tool (Fast Model)
```
User: fork terminal use claude code fast model to refactor this function
→ Opens new terminal, launches Claude Code with Haiku model
```

### With Conversation Summary
```
User: fork session codex cli summarize work done - understand this codebase and write tests
→ Summarizes conversation, opens terminal, launches Codex CLI with context
```

## Model Selection

| Tier | Claude | Gemini | Codex |
|------|--------|--------|-------|
| Fast | Haiku | Flash | Mini |
| Base | Sonnet | Pro | Standard |
| Heavy | Opus | Ultra | Max |

## Cookbook Routing

The skill uses progressive disclosure to load only relevant documentation:

- `@cookbook/cli-command.md` - Raw CLI execution pattern
- `@cookbook/gemini-cli.md` - Gemini CLI integration
- `@cookbook/codex-cli.md` - Codex CLI integration
- `@cookbook/claude-code.md` - Claude Code integration

## Shell Alias Expansion

The fork_terminal.py script automatically expands common shell aliases:

- **`claude` command**: Expands to full path with plugin directory
  - From: `claude --model haiku`
  - To: `~/.claude/local/claude --plugin-dir ~/.claude/plugins/claude-code-toolkit --model haiku`

This ensures commands work correctly in forked terminal sessions where shell aliases may not be loaded.

## Safety

- Always run `--help` command first to understand tool usage
- Preserve current working directory context
- Use YOLO mode (--danger, -y) only when explicitly requested
- Validate authentication before launching agentic tools:
  - Gemini CLI: Uses Google account subscription (no API key needed)
  - Claude Code: Uses ANTHROPIC_API_KEY
  - Codex CLI: Uses CODEX_API_KEY (if applicable)
