# Contributing to Fork Terminal Skill

Thank you for your interest in contributing to the Fork Terminal Skill project!

## How to Contribute

### Reporting Issues

If you encounter bugs or have feature requests:

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear description of the problem or feature
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your platform (macOS, Windows, Linux)
   - Python version and relevant CLI tool versions

### Contributing Code

1. **Fork the repository** (if applicable)
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation as needed
4. **Test your changes**:
   - Test on your platform (macOS/Windows/Linux)
   - Verify the skill works with Claude Code
   - Test cookbook examples if modified
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: description of feature"
   ```
6. **Submit a pull request**

## Code Style Guidelines

### Python (fork_terminal.py)

- **PEP 8 compliance**: Follow Python style guidelines
- **Type hints**: Use type annotations where applicable
- **Docstrings**: Include docstrings for functions
- **Error handling**: Provide clear error messages
- **Cross-platform**: Test on multiple platforms when possible

Example:
```python
def fork_terminal(command: str) -> None:
    """
    Fork a new terminal window and execute the given command.

    Args:
        command: The shell command to execute in the new terminal

    Raises:
        RuntimeError: If the platform is unsupported or terminal not found
    """
```

### Markdown Documentation

- **Clear headings**: Use hierarchical structure (# → ## → ###)
- **Code blocks**: Include language identifiers
- **Examples**: Provide practical, tested examples
- **Links**: Use relative links for internal references
- **Consistency**: Follow existing format in cookbook files

### YAML/Handlebars (SKILL.md)

- **Indentation**: Use 2 spaces for YAML
- **Variables**: Keep variable names descriptive
- **Comments**: Explain non-obvious logic
- **Templates**: Test Handlebars conditionals

## Adding New Features

### New CLI Tool Integration

To add support for a new CLI tool:

1. **Create cookbook file**: `.claude/skills/fork-terminal/cookbook/your-tool-cli.md`
2. **Follow existing format**:
   - Overview
   - Prerequisites
   - Model Selection (if applicable)
   - Pattern
   - Steps
   - Example Invocations
   - Command Options
   - Best Practices
3. **Add variable to SKILL.md**:
   ```yaml
   enable_your_tool_cli: true
   ```
4. **Add conditional include**:
   ```handlebars
   {{#if enable_your_tool_cli}}
   - For Your Tool CLI: Include @cookbook/your-tool-cli.md
   {{/if}}
   ```
5. **Update README.md**: Add to "Supported Tools" section
6. **Test thoroughly**: Ensure examples work

### Platform Support

When adding platform-specific features:

- Test on the target platform
- Provide fallback behavior when possible
- Document platform requirements
- Update INSTALLATION.md with platform notes

## Testing

### Manual Testing Checklist

Before submitting changes:

- [ ] Script executes without errors
- [ ] New terminal window opens correctly
- [ ] Working directory is preserved
- [ ] Cookbook examples work as documented
- [ ] Error messages are clear and helpful
- [ ] Documentation is accurate

### Platform Testing

If possible, test on:
- [ ] macOS (Terminal.app via osascript)
- [ ] Windows (PowerShell)
- [ ] Linux (gnome-terminal/konsole/xterm)

## Documentation Updates

When changing functionality:

1. Update **README.md** if user-facing
2. Update **INSTALLATION.md** for setup changes
3. Update **cookbook files** for new patterns
4. Update **SKILL.md** for new variables or instructions
5. Add **examples** to demonstrate new features

## Commit Message Format

Use clear, descriptive commit messages:

```
Add feature: Support for new CLI tool X

- Create cookbook/cli-tool-x.md
- Add enable_cli_tool_x variable
- Update README.md with examples
- Test on macOS and Linux
```

## Code Review Process

Pull requests will be reviewed for:

- **Functionality**: Does it work as intended?
- **Code quality**: Is it clean, readable, maintainable?
- **Documentation**: Is it well-documented?
- **Testing**: Has it been tested?
- **Compatibility**: Does it work across platforms?

## Questions?

If you have questions about contributing:

- Review existing code and documentation
- Check the [README.md](README.md) and [INSTALLATION.md](INSTALLATION.md)
- Open an issue for clarification
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (specify license here).

## Recognition

Contributors will be acknowledged in:
- Project README.md
- Release notes for significant contributions

Thank you for helping improve the Fork Terminal Skill!
