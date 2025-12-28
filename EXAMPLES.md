# Usage Examples

Practical examples demonstrating how to use the fork_terminal skill in various scenarios.

## Basic Examples

### 1. Fork Session for Quick Task

```
User: "fork session claude code fast - fix these linting errors"
```

**What happens**:
- Claude detects "fast" keyword → selects Haiku model
- Runs: `python tools/fork_terminal.py "claude --model haiku"`
- New terminal opens with Claude Haiku ready for quick fixes

### 2. Fork with Conversation Summary

```
User: "fork session claude opus summarize work - refactor entire backend architecture"
```

**What happens**:
- Claude detects "summarize" keyword → prepares conversation summary
- Uses fork-summary-user-prompt.md template
- Fills in: conversation_history, key_decisions, relevant_files, next_steps
- Saves summary to temp file
- Runs: `python tools/fork_terminal.py "claude --model opus --context-file summary.md"`
- New terminal opens with Claude Opus + full context

### 3. Raw CLI Command Execution

```
User: "fork terminal to run ffmpeg video conversion"
```

**Claude's workflow**:
1. Runs: `ffmpeg --help` to understand options
2. Asks user for specific conversion parameters
3. Runs: `python tools/fork_terminal.py "ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4"`
4. New terminal shows ffmpeg progress

## Real-World Scenarios

### Parallel Feature Development

**Scenario**: You're working on Feature A, but need to start Feature B without losing context.

```
# Main session: Working on authentication
User: "I need to continue work on the password reset feature in parallel"

# Claude response
"I'll fork a new session with Claude Code to work on password reset while keeping this session focused on authentication."

# Executed command
python tools/fork_terminal.py "claude --model sonnet"
```

**Result**: Two independent development sessions running simultaneously.

### Test-Driven Development

**Scenario**: Write tests in one session, implement code in another.

```
# Session 1: Writing tests
User: "fork session for implementing the code to pass these tests"

# Claude forks with test context
python tools/fork_terminal.py "claude --model sonnet --context-file test-requirements.md"
```

**Result**: Original session continues writing tests, forked session implements code.

### Code Review with Context

**Scenario**: Review changes with full understanding of previous work.

```
User: "fork session claude opus summarize work - review security implications of authentication changes"
```

**Claude's actions**:
1. Generates summary including:
   - Changes made to authentication system
   - Security decisions
   - Relevant files modified
   - Next review steps
2. Forks Claude Opus with summary
3. Opus reviews with full context

### Multi-File Refactoring

**Scenario**: Large refactoring task that needs deep focus.

```
User: "fork session claude opus - refactor database layer to use repository pattern"
```

**Result**: New session dedicated to refactoring, preserving main session for other work.

## CLI Tool Integration Examples

### Gemini CLI Examples

#### Quick File Analysis

```
User: "fork gemini fast - summarize this config file"

# Executed
python tools/fork_terminal.py "gemini chat --model flash"
```

#### Code Architecture Review

```
User: "fork terminal gemini pro to review the authentication code"

# Executed
python tools/fork_terminal.py "gemini chat --model pro"
```

#### Comprehensive Analysis

```
User: "fork session gemini ultra summarize - analyze entire codebase architecture"

# Claude prepares summary, then executes
python tools/fork_terminal.py "gemini chat --model ultra --context summary.md"
```

### Codex CLI Examples

#### Function Refactoring

```
User: "fork session codex cli fast - refactor this function for readability"

# Executed
python tools/fork_terminal.py "codex --model mini"
```

#### Test Generation

```
User: "fork terminal use codex to write comprehensive tests"

# Executed
python tools/fork_terminal.py "codex --model standard"
```

#### Codebase Analysis

```
User: "fork session codex max summarize work - analyze the entire codebase architecture"

# Executed with summary context
python tools/fork_terminal.py "codex --model max --context summary.md"
```

### Raw CLI Examples

#### Long-Running Video Processing

```
User: "fork terminal to run ffmpeg video conversion in background"

# Claude workflow
1. Checks: ffmpeg --help
2. Asks for parameters
3. Executes: python tools/fork_terminal.py "ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4"
```

#### Parallel API Testing

```
User: "fork session to test API endpoints with curl"

# Executed
python tools/fork_terminal.py "curl -X POST https://api.example.com/test -H 'Content-Type: application/json' -d '{\"key\":\"value\"}'"
```

#### Large File Download

```
User: "fork terminal for downloading dataset with wget"

# Executed
python tools/fork_terminal.py "wget https://example.com/large-dataset.zip"
```

## Advanced Patterns

### Chained Forking

Fork multiple sessions for different aspects of a project:

```
# Session 1: Main development
User: "fork session for writing tests"
# Fork Test Session

User (in Test Session): "fork another session for documentation"
# Fork Documentation Session

# Result: 3 parallel sessions
- Main: Core development
- Test: Test writing
- Docs: Documentation
```

### Context Preservation

Using summaries to maintain context across sessions:

```
# After 1 hour of work
User: "fork session claude sonnet summarize all work done - implement user authentication"

# Claude's summary includes
- Conversation history (condensed)
- Decisions: Using JWT tokens, bcrypt for passwords
- Relevant files: auth.py, user.model.py, auth.routes.py
- Key decisions: Session expiry 24h, refresh tokens
- Next steps: Implement email verification
```

### Workflow Integration

#### With Git

```
User: "fork terminal to review git diff and suggest improvements"

# Executed
python tools/fork_terminal.py "claude --model sonnet"
# In forked session: "Review `git diff` output and suggest improvements"
```

#### With pytest

```
User: "fork session to run pytest and fix failing tests"

# Executed
python tools/fork_terminal.py "claude --model haiku"
# In forked session: "Run `pytest -v` and fix failures"
```

#### With Linters

```
User: "fork terminal to fix all ruff linting errors"

# Executed
python tools/fork_terminal.py "claude --model haiku"
# In forked session: "Run `ruff check .` and fix all errors"
```

## Tips for Effective Forking

### When to Fork

✅ **Good scenarios for forking**:
- Parallel feature development
- Long-running tasks (video processing, large downloads)
- Maintaining context while starting new task
- Code review with full context
- Test writing while implementing

❌ **When not to fork**:
- Simple, quick tasks (can handle in main session)
- When you need frequent back-and-forth (stay in main session)
- Very short commands (run directly with Bash)

### Model Selection Guide

| Task Complexity | Recommended Model | Example |
|----------------|------------------|---------|
| Quick fixes, simple refactors | Fast (Haiku/Flash/Mini) | Fix typo, simple function |
| Standard development | Base (Sonnet/Pro/Standard) | Feature implementation, bug fixes |
| Complex analysis, architecture | Heavy (Opus/Ultra/Max) | System design, security review |

### Summary Best Practices

**When to include summary**:
- Complex multi-step work completed
- Important decisions made
- Multiple files modified
- Context crucial for next steps

**What to include in summary**:
- Key decisions and rationale
- Files modified
- Patterns established
- Next steps defined
- Any blockers or considerations

## Troubleshooting Examples

### Terminal Doesn't Open

```bash
# Test fork_terminal.py directly
python3 ~/.claude/skills/fork-terminal/tools/fork_terminal.py "echo 'test'"

# If error, check platform support
python3 -c "import platform; print(platform.system())"
```

### Wrong Directory in Forked Terminal

The script captures `os.getcwd()` when executed. Ensure you're in the correct directory:

```bash
# Check current directory before forking
pwd

# Fork will open in this directory
python tools/fork_terminal.py "claude"
```

### API Key Errors

```bash
# Verify API keys are set
cat ~/.claude/skills/fork-terminal/.env

# Or check environment
echo $ANTHROPIC_API_KEY
echo $GOOGLE_API_KEY
```

## More Examples

For tool-specific examples, see:
- [Claude Code Examples](/.claude/skills/fork-terminal/cookbook/claude-code.md#example-invocations)
- [Gemini CLI Examples](/.claude/skills/fork-terminal/cookbook/gemini-cli.md#example-invocations)
- [Codex CLI Examples](/.claude/skills/fork-terminal/cookbook/codex-cli.md#example-invocations)
- [Raw CLI Examples](/.claude/skills/fork-terminal/cookbook/cli-command.md#examples)
