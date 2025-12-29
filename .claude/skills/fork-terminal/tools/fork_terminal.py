#!/usr/bin/env python3
"""
Fork Terminal - Open new terminal instances to run CLI commands or agentic tools

Usage:
    python fork_terminal.py <command>
    python fork_terminal.py --terminal warp <command>
    python fork_terminal.py --terminal terminal <command>

Environment Variables:
    FORK_TERMINAL_APP: Preferred terminal app (warp, terminal, iterm, kitty)

Examples:
    fork_terminal.py "curl https://api.example.com"
    fork_terminal.py "gemini -m flash"
    fork_terminal.py --terminal warp "claude --model haiku"
"""

import subprocess
import sys
import os
import platform
import shutil


def get_preferred_terminal() -> str:
    """Get the preferred terminal from environment or detect available."""
    # Check environment variable first
    env_terminal = os.environ.get("FORK_TERMINAL_APP", "").lower()
    if env_terminal:
        return env_terminal

    # Default to Terminal.app on macOS (most reliable with AppleScript)
    # Warp and iTerm2 have AppleScript compatibility issues
    return "terminal"


def expand_aliases(command: str) -> str:
    """Expand shell aliases in the command."""
    # Expand 'claude' alias to full path
    if command.startswith("claude ") or command == "claude":
        home = os.path.expanduser("~")
        claude_path = f"{home}/.claude/local/claude --plugin-dir {home}/.claude/plugins/claude-code-toolkit"
        command = command.replace("claude", claude_path, 1)
    return command


def fork_terminal(command: str, terminal: str = None) -> None:
    """
    Fork a new terminal window and execute the given command.

    Args:
        command: The command to execute in the new terminal
        terminal: Preferred terminal app (warp, terminal, iterm, kitty)
    """
    current_dir = os.getcwd()
    system = platform.system()

    if terminal is None:
        terminal = get_preferred_terminal()

    if system == "Darwin":  # macOS
        if terminal == "warp":
            # Warp terminal - use clipboard paste approach
            full_command = f"cd {current_dir} && {command}\n"

            # Copy command WITH newline to clipboard
            subprocess.run(["pbcopy"], input=full_command.encode(), check=True)

            applescript = '''
            tell application "Warp"
                activate
            end tell
            delay 1.0
            tell application "System Events"
                tell process "Warp"
                    keystroke "n" using command down
                    delay 1.0
                    keystroke "v" using command down
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript], check=True)

        elif terminal == "iterm":
            # iTerm2 - use AppleScript
            applescript = f'''
            tell application "iTerm"
                activate
                create window with default profile
                tell current session of current window
                    write text "cd {current_dir} && {command}"
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript], check=True)

        else:
            # Default macOS Terminal
            applescript = f'''
            tell application "Terminal"
                do script "cd {current_dir} && {command}"
                activate
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript], check=True)

    elif system == "Windows":
        # Windows Terminal or PowerShell
        if terminal == "wt" and shutil.which("wt"):
            # Windows Terminal
            subprocess.run(["wt", "-d", current_dir, "cmd", "/k", command], check=True)
        else:
            # PowerShell fallback
            ps_command = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd {current_dir}; {command}"'
            subprocess.run(["powershell", "-Command", ps_command], check=True)

    elif system == "Linux":
        # Try common terminal emulators
        terminals = [
            ["kitty", "--directory", current_dir, "-e", "bash", "-c", f"{command}; exec bash"],
            ["gnome-terminal", "--working-directory", current_dir, "--", "bash", "-c", f"{command}; exec bash"],
            ["konsole", "--workdir", current_dir, "-e", "bash", "-c", f"{command}; exec bash"],
            ["xterm", "-e", f"cd {current_dir} && {command}; exec bash"],
        ]

        for terminal_cmd in terminals:
            try:
                subprocess.run(terminal_cmd, check=True)
                return
            except FileNotFoundError:
                continue

        raise RuntimeError("No supported terminal emulator found on Linux")

    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


def main():
    """Main entry point for the fork_terminal script."""
    args = sys.argv[1:]
    terminal = None

    # Parse --terminal flag
    if "--terminal" in args:
        idx = args.index("--terminal")
        if idx + 1 < len(args):
            terminal = args[idx + 1].lower()
            args = args[:idx] + args[idx + 2:]
        else:
            print("Error: --terminal requires an argument (warp, terminal, iterm, kitty)")
            sys.exit(1)

    if not args:
        print("Usage: fork_terminal.py [--terminal warp|terminal|iterm] <command>")
        print("\nTerminal Options:")
        print("  terminal  - Default Terminal.app (macOS) [recommended]")
        print("  iterm     - iTerm2 (macOS)")
        print("  warp      - Warp terminal (macOS) [requires manual Enter]")
        print("  kitty     - Kitty terminal (Linux/macOS)")
        print("\nEnvironment Variables:")
        print("  FORK_TERMINAL_APP - Set default terminal")
        print("\nExamples:")
        print("  fork_terminal.py 'curl https://api.example.com'")
        print("  fork_terminal.py 'gemini -m flash'")
        print("  fork_terminal.py --terminal iterm 'claude --model haiku'")
        print(f"\nDetected terminal: {get_preferred_terminal()}")
        sys.exit(1)

    command = " ".join(args)

    try:
        used_terminal = terminal or get_preferred_terminal()
        fork_terminal(command, terminal)
        print(f"✓ Forked {used_terminal} terminal with command: {command}")
    except Exception as e:
        print(f"✗ Error forking terminal: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
