#!/usr/bin/env python3
"""
Generate Summary - Create conversation summaries for fork handoff

This tool generates a markdown summary from conversation data that can be
passed to a forked terminal session to provide context.

Usage:
    python generate_summary.py --user-request "Original request" --response-summary "What was done"
    python generate_summary.py --from-json context.json
    python generate_summary.py --interactive

Output:
    Prints the formatted summary to stdout, suitable for piping to a file
    or passing to a forked session.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def get_template_path() -> Path:
    """Get the path to the summary template."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "prompts" / "fork-summary-user-prompt.md"


def load_template() -> str:
    """Load the summary template."""
    template_path = get_template_path()
    if template_path.exists():
        return template_path.read_text()

    # Fallback template if file not found
    return """# Forked Session Context

You are continuing work from a previous conversation session.

## Summary of User's Request

{summarized_user_prompt}

## Summary of Work Done

{response_summary}

## Current Working Directory

{working_directory}

## Relevant Files

{relevant_files}

## Key Decisions Made

{key_decisions}

## Next Steps

{next_steps}

---

**Instructions**: Continue the work described above. You have context from the previous session.
"""


def format_list(items: Optional[List[str]], empty_text: str = "_None specified_") -> str:
    """Format a list of items as markdown bullet points."""
    if not items:
        return empty_text
    return "\n".join(f"- {item}" for item in items)


def generate_summary(
    user_request: str,
    response_summary: str,
    working_directory: Optional[str] = None,
    relevant_files: Optional[List[str]] = None,
    key_decisions: Optional[List[str]] = None,
    next_steps: Optional[str] = None,
    conversation_history: Optional[str] = None,
) -> str:
    """
    Generate a formatted summary for fork handoff.

    Args:
        user_request: The original user request/task
        response_summary: Summary of what was accomplished
        working_directory: Current working directory (auto-detected if None)
        relevant_files: List of files that were modified or referenced
        key_decisions: List of important decisions made during the session
        next_steps: Description of recommended next steps
        conversation_history: Optional condensed conversation history

    Returns:
        Formatted markdown summary string
    """
    if working_directory is None:
        working_directory = os.getcwd()

    template = load_template()

    # Handle the template variables
    # The template uses {{variable}} syntax from Handlebars, but we'll do simple replacement
    summary = template

    # Replace template variables
    replacements = {
        "{{conversation_history}}": conversation_history or "_No conversation history provided_",
        "{{summarized_user_prompt}}": user_request,
        "{{response_summary}}": response_summary,
        "{{working_directory}}": working_directory,
        "{{relevant_files}}": format_list(relevant_files, "_No specific files mentioned_"),
        "{{key_decisions}}": format_list(key_decisions, "_No key decisions documented_"),
        "{{next_steps}}": next_steps or "_Continue with the task as described_",
    }

    for key, value in replacements.items():
        summary = summary.replace(key, value)

    # Handle Handlebars conditionals by replacing them with the content
    # This is a simplified handler - just removes the conditional syntax
    import re

    # Remove {{#if ...}} and {{/if}} blocks, keeping content
    summary = re.sub(r'\{\{#if \w+\}\}\s*', '', summary)
    summary = re.sub(r'\{\{/if\}\}\s*', '', summary)

    # Remove {{#each ...}} loops - replace with the formatted list already inserted
    summary = re.sub(r'\{\{#each \w+\}\}\s*', '', summary)
    summary = re.sub(r'\{\{/each\}\}\s*', '', summary)

    # Remove {{else}} blocks
    summary = re.sub(r'\{\{else\}\}[^{]*', '', summary)

    # Remove any remaining {{this}} references
    summary = re.sub(r'\{\{this\}\}', '', summary)

    return summary.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate conversation summary for fork handoff",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic summary
  python generate_summary.py \\
    --user-request "Implement user authentication" \\
    --response-summary "Added JWT-based auth with login/logout endpoints"

  # Full summary with all context
  python generate_summary.py \\
    --user-request "Refactor database layer" \\
    --response-summary "Migrated to repository pattern" \\
    --files src/db.py src/repos/*.py \\
    --decisions "Used SQLAlchemy ORM" "Added connection pooling" \\
    --next-steps "Add unit tests for repositories"

  # From JSON file
  python generate_summary.py --from-json context.json

  # Save to file
  python generate_summary.py --user-request "..." --response-summary "..." -o summary.md
        """
    )

    parser.add_argument(
        "--user-request", "-u",
        help="The original user request or task description"
    )
    parser.add_argument(
        "--response-summary", "-r",
        help="Summary of what was accomplished"
    )
    parser.add_argument(
        "--files", "-f",
        nargs="*",
        help="List of relevant files"
    )
    parser.add_argument(
        "--decisions", "-d",
        nargs="*",
        help="Key decisions made during the session"
    )
    parser.add_argument(
        "--next-steps", "-n",
        help="Recommended next steps"
    )
    parser.add_argument(
        "--working-dir", "-w",
        help="Working directory (defaults to current)"
    )
    parser.add_argument(
        "--conversation", "-c",
        help="Condensed conversation history"
    )
    parser.add_argument(
        "--from-json", "-j",
        help="Load context from a JSON file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (defaults to stdout)"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode - prompt for each field"
    )

    args = parser.parse_args()

    # Load from JSON if specified
    if args.from_json:
        try:
            with open(args.from_json) as f:
                data = json.load(f)

            summary = generate_summary(
                user_request=data.get("user_request", ""),
                response_summary=data.get("response_summary", ""),
                working_directory=data.get("working_directory"),
                relevant_files=data.get("relevant_files"),
                key_decisions=data.get("key_decisions"),
                next_steps=data.get("next_steps"),
                conversation_history=data.get("conversation_history"),
            )
        except FileNotFoundError:
            print(f"Error: File not found: {args.from_json}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.interactive:
        print("=== Fork Summary Generator (Interactive Mode) ===\n")

        user_request = input("User's original request: ").strip()
        response_summary = input("Summary of work done: ").strip()

        files_input = input("Relevant files (comma-separated, or empty): ").strip()
        relevant_files = [f.strip() for f in files_input.split(",")] if files_input else None

        decisions_input = input("Key decisions (comma-separated, or empty): ").strip()
        key_decisions = [d.strip() for d in decisions_input.split(",")] if decisions_input else None

        next_steps = input("Next steps (or empty): ").strip() or None

        summary = generate_summary(
            user_request=user_request,
            response_summary=response_summary,
            relevant_files=relevant_files,
            key_decisions=key_decisions,
            next_steps=next_steps,
        )

    elif args.user_request and args.response_summary:
        summary = generate_summary(
            user_request=args.user_request,
            response_summary=args.response_summary,
            working_directory=args.working_dir,
            relevant_files=args.files,
            key_decisions=args.decisions,
            next_steps=args.next_steps,
            conversation_history=args.conversation,
        )

    else:
        parser.print_help()
        print("\nError: Either --user-request and --response-summary, --from-json, or --interactive is required")
        sys.exit(1)

    # Output the summary
    if args.output:
        with open(args.output, "w") as f:
            f.write(summary)
        print(f"Summary written to: {args.output}")
    else:
        print(summary)


if __name__ == "__main__":
    main()
