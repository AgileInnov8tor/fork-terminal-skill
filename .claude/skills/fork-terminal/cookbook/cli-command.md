# Raw CLI Command Execution

## Pattern

When forking a terminal to run a raw CLI command:

1. **Always run help first**: Before executing any CLI tool, run the `--help` command to understand its usage
2. **Preserve context**: Maintain the current working directory in the forked terminal
3. **Execute command**: Run the command in the new terminal window

## Steps

```bash
# 1. Understand the tool
<tool> --help

# 2. Fork terminal with command
python tools/fork_terminal.py "<full-command>"
```

## Examples

### Video Processing with FFmpeg
```bash
# First, check FFmpeg help
ffmpeg --help

# Then fork terminal to process video
python tools/fork_terminal.py "ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4"
```

### API Call with curl
```bash
# Check curl help
curl --help

# Fork terminal to make API call
python tools/fork_terminal.py "curl -X POST https://api.example.com/data -H 'Content-Type: application/json' -d '{\"key\":\"value\"}'"
```

### File Download with wget
```bash
# Check wget help
wget --help

# Fork terminal to download file
python tools/fork_terminal.py "wget https://example.com/large-file.zip"
```

## Best Practices

- Always quote commands properly to handle special characters
- Use absolute paths for file references when possible
- Consider using screen or tmux for long-running processes
- Redirect output to files for commands that produce lots of output

## Safety Considerations

- Validate commands before execution
- Avoid running destructive commands without user confirmation
- Be careful with commands that require sudo/admin privileges
- Check disk space for operations that create large files
