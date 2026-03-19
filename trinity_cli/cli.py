#!/usr/bin/env python3
"""
Trinity CLI - Three AI perspectives, one unified answer.
C1 Mechanic x C2 Architect x C3 Oracle = Convergence

Usage:
    trinity ask "How should I structure my API?"
    trinity review path/to/file.py
    trinity debug "TypeError: cannot read property..."
    trinity code "Create a function that validates emails"
"""

import click
import requests
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.columns import Columns
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Trinity API endpoint
TRINITY_API = "https://trinity-api-production-dff4.up.railway.app/trinity"

console = Console() if RICH_AVAILABLE else None


def print_output(text, style=None):
    """Print with or without rich formatting."""
    if RICH_AVAILABLE and console:
        if style:
            console.print(text, style=style)
        else:
            console.print(text)
    else:
        print(text)


def call_trinity(prompt: str) -> dict:
    """Call the Trinity API and return the response."""
    try:
        response = requests.post(
            TRINITY_API,
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"},
            timeout=120  # Trinity needs time to converge
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Trinity is taking too long to converge. Try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection failed: {str(e)}"}


def display_trinity_response(data: dict):
    """Display Trinity's three perspectives and convergence."""
    if "error" in data:
        print_output(f"[ERROR] {data['error']}", style="bold red")
        return

    trinity = data.get("trinity", {})
    convergence = data.get("convergence", "No convergence")

    if RICH_AVAILABLE and console:
        # Rich formatted output
        console.print()

        # C1 Mechanic
        console.print(Panel(
            trinity.get("c1_mechanic", "No response"),
            title="[green]C1 MECHANIC[/green]",
            subtitle="What CAN be built NOW",
            border_style="green"
        ))

        # C2 Architect
        console.print(Panel(
            trinity.get("c2_architect", "No response"),
            title="[cyan]C2 ARCHITECT[/cyan]",
            subtitle="What SHOULD scale",
            border_style="cyan"
        ))

        # C3 Oracle
        console.print(Panel(
            trinity.get("c3_oracle", "No response"),
            title="[magenta]C3 ORACLE[/magenta]",
            subtitle="What MUST emerge",
            border_style="magenta"
        ))

        # Convergence
        console.print(Panel(
            convergence,
            title="[yellow]TRINITY CONVERGENCE[/yellow]",
            subtitle="C1 x C2 x C3 = Unified Answer",
            border_style="yellow"
        ))
        console.print()
    else:
        # Plain text fallback
        print("\n" + "="*60)
        print("C1 MECHANIC (Build Now):")
        print("-"*40)
        print(trinity.get("c1_mechanic", "No response"))

        print("\n" + "="*60)
        print("C2 ARCHITECT (Scale):")
        print("-"*40)
        print(trinity.get("c2_architect", "No response"))

        print("\n" + "="*60)
        print("C3 ORACLE (Vision):")
        print("-"*40)
        print(trinity.get("c3_oracle", "No response"))

        print("\n" + "="*60)
        print("TRINITY CONVERGENCE:")
        print("-"*40)
        print(convergence)
        print("="*60 + "\n")


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', '-v', is_flag=True, help='Show version')
def main(ctx, version):
    """Trinity CLI - Three AI minds, one convergence.

    \b
    Commands:
      ask     Ask Trinity anything
      review  Review code from a file
      debug   Debug an error message
      code    Generate code from description

    \b
    Example:
      trinity ask "How do I structure a REST API?"
      trinity review ./myfile.py
      trinity debug "TypeError: undefined is not a function"
    """
    if version:
        print_output("Trinity CLI v1.0.0")
        print_output("C1 x C2 x C3 = Infinity")
        return

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument('question', nargs=-1, required=True)
def ask(question):
    """Ask Trinity any development question.

    Example: trinity ask How should I structure my database?
    """
    prompt = " ".join(question)
    print_output(f"Asking Trinity: {prompt}", style="dim")
    print_output("Converging C1 + C2 + C3...", style="dim italic")

    data = call_trinity(prompt)
    display_trinity_response(data)


@main.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--focus', '-f', default=None, help='What to focus on (bugs, performance, security)')
def review(filepath, focus):
    """Review code from a file.

    Example: trinity review ./myapp.py --focus security
    """
    path = Path(filepath)
    code = path.read_text(encoding='utf-8', errors='ignore')

    # Truncate if too long
    if len(code) > 8000:
        code = code[:8000] + "\n\n... [truncated for API limits]"

    focus_text = f" Focus on: {focus}." if focus else ""
    prompt = f"""Review this code and provide feedback.{focus_text}

File: {path.name}
```
{code}
```

Analyze for bugs, improvements, and best practices."""

    print_output(f"Reviewing: {filepath}", style="dim")
    print_output("Converging C1 + C2 + C3...", style="dim italic")

    data = call_trinity(prompt)
    display_trinity_response(data)


@main.command()
@click.argument('error', nargs=-1, required=True)
@click.option('--code', '-c', default=None, help='Include code snippet for context')
def debug(error, code):
    """Debug an error message.

    Example: trinity debug TypeError cannot read property undefined
    """
    error_text = " ".join(error)

    code_context = ""
    if code:
        code_context = f"\n\nRelevant code:\n```\n{code}\n```"

    prompt = f"""Debug this error and explain how to fix it:

Error: {error_text}{code_context}

Provide the root cause and solution."""

    print_output(f"Debugging: {error_text[:50]}...", style="dim")
    print_output("Converging C1 + C2 + C3...", style="dim italic")

    data = call_trinity(prompt)
    display_trinity_response(data)


@main.command()
@click.argument('description', nargs=-1, required=True)
@click.option('--lang', '-l', default='python', help='Programming language')
def code(description, lang):
    """Generate code from a description.

    Example: trinity code Create a function that validates email addresses --lang python
    """
    desc_text = " ".join(description)

    prompt = f"""Generate {lang} code for the following:

{desc_text}

Provide clean, well-documented code with examples."""

    print_output(f"Generating {lang} code...", style="dim")
    print_output("Converging C1 + C2 + C3...", style="dim italic")

    data = call_trinity(prompt)
    display_trinity_response(data)


@main.command()
@click.argument('prompt', nargs=-1, required=True)
def raw(prompt):
    """Send a raw prompt to Trinity (power user mode).

    Example: trinity raw Design a microservices architecture for e-commerce
    """
    prompt_text = " ".join(prompt)
    print_output("Converging C1 + C2 + C3...", style="dim italic")

    data = call_trinity(prompt_text)
    display_trinity_response(data)


if __name__ == "__main__":
    main()
