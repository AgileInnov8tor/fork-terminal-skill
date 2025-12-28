# Gemini CLI Integration

> **⚠️ Community Documentation**: This guide is based on publicly available information about Gemini CLI. Command syntax and features may have changed. Always verify with `gemini --help` before use.

## Overview

Fork terminal sessions to launch Google Gemini CLI with conversation context.
Uses Google account authentication (subscription-based), not API keys.

## Prerequisites

- Gemini CLI installed (check Google's official documentation for installation)
- Logged in via `gemini` (will prompt for Google account auth on first run)
- Active internet connection

> **Note**: Verify installation and authentication requirements with the official Gemini CLI documentation, as these may change.

## Authentication

Gemini CLI uses your Google account subscription, not API keys:

```bash
# First run will prompt for Google account login
gemini

# Or explicitly trigger login if needed
# (authentication handled automatically)
```

## Model Selection

| Tier | Model | Flag |
|------|-------|------|
| Fast | Gemini Flash | `-m flash` or `--model flash` |
| Base | Gemini Pro | `-m pro` or default |
| Heavy | Gemini Ultra | `-m ultra` or `--model ultra` |

## Command Syntax (from --help)

```bash
# Interactive mode (default)
gemini [query..]

# With specific model
gemini -m flash "your query here"

# Interactive after initial prompt
gemini -i "start with this context"

# YOLO mode (auto-approve all actions)
gemini -y "task description"

# Resume previous session
gemini -r latest
gemini --resume 5

# With sandbox
gemini -s "sandboxed task"
```

## Pattern

1. **Determine model tier** from user request (fast/base/heavy)
2. **Prepare fork summary** (if "summarize" keyword present)
3. **Execute fork** with Gemini CLI command

## Steps

### Interactive Mode (stays open for chat)
```bash
# Fast model - interactive
python tools/fork_terminal.py "gemini -m flash"

# Base model - interactive
python tools/fork_terminal.py "gemini"

# Heavy model - interactive
python tools/fork_terminal.py "gemini -m ultra"

# Interactive with initial context (stays open after first response)
python tools/fork_terminal.py "gemini -i 'analyze this codebase'"
```

### One-Shot Mode (runs query and exits)
```bash
# Quick question (exits after response)
python tools/fork_terminal.py "gemini -m flash 'what is 2+2'"
```

### With Summary
```bash
# 1. Generate summary using fork-summary-user-prompt.md template
# 2. Pass summary as initial prompt via -i flag (interactive after prompt)

python tools/fork_terminal.py "gemini -i 'Context from previous session: [summary]'"
```

### YOLO Mode (Auto-approve)
```bash
# Auto-approve all tool actions
python tools/fork_terminal.py "gemini -y 'refactor the auth module'"

# Or with approval-mode flag
python tools/fork_terminal.py "gemini --approval-mode yolo 'task'"
```

## Example Invocations

### Quick Task (Fast Model)
```
User: fork session gemini cli fast - summarize this file
→ Opens Gemini Flash in new terminal with file context
→ Command: gemini -m flash "summarize the current file"
```

### Code Review (Base Model)
```
User: fork terminal use gemini cli to review the authentication code
→ Opens Gemini Pro in new terminal for code review
→ Command: gemini "review the authentication code"
```

### Complex Analysis (Heavy Model)
```
User: fork session gemini ultra summarize work done - now write comprehensive tests
→ Opens Gemini Ultra with conversation summary
→ Command: gemini -m ultra -i "[summary context]"
```

### Autonomous Task (YOLO Mode)
```
User: fork gemini yolo mode to fix all linting errors
→ Opens Gemini with auto-approval enabled
→ Command: gemini -y "fix all linting errors in this project"
```

## Advanced Options

```bash
# Resume latest session
gemini -r latest

# Resume specific session (by index)
gemini --resume 5

# List available sessions
gemini --list-sessions

# Include additional directories
gemini --include-directories ../shared,../common

# Run with specific extensions
gemini -e lint,test "run quality checks"

# List available extensions
gemini -l
```

## Best Practices

- Use Flash (`-m flash`) for quick tasks (summaries, simple questions)
- Use Pro (default) for standard coding tasks (refactoring, debugging)
- Use Ultra (`-m ultra`) for complex analysis (architecture reviews)
- Use `-i` flag to start with context then continue interactively
- Use `-y` (YOLO mode) cautiously, only for trusted automated tasks
- Use `--resume latest` to continue previous work
- Pass file paths directly in the query for context

## Subscription vs API

This integration uses **Google account authentication** (subscription-based):
- No API key management required
- Uses your Google Cloud/Gemini subscription
- Automatic token/billing through your Google account
- Login state persists across sessions
