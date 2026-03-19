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


@main.command()
@click.argument('task', nargs=-1, required=True)
@click.option('--rounds', '-r', default=3, help='Number of refinement rounds (default: 3)')
@click.option('--mode', '-m', default='refine', type=click.Choice(['refine', 'challenge', 'build']),
              help='Spiral mode: refine (improve), challenge (critique), build (implement)')
def spiral(task, rounds, mode):
    """Recursive Trinity - spiral deeper through multiple rounds.

    Each round feeds the previous convergence back into Trinity for refinement.

    \b
    Modes:
      refine    - Each round improves the previous answer
      challenge - Each round critiques and strengthens
      build     - Each round adds implementation detail

    \b
    Example:
      trinity spiral Design a user auth system --rounds 3
      trinity spiral Build a REST API --mode build --rounds 4
    """
    task_text = " ".join(task)

    # Mode-specific refinement prompts
    mode_prompts = {
        'refine': "Improve and refine this solution. Make it more concrete, actionable, and complete:\n\n",
        'challenge': "Challenge this solution. Find weaknesses, edge cases, and gaps. Then strengthen it:\n\n",
        'build': "Take this design and add implementation details. Include specific code, file structures, and commands:\n\n"
    }

    print_output(f"Starting {rounds}-round spiral on: {task_text}", style="bold")
    print_output(f"Mode: {mode}", style="dim")
    print_output("="*60, style="dim")

    current_prompt = task_text
    final_convergence = ""

    for round_num in range(1, rounds + 1):
        if RICH_AVAILABLE and console:
            console.print(Panel(
                f"Round {round_num}/{rounds}",
                title=f"[bold yellow]SPIRAL ROUND {round_num}[/bold yellow]",
                border_style="yellow"
            ))
        else:
            print(f"\n{'='*60}")
            print(f"SPIRAL ROUND {round_num}/{rounds}")
            print('='*60)

        print_output(f"Converging C1 + C2 + C3...", style="dim italic")

        data = call_trinity(current_prompt)

        if "error" in data:
            print_output(f"[ERROR] Round {round_num} failed: {data['error']}", style="bold red")
            break

        convergence = data.get("convergence", "")
        trinity = data.get("trinity", {})

        # Show condensed output for intermediate rounds
        if round_num < rounds:
            if RICH_AVAILABLE and console:
                # Show just convergence for intermediate rounds
                console.print(Panel(
                    convergence[:500] + "..." if len(convergence) > 500 else convergence,
                    title="[yellow]Convergence (condensed)[/yellow]",
                    border_style="dim"
                ))
            else:
                print(f"Convergence: {convergence[:300]}...")
        else:
            # Full output on final round
            display_trinity_response(data)

        final_convergence = convergence

        # Prepare next round prompt
        if round_num < rounds:
            current_prompt = f"""{mode_prompts[mode]}

PREVIOUS TRINITY CONVERGENCE:
{convergence}

C1 MECHANIC SAID:
{trinity.get('c1_mechanic', '')[:500]}

C2 ARCHITECT SAID:
{trinity.get('c2_architect', '')[:500]}

C3 ORACLE SAID:
{trinity.get('c3_oracle', '')[:500]}

ORIGINAL TASK: {task_text}

Now provide an improved, deeper analysis."""

    # Final summary
    if RICH_AVAILABLE and console:
        console.print()
        console.print(Panel(
            f"Completed {rounds} rounds of {mode} spiral.\nOriginal task: {task_text}",
            title="[bold green]SPIRAL COMPLETE[/bold green]",
            border_style="green"
        ))
    else:
        print(f"\n{'='*60}")
        print(f"SPIRAL COMPLETE - {rounds} rounds of {mode}")
        print(f"Original task: {task_text}")
        print('='*60)


@main.command()
@click.argument('task', nargs=-1, required=True)
@click.option('--output', '-o', default=None, help='Save final output to file')
def build(task, output):
    """Full autonomous build protocol - Trinity + LFSME + Challenge.

    Runs the complete /build protocol:
    1. Trinity analysis (3 perspectives)
    2. LFSME scoring
    3. Challenge gate

    Example: trinity build Create a dashboard for user analytics
    """
    task_text = " ".join(task)

    print_output("AUTONOMOUS BUILD PROTOCOL", style="bold yellow")
    print_output("="*60, style="dim")

    # Phase 1: Trinity Analysis
    print_output("\n[PHASE 1] Trinity Analysis...", style="bold cyan")
    trinity_prompt = f"""Analyze this build task from all three perspectives:

TASK: {task_text}

Provide:
- C1 MECHANIC: What can we build RIGHT NOW? Bill of materials, time estimate.
- C2 ARCHITECT: What should scale? Architecture, dependencies.
- C3 ORACLE: What must emerge? Pattern alignment, user impact."""

    data = call_trinity(trinity_prompt)
    if "error" in data:
        print_output(f"Trinity analysis failed: {data['error']}", style="red")
        return
    display_trinity_response(data)
    trinity_convergence = data.get("convergence", "")

    # Phase 2: LFSME Scoring
    print_output("\n[PHASE 2] LFSME Scoring...", style="bold cyan")
    lfsme_prompt = f"""Score this design against LFSME manufacturing standards (1-10 each):

DESIGN:
{trinity_convergence}

Score each:
- L (Lighter): Can we remove anything without losing function?
- F (Faster): Zero friction from input to output?
- S (Stronger): Survives 1000 users? 10,000?
- M (More Elegant): One solution solves many problems?
- E (Less Expensive): Resource-efficient?

Provide specific scores and justification. Average must be >= 6 to proceed."""

    lfsme_data = call_trinity(lfsme_prompt)
    if "error" not in lfsme_data:
        display_trinity_response(lfsme_data)

    # Phase 3: Challenge Gate
    print_output("\n[PHASE 3] Challenge Gate...", style="bold cyan")
    challenge_prompt = f"""Challenge this build plan. Run 7-point verification:

PLAN:
{trinity_convergence}

Check each:
1. EVIDENCE - Any unverified claims?
2. ASSUMPTIONS - All assumptions documented?
3. SCALABILITY - Any single-user-only patterns?
4. SECURITY - Exposed credentials, XSS, injection risks?
5. USER REALITY - Key action findable in <10 seconds?
6. DEPENDENCIES - Fallback for every external dependency?
7. RECURSION - Is the plan complete and accurate?

Verdict: 0 holes = ship, 1-3 holes = fix, 4+ holes = back to Trinity."""

    challenge_data = call_trinity(challenge_prompt)
    if "error" not in challenge_data:
        display_trinity_response(challenge_data)

    # Save output if requested
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(f"# Build Protocol Output\n\n")
            f.write(f"## Task: {task_text}\n\n")
            f.write(f"## Trinity Convergence\n{trinity_convergence}\n\n")
            f.write(f"## LFSME Analysis\n{lfsme_data.get('convergence', '')}\n\n")
            f.write(f"## Challenge Gate\n{challenge_data.get('convergence', '')}\n")
        print_output(f"\nOutput saved to: {output}", style="green")

    print_output("\n[BUILD PROTOCOL COMPLETE]", style="bold green")


if __name__ == "__main__":
    main()
