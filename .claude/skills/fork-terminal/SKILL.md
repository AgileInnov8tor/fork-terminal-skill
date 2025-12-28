---
name: fork-terminal
description: Fork terminal sessions to run CLI commands or launch agentic coding tools with conversation context
version: 1.1.0
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

Open new terminal instances to run CLI commands or launch agentic coding tools (Claude Code, Gemini CLI, Codex CLI) with optional conversation context.

## Purpose

This skill allows you to:
1. **Fork terminal with raw CLI commands**: Open a new terminal window and execute any command (ffmpeg, curl, etc.)
2. **Fork with agentic coding tools**: Launch Claude Code, Gemini CLI, or Codex CLI in a new terminal
3. **Fork with conversation summary**: Pass summarized conversation context to the new agent

## Instructions

When the user requests to fork a terminal session or run commands in a new window:

### Step 1: Determine the Fork Type

Based on the user's request, identify:
- **Raw CLI command**: User wants to run a specific CLI tool (e.g., "fork terminal run ffmpeg -i video.mp4")
- **Agentic tool**: User wants to launch an AI coding assistant (e.g., "fork session use claude code to refactor")
- **With summary**: User mentions "summarize" to pass conversation context (e.g., "fork session summarize work done")

### Step 2: Select the Appropriate Guide

Based on the fork type, read the relevant cookbook file:

| Request Type | Cookbook File | Example Trigger |
|-------------|---------------|-----------------|
| Raw CLI command | `@cookbook/cli-command.md` | "fork terminal curl...", "fork terminal npm run..." |
| Claude Code | `@cookbook/claude-code.md` | "fork claude", "fork claude code", "fork claude haiku" |
| Gemini CLI | `@cookbook/gemini-cli.md` | "fork gemini", "fork gemini flash" |
| Codex CLI | `@cookbook/codex-cli.md` | "fork codex", "fork codex cli" |

### Step 3: Detect Model Tier (for agentic tools)

If the user specifies a model tier, map it:

| User Says | Claude Code | Gemini CLI | Codex CLI |
|-----------|-------------|------------|-----------|
| "fast", "quick", "haiku", "flash", "mini" | `--model haiku` | `-m flash` | `--tier mini` |
| "base", "default", "sonnet", "pro", "standard" | `--model sonnet` | `-m pro` | `--tier standard` |
| "heavy", "opus", "ultra", "max" | `--model opus` | `-m ultra` | `--tier max` |

### Step 4: Generate Fork Summary (if requested)

If the user mentions "summarize" or "with context":
1. Use the template from `@prompts/fork-summary-user-prompt.md`
2. Fill in: conversation history, user request summary, key decisions, relevant files
3. Save to a temporary file or include inline

### Step 5: Execute the Fork

Use the fork_terminal.py tool:
```bash
python tools/fork_terminal.py [OPTIONS] "<command>"
```

**Options:**
- `--terminal <name>`: Specify terminal (terminal, iterm, warp, kitty, etc.)
- `--timeout <secs>`: Timeout for fork operation
- `--json`: Output result as JSON
- `--no-validate`: Skip tool availability check

## Examples

### Raw CLI Command
```
User: fork terminal curl https://api.example.com/data
→ python tools/fork_terminal.py "curl https://api.example.com/data"
```

### Agentic Tool (Fast Model)
```
User: fork terminal use claude code fast model to fix linting
→ python tools/fork_terminal.py "claude --model haiku"
```

### Agentic Tool (Heavy Model)
```
User: fork session gemini ultra to analyze architecture
→ python tools/fork_terminal.py "gemini -m ultra"
```

### With Conversation Summary
```
User: fork session claude opus summarize work done
→ Generate summary using template
→ python tools/fork_terminal.py "claude --model opus"
→ Paste summary as initial context
```

## Model Selection Reference

| Tier | Claude | Gemini | Codex |
|------|--------|--------|-------|
| Fast | Haiku | Flash | Mini |
| Base | Sonnet | Pro | Standard |
| Heavy | Opus | Ultra | Max |

## Safety Guidelines

- Always validate tool availability before launching
- Preserve current working directory context
- Use YOLO/auto-approve modes (--danger, -d, -y) only when explicitly requested
- Check for required authentication:
  - Claude Code: ANTHROPIC_API_KEY
  - Gemini CLI: Google account (see gemini-cli.md)
  - Codex CLI: CODEX_API_KEY (see codex-cli.md)

## Tool Documentation

> **Note**: Gemini CLI and Codex CLI documentation is based on publicly available information and may not reflect the latest versions. Verify commands with `--help` before use.

For detailed command references, see the cookbook files:
- `cookbook/cli-command.md` - Raw CLI execution patterns
- `cookbook/claude-code.md` - Claude Code CLI reference (verified)
- `cookbook/gemini-cli.md` - Gemini CLI reference (community documentation)
- `cookbook/codex-cli.md` - Codex CLI reference (community documentation)
