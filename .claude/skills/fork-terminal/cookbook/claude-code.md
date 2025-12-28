# Claude Code Integration

## Overview

Fork terminal sessions to launch Claude Code CLI with conversation context.

## Prerequisites

- Claude Code CLI installed
- ANTHROPIC_API_KEY environment variable set
- Active internet connection

## Model Selection

| Tier | Model | Flag |
|------|-------|------|
| Fast | Claude Haiku | `--model haiku` |
| Base | Claude Sonnet | `--model sonnet` (default) |
| Heavy | Claude Opus | `--model opus` |

## Pattern

1. **Check Claude Code help** (if not already known)
2. **Determine model tier** from user request (fast/base/heavy)
3. **Prepare fork summary** (if "summarize" keyword present)
4. **Execute fork** with Claude Code command

## Steps

### Without Summary
```bash
# Fast model
python tools/fork_terminal.py "claude --model haiku"

# Base model (default)
python tools/fork_terminal.py "claude"

# Heavy model
python tools/fork_terminal.py "claude --model opus"
```

### With Summary
```bash
# 1. Generate summary using fork-summary-user-prompt.md template
# 2. Save summary to temp file or pass inline
# 3. Fork with summary as initial context

python tools/fork_terminal.py "claude --model sonnet --context-file summary.md"
```

## Example Invocations

### Quick Task (Fast Model)
```
User: fork session claude code fast - fix these linting errors
→ Opens Claude Haiku in new terminal for quick fixes
```

### Standard Development (Base Model)
```
User: fork terminal use claude code to implement user authentication
→ Opens Claude Sonnet in new terminal
```

### Complex Refactor (Heavy Model)
```
User: fork session claude opus summarize work done - refactor entire backend architecture
→ Opens Claude Opus with conversation summary
```

## Command Options

```bash
# Interactive mode
claude --model haiku

# Single prompt mode
claude prompt "Your question here" --model sonnet

# File-specific operation
claude edit app.py "Add error handling" --model haiku

# Code generation
claude generate "Create REST API endpoints" --model sonnet

# Code review
claude review src/ --model opus

# YOLO mode (skip confirmations)
claude --danger --model haiku
```

## Best Practices

- Use Haiku for quick fixes, simple refactors, and fast iterations
- Use Sonnet for standard development tasks (features, bug fixes, tests)
- Use Opus for complex analysis, architecture decisions, and critical code
- Always provide specific file paths or clear scope
- Use --context-file to pass conversation summaries
- Consider --danger flag only for trusted, non-critical operations

## API Key Management

Ensure ANTHROPIC_API_KEY is set:
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# Set API key (add to .env or shell profile)
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Common Use Cases

### 1. Parallel Feature Development
```
# Main session: work on feature A
# Forked session: work on feature B
fork session claude haiku - implement password reset feature
```

### 2. Test-Driven Development
```
# Main session: write tests
# Forked session: implement code to pass tests
fork terminal claude sonnet - implement code for these test cases
```

### 3. Documentation
```
# Generate docs in parallel
fork session claude haiku - update README with new API endpoints
```

### 4. Code Review
```
# Fork a session for detailed review
fork terminal claude opus summarize work - review security implications of authentication changes
```

### 5. Multi-File Refactoring
```
# Offload large refactoring task
fork session claude opus - refactor database layer to use repository pattern
```

## Working Directory Context

Claude Code automatically uses the current working directory, so forked sessions will have the same codebase context:

```bash
# Current directory is preserved
cd /path/to/project
fork terminal claude haiku - fix type errors in src/
# New terminal opens in /path/to/project
```

## Integration with Other Tools

### With Git
```bash
fork terminal claude sonnet - review git diff and suggest improvements
```

### With pytest
```bash
fork session claude haiku - run pytest and fix failing tests
```

### With linters
```bash
fork terminal claude haiku - fix all ruff linting errors
```
