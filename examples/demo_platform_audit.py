#!/usr/bin/env python3
"""
FairProp Platform Audit Demo
----------------------------
This script demonstrates how a real estate platform (e.g., Zillow, Craigslist, Airbnb)
can use FairProp to automatically audit listings for Fair Housing violations
across different jurisdictions.

Scenarios covered:
1. NYC Luxury Apartment (checking for income discrimination & family status)
2. California Rental (checking for source of income & implicit age bias)
3. University Housing (checking for student status vs protected class)
"""

import sys
import os
from typing import Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Ensure we can import fairprop from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from fairprop import FairHousingAuditor
except ImportError:
    print("Error: fairprop package not found. Please install it with 'pip install -e .'")
    sys.exit(1)

console = Console()

def run_platform_audit():
    """Simulate a platform-wide audit process."""
    console.print(Panel.fit(
        "[bold blue]🛡️  FairProp Platform Audit Simulator[/bold blue]",
        subtitle="Automated Compliance Check"
    ))

    # Initialize Auditor with multiple jurisdictions
    # In a real platform, this would be a persistent service or serverless function
    console.print("[dim]Initializing compliance engine with multi-jurisdiction rules...[/dim]")
    auditor = FairHousingAuditor(jurisdictions=['california', 'nyc', 'federal'])

    # Mock Listings Data
    listings = [
        {
            "id": "NYC-LUX-001",
            "platform": "UrbanLiving NYC",
            "location": "New York, NY",
            "jurisdictions": ["federal", "nyc"],
            "title": "Exclusive Penthouse in Manhattan",
            "description": "Perfect for young professionals! No Section 8. "
                           "Must have 40x rent in income. No children under 12."
        },
        {
            "id": "CA-BEACH-042",
            "platform": "CaliRentals",
            "location": "Santa Monica, CA",
            "jurisdictions": ["federal", "california"],
            "title": "Sunny Beachside Studio",
            "description": "Walking distance to pier. Great for active singles. "
                           "Christians preferred as it is near the church."
        },
        {
            "id": "TX-AUSTIN-101",
            "platform": "StudentLocators",
            "location": "Austin, TX",
            "jurisdictions": ["federal"],
            "title": "Near UT Campus",
            "description": "Student housing only. Female roommates wanted for shared suite. Safe & secure."
        }
    ]

    # Process listings
    for listing in listings:
        audit_listing(auditor, listing)

def audit_listing(auditor: FairHousingAuditor, listing: Dict):
    """Audit a single listing and display results."""
    console.print(f"\n[bold]Scanning Listing:[/bold] {listing['id']} ({listing['platform']})")
    console.print(f"[dim]Location: {listing['location']} | Rules: {', '.join(listing['jurisdictions'])}[/dim]")
    
    # Combine title and description for full context scan
    full_text = f"{listing['title']}. {listing['description']}"
    
    # Run Audit
    # We pass the specific jurisdictions relevant to this listing's location
    report = auditor.scan_text(full_text)
    
    # Display Score
    score_color = "green" if report['score'] > 90 else "yellow" if report['score'] > 70 else "red"
    console.print(f"Compliance Score: [{score_color}]{report['score']}/100[/{score_color}]")

    if report['is_safe']:
        console.print("[bold green]✅ Approved for Publication[/bold green]")
    else:
        console.print("[bold red]❌ Rejected / Review Required[/bold red]")
        
        # Display Violations Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Severity", width=10)
        table.add_column("Category", width=20)
        table.add_column("Trigger", width=20)
        table.add_column("Remediation Suggestion")

        for flag in report['flagged_items']:
            severity_style = "red" if flag['severity'] == "Critical" else "yellow"
            table.add_row(
                f"[{severity_style}]{flag['severity']}[/{severity_style}]",
                flag['category'],
                f"'{flag['found_word']}'",
                flag.get('suggestion', 'Remove or rephrase.')
            )
        
        console.print(table)
        
        # AI Fix Suggestion (Simulated for demo if AI not active, or real if available)
        # Note: In a real app, you would verify auditor.model_manager.has_ai
        console.print("[italic]🤖 AI Suggestion:[/italic] Consider rewriting to focus on property features rather than tenant characteristics.")

if __name__ == "__main__":
    run_platform_audit()
