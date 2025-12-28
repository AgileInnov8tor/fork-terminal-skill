# Codex CLI Integration

## Overview

Fork terminal sessions to launch Codex CLI (or similar AI coding assistant) with conversation context.

## Prerequisites

- Codex CLI installed
- CODEX_API_KEY or appropriate credentials configured
- Active internet connection

## Model Selection

| Tier | Model | Flag |
|------|-------|------|
| Fast | Codex Mini | `--model mini` |
| Base | Codex Standard | `--model standard` (default) |
| Heavy | Codex Max | `--model max` |

## Pattern

1. **Check Codex CLI help** (if not already known)
2. **Determine model tier** from user request (fast/base/heavy)
3. **Prepare fork summary** (if "summarize" keyword present)
4. **Execute fork** with Codex CLI command

## Steps

### Without Summary
```bash
# Fast model
python tools/fork_terminal.py "codex --model mini"

# Base model (default)
python tools/fork_terminal.py "codex"

# Heavy model
python tools/fork_terminal.py "codex --model max"
```

### With Summary
```bash
# 1. Generate summary using fork-summary-user-prompt.md template
# 2. Save summary to temp file
# 3. Fork with summary as initial context

python tools/fork_terminal.py "codex --model standard --context summary.md"
```

## Example Invocations

### Quick Refactor (Fast Model)
```
User: fork session codex cli fast - refactor this function for readability
→ Opens Codex Mini in new terminal with function context
```

### Test Generation (Base Model)
```
User: fork terminal use codex to write comprehensive tests
→ Opens Codex Standard in new terminal
```

### Architecture Analysis (Heavy Model)
```
User: fork session codex max summarize work - analyze the entire codebase architecture
→ Opens Codex Max with full conversation summary
```

## Command Options

```bash
# Interactive mode
codex --model mini

# Single task mode
codex task "Write tests for authentication.py" --model standard

# File-specific operation
codex refactor src/app.py --model mini

# Codebase analysis
codex analyze . --model max

# Code review
codex review --files src/**/*.py --model standard
```

## Best Practices

- Use Mini for quick refactors and simple tasks
- Use Standard for test generation and standard development
- Use Max for codebase-wide analysis and complex operations
- Always provide specific file paths or clear scope
- Use --context flag to pass conversation summaries
- Consider using --output flag to save generated code

## Configuration

Ensure API credentials are configured:
```bash
# Check configuration
codex config show

# Set API key
codex config set api_key "your-api-key-here"

# Set default model
codex config set default_model standard
```

## Common Use Cases

### 1. Parallel Test Writing
```
# Main session: implement feature
# Forked session: write tests for implemented code
fork session codex mini - write unit tests for UserAuth class
```

### 2. Code Review
```
# Fork a session to review changes
fork terminal codex standard - review changes in auth system
```

### 3. Documentation Generation
```
# Generate docs in parallel
fork session codex mini - generate API documentation for all endpoints
```

### 4. Refactoring Large Files
```
# Offload refactoring to forked session
fork terminal codex max summarize work - refactor database.py following current patterns
```
