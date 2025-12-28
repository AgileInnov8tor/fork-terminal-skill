# Claude Code Integration

## Overview

Fork terminal sessions to launch Claude Code CLI with conversation context.

## Prerequisites

- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- ANTHROPIC_API_KEY environment variable set
- Active internet connection

## Model Selection

| Tier | Model | Flag |
|------|-------|------|
| Fast | Claude Haiku | `--model haiku` |
| Base | Claude Sonnet | `--model sonnet` (default) |
| Heavy | Claude Opus | `--model opus` |

## Pattern

1. **Determine model tier** from user request (fast/base/heavy)
2. **Prepare initial prompt** (if specific task mentioned)
3. **Execute fork** with Claude Code command

## Command Reference

```bash
# Interactive mode (default)
claude

# With specific model
claude --model haiku
claude --model sonnet
claude --model opus

# Single prompt mode (non-interactive)
claude -p "Your question or task here"
claude --print "Explain this code"

# Resume previous session
claude -r
claude --resume

# Skip permission prompts (use with caution)
claude -d
claude --dangerously-skip-permissions

# Combine flags
claude --model haiku -p "Quick question"
claude --model opus -d  # Opus with auto-approve
```

## Steps

### Basic Fork (Interactive Mode)
```bash
# Fast model - quick tasks
python tools/fork_terminal.py "claude --model haiku"

# Base model (default) - standard development
python tools/fork_terminal.py "claude"

# Heavy model - complex analysis
python tools/fork_terminal.py "claude --model opus"
```

### Fork with Initial Prompt
```bash
# Pass a starting prompt to the new session
python tools/fork_terminal.py "claude -p 'Analyze the test coverage in this project'"

# For multi-word prompts, use proper quoting
python tools/fork_terminal.py "claude --model sonnet -p 'Refactor the authentication module'"
```

### Fork with YOLO Mode (Auto-approve)
```bash
# Use -d flag to skip permission prompts
# WARNING: Only use for trusted operations
python tools/fork_terminal.py "claude --model haiku -d"
```

## Example Invocations

### Quick Task (Fast Model)
```
User: fork session claude code fast - fix these linting errors
→ Opens Claude Haiku in new terminal for quick fixes

Command: python tools/fork_terminal.py "claude --model haiku"
```

### Standard Development (Base Model)
```
User: fork terminal use claude code to implement user authentication
→ Opens Claude Sonnet in new terminal

Command: python tools/fork_terminal.py "claude"
```

### Complex Refactor (Heavy Model)
```
User: fork session claude opus - refactor entire backend architecture
→ Opens Claude Opus for complex analysis

Command: python tools/fork_terminal.py "claude --model opus"
```

## Best Practices

- **Use Haiku** for quick fixes, simple refactors, and fast iterations
- **Use Sonnet** for standard development tasks (features, bug fixes, tests)
- **Use Opus** for complex analysis, architecture decisions, and critical code
- **Avoid -d flag** unless you fully trust the operation
- **Provide clear context** in your initial prompt when forking

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
→ python tools/fork_terminal.py "claude --model haiku"
```

### 2. Test-Driven Development
```
# Main session: write tests
# Forked session: implement code to pass tests
fork terminal claude sonnet - implement code for these test cases
→ python tools/fork_terminal.py "claude"
```

### 3. Quick Documentation
```
# Generate docs in parallel with fast model
fork session claude haiku - update README
→ python tools/fork_terminal.py "claude --model haiku"
```

### 4. Code Review
```
# Fork a session for detailed review with heavy model
fork terminal claude opus - review security implications
→ python tools/fork_terminal.py "claude --model opus"
```

### 5. Multi-File Refactoring
```
# Offload large refactoring task
fork session claude opus - refactor database layer to use repository pattern
→ python tools/fork_terminal.py "claude --model opus"
```

## Working Directory Context

Forked sessions automatically inherit the current working directory:

```bash
# Current directory is preserved
cd /path/to/project
fork terminal claude haiku - fix type errors in src/
# New terminal opens in /path/to/project with full codebase access
```

## Integration Examples

### With Git Workflow
```bash
# Review staged changes
fork terminal claude sonnet
# Then in the forked session: "Review git diff and suggest improvements"
```

### With Testing
```bash
# Run and fix tests
fork session claude haiku
# Then: "Run pytest and fix any failing tests"
```

### With Linting
```bash
# Fix linting issues quickly
fork terminal claude haiku
# Then: "Fix all ruff linting errors"
```

## Troubleshooting

### Claude Code not found
```bash
# Check if claude is installed
which claude

# Install if missing
npm install -g @anthropic-ai/claude-code
```

### API key not set
```bash
# Verify API key is available
echo $ANTHROPIC_API_KEY

# Set for current session
export ANTHROPIC_API_KEY="sk-ant-..."

# Or add to ~/.bashrc or ~/.zshrc for persistence
```

### Permission denied
```bash
# If you get permission errors, check file permissions
# or use -d flag for auto-approve (with caution)
claude -d
```
