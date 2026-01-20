# pylint: disable=import-error
import typer
import os

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from .auditor import FairHousingAuditor

app = typer.Typer(help="FairProp: The Open Source Standard for Fair Housing Compliance.")
console = Console()

@app.command()
def scan(
    text: str = typer.Argument(..., help="Text to scan or path to a text file."),
    rules: str = typer.Option("fha_rules.json", help="Path to rules JSON."),
    jurisdiction: list[str] = typer.Option(None, "--jurisdiction", "-j", help="Additional jurisdictions (e.g., california, nyc)"),
):
    """
    Scans a text string or file for Fair Housing Act violations.
    """
    if os.path.exists(text):
        with open(text, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = text

    console.print(Panel("[bold blue]Scanning content...[/bold blue]"))
    
    try:
        auditor = FairHousingAuditor(rules_path=rules, jurisdictions=jurisdiction or [])
        report = auditor.scan_text(content)
        
        # Display Score
        score_color = "green" if report['is_safe'] else "red"
        console.print(f"Safety Score: [{score_color}]{report['score']}/100[/{score_color}]")
        
        if report['flagged_items']:
            console.print("\n[bold red]Violations Found:[/bold red]")
            for item in report['flagged_items']:
                severity_icon = "🔴" if item['severity'] == "Critical" else "🟡"
                console.print(f"{severity_icon} [bold]{item['category']}[/bold]")
                console.print(f"   Found: [italic]'{item['found_word']}'[/italic]")
                console.print(f"   Suggestion: {item['suggestion']}")
                console.print(f"   Basis: {item['legal_basis']}\n")
        else:
            console.print("\n[bold green]No violations found! ✅[/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@app.command()
def fix(
    text: str = typer.Argument(..., help="Text to fix."),
):
    """
    Suggests an AI-generated compliant version of the text.
    """
    console.print("[bold yellow]Generating fix...[/bold yellow]")
    try:
        auditor = FairHousingAuditor()
        fixed = auditor.suggest_fix(text)
        console.print(Panel(Markdown(fixed), title="Suggested Revision"))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()
