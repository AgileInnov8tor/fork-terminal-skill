#!/usr/bin/env python3
"""
Tests for fork_terminal.py

Run with: python -m pytest test_fork_terminal.py -v
Or simply: python test_fork_terminal.py
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Import the module under test
from fork_terminal import (
    get_preferred_terminal,
    escape_for_applescript,
    validate_tool_availability,
    extract_tool_name,
    fork_terminal,
)


class TestGetPreferredTerminal(unittest.TestCase):
    """Tests for get_preferred_terminal function."""

    def test_returns_env_var_when_set(self):
        """Should return FORK_TERMINAL_APP when set."""
        with patch.dict(os.environ, {"FORK_TERMINAL_APP": "iterm"}):
            result = get_preferred_terminal("Darwin")
            self.assertEqual(result, "iterm")

    def test_returns_terminal_for_darwin_default(self):
        """Should return 'terminal' for macOS when no env var."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove the env var if it exists
            os.environ.pop("FORK_TERMINAL_APP", None)
            result = get_preferred_terminal("Darwin")
            self.assertEqual(result, "terminal")

    def test_returns_wt_for_windows_when_available(self):
        """Should return 'wt' for Windows when Windows Terminal is available."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FORK_TERMINAL_APP", None)
            with patch("shutil.which", return_value="/usr/bin/wt"):
                result = get_preferred_terminal("Windows")
                self.assertEqual(result, "wt")

    def test_returns_powershell_for_windows_fallback(self):
        """Should return 'powershell' when wt not available."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FORK_TERMINAL_APP", None)
            with patch("shutil.which", return_value=None):
                result = get_preferred_terminal("Windows")
                self.assertEqual(result, "powershell")

    def test_returns_available_terminal_for_linux(self):
        """Should return first available terminal on Linux."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FORK_TERMINAL_APP", None)

            def mock_which(name):
                if name == "gnome-terminal":
                    return "/usr/bin/gnome-terminal"
                return None

            with patch("shutil.which", side_effect=mock_which):
                result = get_preferred_terminal("Linux")
                self.assertEqual(result, "gnome-terminal")

    def test_returns_xterm_fallback_for_linux(self):
        """Should return 'xterm' as Linux fallback."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("FORK_TERMINAL_APP", None)
            with patch("shutil.which", return_value=None):
                result = get_preferred_terminal("Linux")
                self.assertEqual(result, "xterm")


class TestEscapeForApplescript(unittest.TestCase):
    """Tests for escape_for_applescript function."""

    def test_escapes_double_quotes(self):
        """Should escape double quotes."""
        result = escape_for_applescript('echo "hello"')
        self.assertEqual(result, 'echo \\"hello\\"')

    def test_escapes_backslashes(self):
        """Should escape backslashes."""
        result = escape_for_applescript("path\\to\\file")
        self.assertEqual(result, "path\\\\to\\\\file")

    def test_escapes_both(self):
        """Should escape both backslashes and quotes correctly."""
        result = escape_for_applescript('say "hello\\world"')
        self.assertEqual(result, 'say \\"hello\\\\world\\"')

    def test_handles_empty_string(self):
        """Should handle empty string."""
        result = escape_for_applescript("")
        self.assertEqual(result, "")

    def test_leaves_safe_chars_alone(self):
        """Should not modify safe characters."""
        safe_str = "hello world 123 !@#$%"
        result = escape_for_applescript(safe_str)
        self.assertEqual(result, safe_str)


class TestValidateToolAvailability(unittest.TestCase):
    """Tests for validate_tool_availability function."""

    def test_returns_true_when_tool_exists(self):
        """Should return (True, message) when tool is in PATH."""
        with patch("shutil.which", return_value="/usr/local/bin/claude"):
            available, msg = validate_tool_availability("claude")
            self.assertTrue(available)
            self.assertIn("Found claude", msg)
            self.assertIn("/usr/local/bin/claude", msg)

    def test_returns_false_when_tool_missing(self):
        """Should return (False, warning) when tool not found."""
        with patch("shutil.which", return_value=None):
            available, msg = validate_tool_availability("nonexistent-tool")
            self.assertFalse(available)
            self.assertIn("Warning", msg)
            self.assertIn("not found", msg)


class TestExtractToolName(unittest.TestCase):
    """Tests for extract_tool_name function."""

    def test_extracts_simple_command(self):
        """Should extract first word from simple command."""
        result = extract_tool_name("claude --model haiku")
        self.assertEqual(result, "claude")

    def test_extracts_path_command(self):
        """Should extract path-based command."""
        result = extract_tool_name("/usr/bin/python script.py")
        self.assertEqual(result, "/usr/bin/python")

    def test_handles_empty_string(self):
        """Should return None for empty string."""
        result = extract_tool_name("")
        self.assertIsNone(result)

    def test_handles_whitespace_only(self):
        """Should return None for whitespace-only string."""
        result = extract_tool_name("   ")
        self.assertIsNone(result)

    def test_handles_single_word(self):
        """Should handle single word command."""
        result = extract_tool_name("ls")
        self.assertEqual(result, "ls")


class TestForkTerminalMacOS(unittest.TestCase):
    """Tests for fork_terminal on macOS."""

    @patch("platform.system", return_value="Darwin")
    @patch("os.getcwd", return_value="/Users/test/project")
    @patch("subprocess.run")
    def test_default_terminal_uses_applescript(self, mock_run, mock_cwd, mock_system):
        """Should use AppleScript for default Terminal.app."""
        mock_run.return_value = MagicMock()

        result = fork_terminal("echo hello", terminal="terminal")

        self.assertTrue(result["success"])
        self.assertEqual(result["terminal"], "terminal")
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        self.assertEqual(call_args[0][0][0], "osascript")

    @patch("platform.system", return_value="Darwin")
    @patch("os.getcwd", return_value="/Users/test/my project")
    @patch("subprocess.run")
    def test_handles_spaces_in_path(self, mock_run, mock_cwd, mock_system):
        """Should properly escape paths with spaces."""
        mock_run.return_value = MagicMock()

        result = fork_terminal("ls", terminal="terminal")

        self.assertTrue(result["success"])
        # Verify the AppleScript was called
        call_args = mock_run.call_args
        applescript = call_args[0][0][2]  # The -e argument
        # Path should be quoted
        self.assertIn("'/Users/test/my project'", applescript)

    @patch("platform.system", return_value="Darwin")
    @patch("os.getcwd", return_value="/Users/test")
    @patch("subprocess.run")
    def test_warp_shows_warning_message(self, mock_run, mock_cwd, mock_system):
        """Should include warning about manual Enter for Warp."""
        mock_run.return_value = MagicMock()

        result = fork_terminal("echo hello", terminal="warp")

        self.assertTrue(result["success"])
        self.assertIn("ENTER", result["message"])


class TestForkTerminalLinux(unittest.TestCase):
    """Tests for fork_terminal on Linux."""

    @patch("platform.system", return_value="Linux")
    @patch("os.getcwd", return_value="/home/user/project")
    @patch("subprocess.run")
    def test_uses_specified_terminal(self, mock_run, mock_cwd, mock_system):
        """Should use the specified terminal if available."""
        mock_run.return_value = MagicMock()

        with patch("shutil.which", return_value="/usr/bin/kitty"):
            result = fork_terminal("echo hello", terminal="kitty")

        self.assertTrue(result["success"])
        self.assertEqual(result["terminal"], "kitty")

    @patch("platform.system", return_value="Linux")
    @patch("os.getcwd", return_value="/home/user/project")
    @patch("subprocess.run")
    def test_falls_back_to_available_terminal(self, mock_run, mock_cwd, mock_system):
        """Should fall back to available terminal when specified not found."""
        mock_run.return_value = MagicMock()

        def mock_which(name):
            if name == "gnome-terminal":
                return "/usr/bin/gnome-terminal"
            return None

        with patch("shutil.which", side_effect=mock_which):
            result = fork_terminal("echo hello", terminal="kitty")

        self.assertTrue(result["success"])
        self.assertEqual(result["terminal"], "gnome-terminal")

    @patch("platform.system", return_value="Linux")
    @patch("os.getcwd", return_value="/home/user/project")
    def test_raises_when_no_terminal_found(self, mock_cwd, mock_system):
        """Should raise RuntimeError when no terminal is found."""
        with patch("shutil.which", return_value=None):
            with patch("subprocess.run", side_effect=FileNotFoundError):
                with self.assertRaises(RuntimeError) as context:
                    fork_terminal("echo hello")

                self.assertIn("No supported terminal", str(context.exception))


class TestForkTerminalWindows(unittest.TestCase):
    """Tests for fork_terminal on Windows."""

    @patch("platform.system", return_value="Windows")
    @patch("os.getcwd", return_value="C:\\Users\\test\\project")
    @patch("subprocess.run")
    def test_uses_windows_terminal_when_available(self, mock_run, mock_cwd, mock_system):
        """Should use Windows Terminal when available."""
        mock_run.return_value = MagicMock()

        with patch("shutil.which", return_value="C:\\wt.exe"):
            result = fork_terminal("echo hello", terminal="wt")

        self.assertTrue(result["success"])
        self.assertIn("Windows Terminal", result["message"])

    @patch("platform.system", return_value="Windows")
    @patch("os.getcwd", return_value="C:\\Users\\test\\project")
    @patch("subprocess.run")
    def test_falls_back_to_powershell(self, mock_run, mock_cwd, mock_system):
        """Should fall back to PowerShell when wt not available."""
        mock_run.return_value = MagicMock()

        with patch("shutil.which", return_value=None):
            result = fork_terminal("echo hello", terminal="powershell")

        self.assertTrue(result["success"])
        self.assertIn("PowerShell", result["message"])


class TestForkTerminalTimeout(unittest.TestCase):
    """Tests for timeout functionality."""

    @patch("platform.system", return_value="Darwin")
    @patch("os.getcwd", return_value="/Users/test")
    @patch("subprocess.run")
    def test_passes_timeout_to_subprocess(self, mock_run, mock_cwd, mock_system):
        """Should pass timeout to subprocess.run."""
        mock_run.return_value = MagicMock()

        fork_terminal("echo hello", terminal="terminal", timeout=30)

        call_kwargs = mock_run.call_args[1]
        self.assertEqual(call_kwargs["timeout"], 30)


class TestSecurityEscaping(unittest.TestCase):
    """Tests for security-related escaping."""

    @patch("platform.system", return_value="Darwin")
    @patch("os.getcwd", return_value="/Users/test")
    @patch("subprocess.run")
    def test_escapes_quotes_in_command(self, mock_run, mock_cwd, mock_system):
        """Should properly escape quotes in commands."""
        mock_run.return_value = MagicMock()

        result = fork_terminal('echo "hello world"', terminal="terminal")

        self.assertTrue(result["success"])
        call_args = mock_run.call_args
        applescript = call_args[0][0][2]
        # Quotes should be escaped in AppleScript
        self.assertIn('\\"', applescript)

    @patch("platform.system", return_value="Darwin")
    @patch("os.getcwd", return_value="/Users/test/project's folder")
    @patch("subprocess.run")
    def test_handles_apostrophes_in_path(self, mock_run, mock_cwd, mock_system):
        """Should handle apostrophes in directory path."""
        mock_run.return_value = MagicMock()

        result = fork_terminal("ls", terminal="terminal")

        self.assertTrue(result["success"])


class TestUnsupportedOS(unittest.TestCase):
    """Tests for unsupported operating systems."""

    @patch("platform.system", return_value="FreeBSD")
    @patch("os.getcwd", return_value="/home/user")
    def test_raises_for_unsupported_os(self, mock_cwd, mock_system):
        """Should raise RuntimeError for unsupported OS."""
        with self.assertRaises(RuntimeError) as context:
            fork_terminal("echo hello")

        self.assertIn("Unsupported operating system", str(context.exception))
        self.assertIn("FreeBSD", str(context.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
