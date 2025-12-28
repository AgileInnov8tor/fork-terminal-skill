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
import shlex
import json
from typing import Optional, Tuple


def get_preferred_terminal(system: str = None) -> str:
    """Get the preferred terminal from environment or detect available.

    Args:
        system: Operating system name (Darwin, Windows, Linux). Auto-detected if None.

    Returns:
        Terminal identifier string.
    """
    if system is None:
        system = platform.system()

    # Check environment variable first
    env_terminal = os.environ.get("FORK_TERMINAL_APP", "").lower()
    if env_terminal:
        return env_terminal

    # Platform-specific defaults
    if system == "Darwin":
        # Default to Terminal.app on macOS (most reliable with AppleScript)
        return "terminal"
    elif system == "Windows":
        # Prefer Windows Terminal if available
        if shutil.which("wt"):
            return "wt"
        return "powershell"
    elif system == "Linux":
        # Try to find an available terminal
        linux_terminals = ["kitty", "gnome-terminal", "konsole", "xterm"]
        for term in linux_terminals:
            if shutil.which(term):
                return term
        return "xterm"  # Fallback

    return "terminal"


def escape_for_applescript(s: str) -> str:
    """Escape a string for safe inclusion in AppleScript.

    Args:
        s: String to escape.

    Returns:
        Escaped string safe for AppleScript double-quoted strings.
    """
    # Escape backslashes first, then double quotes
    return s.replace("\\", "\\\\").replace('"', '\\"')


def validate_tool_availability(tool_name: str) -> Tuple[bool, str]:
    """Check if a CLI tool is available in PATH.

    Args:
        tool_name: Name of the tool to check (e.g., 'claude', 'gemini').

    Returns:
        Tuple of (is_available, message).
    """
    tool_path = shutil.which(tool_name)
    if tool_path:
        return True, f"Found {tool_name} at {tool_path}"
    return False, f"Warning: '{tool_name}' not found in PATH. The command may fail."


def fork_terminal(command: str, terminal: str = None, timeout: int = None) -> dict:
    """
    Fork a new terminal window and execute the given command.

    Args:
        command: The command to execute in the new terminal.
        terminal: Preferred terminal app (warp, terminal, iterm, kitty, etc.).
        timeout: Optional timeout in seconds for the fork operation itself.

    Returns:
        dict with keys: success (bool), terminal (str), message (str).

    Raises:
        RuntimeError: If no supported terminal is found or OS is unsupported.
    """
    current_dir = os.getcwd()
    system = platform.system()

    if terminal is None:
        terminal = get_preferred_terminal(system)

    # Properly escape paths and commands for shell embedding
    safe_dir = shlex.quote(current_dir)
    safe_command = command  # Command is passed as-is; user is responsible for quoting

    result = {"success": False, "terminal": terminal, "message": ""}

    if system == "Darwin":  # macOS
        if terminal == "warp":
            # Warp terminal - use clipboard paste approach
            # WARNING: Warp has AppleScript limitations - requires manual Enter key
            full_command = f"cd {safe_dir} && {safe_command}\n"

            # Copy command WITH newline to clipboard
            subprocess.run(["pbcopy"], input=full_command.encode(), check=True, timeout=timeout)

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
            subprocess.run(["osascript", "-e", applescript], check=True, timeout=timeout)
            result["success"] = True
            result["message"] = "Command pasted to Warp. Press ENTER to execute (Warp limitation)."

        elif terminal == "iterm":
            # iTerm2 - use AppleScript with proper escaping
            escaped_dir = escape_for_applescript(current_dir)
            escaped_cmd = escape_for_applescript(safe_command)
            applescript = f'''
            tell application "iTerm"
                activate
                create window with default profile
                tell current session of current window
                    write text "cd {shlex.quote(escaped_dir)} && {escaped_cmd}"
                end tell
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript], check=True, timeout=timeout)
            result["success"] = True
            result["message"] = "Opened new iTerm2 window."

        else:
            # Default macOS Terminal with proper escaping
            escaped_dir = escape_for_applescript(current_dir)
            escaped_cmd = escape_for_applescript(safe_command)
            applescript = f'''
            tell application "Terminal"
                do script "cd {shlex.quote(escaped_dir)} && {escaped_cmd}"
                activate
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript], check=True, timeout=timeout)
            result["success"] = True
            result["message"] = "Opened new Terminal window."

    elif system == "Windows":
        # Properly escape for Windows
        # Windows Terminal or PowerShell
        if terminal == "wt" and shutil.which("wt"):
            # Windows Terminal - arguments are passed directly, no shell escaping needed
            subprocess.run(["wt", "-d", current_dir, "cmd", "/k", command], check=True, timeout=timeout)
            result["success"] = True
            result["message"] = "Opened new Windows Terminal tab."
        else:
            # PowerShell fallback - need to escape for PowerShell
            # Use JSON encoding for safe string passing
            ps_dir = current_dir.replace("'", "''")
            ps_cmd = command.replace("'", "''")
            ps_command = f"Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd ''{ps_dir}''; {ps_cmd}'"
            subprocess.run(["powershell", "-Command", ps_command], check=True, timeout=timeout)
            result["success"] = True
            result["message"] = "Opened new PowerShell window."

    elif system == "Linux":
        # Build terminal commands with proper escaping
        bash_cmd = f"{safe_command}; exec bash"

        # Map of terminal -> command builder
        terminal_commands = {
            "kitty": ["kitty", "--directory", current_dir, "-e", "bash", "-c", bash_cmd],
            "gnome-terminal": ["gnome-terminal", "--working-directory", current_dir, "--", "bash", "-c", bash_cmd],
            "konsole": ["konsole", "--workdir", current_dir, "-e", "bash", "-c", bash_cmd],
            "xterm": ["xterm", "-e", "bash", "-c", f"cd {safe_dir} && {bash_cmd}"],
            "alacritty": ["alacritty", "--working-directory", current_dir, "-e", "bash", "-c", bash_cmd],
            "tilix": ["tilix", "--working-directory", current_dir, "-e", "bash", "-c", bash_cmd],
        }

        # If user specified a terminal, try that first
        if terminal in terminal_commands:
            if shutil.which(terminal):
                subprocess.run(terminal_commands[terminal], check=True, timeout=timeout)
                result["success"] = True
                result["message"] = f"Opened new {terminal} window."
                return result
            else:
                print(f"Warning: Specified terminal '{terminal}' not found, trying alternatives...", file=sys.stderr)

        # Try terminals in preference order
        for term_name, term_cmd in terminal_commands.items():
            if shutil.which(term_name):
                try:
                    subprocess.run(term_cmd, check=True, timeout=timeout)
                    result["success"] = True
                    result["terminal"] = term_name
                    result["message"] = f"Opened new {term_name} window."
                    return result
                except subprocess.CalledProcessError:
                    continue

        raise RuntimeError("No supported terminal emulator found on Linux. Install one of: kitty, gnome-terminal, konsole, xterm, alacritty, tilix")

    else:
        raise RuntimeError(f"Unsupported operating system: {system}")

    return result


def extract_tool_name(command: str) -> Optional[str]:
    """Extract the primary tool name from a command for validation.

    Args:
        command: The full command string.

    Returns:
        The tool name (first word) or None if empty.
    """
    parts = command.strip().split()
    if parts:
        return parts[0]
    return None


def main():
    """Main entry point for the fork_terminal script."""
    args = sys.argv[1:]
    terminal = None
    timeout = None
    validate = True
    output_json = False

    # Parse flags
    while args:
        if args[0] == "--terminal" and len(args) > 1:
            terminal = args[1].lower()
            args = args[2:]
        elif args[0] == "--timeout" and len(args) > 1:
            try:
                timeout = int(args[1])
            except ValueError:
                print("Error: --timeout requires an integer value (seconds)", file=sys.stderr)
                sys.exit(1)
            args = args[2:]
        elif args[0] == "--no-validate":
            validate = False
            args = args[1:]
        elif args[0] == "--json":
            output_json = True
            args = args[1:]
        elif args[0] == "--help" or args[0] == "-h":
            args = []  # Trigger help display
            break
        elif args[0].startswith("--"):
            print(f"Error: Unknown flag {args[0]}", file=sys.stderr)
            sys.exit(1)
        else:
            break

    if not args:
        system = platform.system()
        print("Fork Terminal - Open new terminal instances for CLI commands or agentic tools")
        print("")
        print("Usage: fork_terminal.py [OPTIONS] <command>")
        print("")
        print("Options:")
        print("  --terminal <name>  Specify terminal emulator")
        print("  --timeout <secs>   Timeout for fork operation")
        print("  --no-validate      Skip tool availability check")
        print("  --json             Output result as JSON")
        print("  --help, -h         Show this help message")
        print("")
        print("Terminal Options:")
        if system == "Darwin":
            print("  terminal  - Default Terminal.app [recommended]")
            print("  iterm     - iTerm2")
            print("  warp      - Warp terminal [requires manual Enter]")
            print("  kitty     - Kitty terminal")
        elif system == "Windows":
            print("  wt        - Windows Terminal [recommended if available]")
            print("  powershell - PowerShell")
        else:
            print("  kitty          - Kitty terminal")
            print("  gnome-terminal - GNOME Terminal")
            print("  konsole        - KDE Konsole")
            print("  alacritty      - Alacritty")
            print("  tilix          - Tilix")
            print("  xterm          - XTerm")
        print("")
        print("Environment Variables:")
        print("  FORK_TERMINAL_APP - Set default terminal preference")
        print("")
        print("Examples:")
        print("  fork_terminal.py 'curl https://api.example.com'")
        print("  fork_terminal.py 'claude --model haiku'")
        print("  fork_terminal.py --terminal iterm 'npm run dev'")
        print("  fork_terminal.py --timeout 30 'long-running-command'")
        print("")
        print(f"Detected OS: {system}")
        print(f"Default terminal: {get_preferred_terminal(system)}")
        sys.exit(0)

    command = " ".join(args)

    # Validate tool availability if requested
    if validate:
        tool_name = extract_tool_name(command)
        if tool_name:
            is_available, msg = validate_tool_availability(tool_name)
            if not is_available:
                print(f"⚠ {msg}", file=sys.stderr)

    try:
        result = fork_terminal(command, terminal, timeout)

        if output_json:
            result["command"] = command
            result["working_directory"] = os.getcwd()
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"✓ Forked terminal: {result['terminal']}")
                print(f"  Command: {command}")
                if result.get("message"):
                    print(f"  {result['message']}")
            else:
                print(f"✗ Failed to fork terminal", file=sys.stderr)
                sys.exit(1)

    except subprocess.TimeoutExpired:
        error_msg = f"Timeout after {timeout} seconds"
        if output_json:
            print(json.dumps({"success": False, "error": error_msg}))
        else:
            print(f"✗ {error_msg}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_msg = str(e)
        if output_json:
            print(json.dumps({"success": False, "error": error_msg}))
        else:
            print(f"✗ Error forking terminal: {error_msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
