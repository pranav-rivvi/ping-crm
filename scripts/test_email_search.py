#!/usr/bin/env python3
"""
Test Email Search in Apollo
Quick verification that email-based enrichment works
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from src.apollo_client import ApolloClient

console = Console()


def test_email_search():
    """Test searching Apollo by email"""

    # Initialize Apollo client
    api_key = os.getenv('APOLLO_API_KEY')
    if not api_key:
        console.print("[red]Error: APOLLO_API_KEY not found[/red]")
        return 1

    apollo = ApolloClient(api_key)

    # Test emails (these are public executives)
    test_emails = [
        "tim@apple.com",  # Tim Cook (Apple CEO) - may or may not be in Apollo
        # You can add real emails you want to test
    ]

    console.print("\n[cyan]Testing Apollo Email Search[/cyan]\n")

    for email in test_emails:
        console.print(f"[yellow]Searching for: {email}[/yellow]")

        try:
            person_data, company_data = apollo.search_by_email(email)

            if person_data:
                console.print(f"[green]✓ Found: {person_data['name']}[/green]")

                # Show details
                table = Table(title=f"Contact Details for {email}")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Name", person_data.get('name', 'N/A'))
                table.add_row("Title", person_data.get('title', 'N/A'))
                table.add_row("Email", person_data.get('email', 'N/A'))
                table.add_row("Phone", person_data.get('phone', 'N/A'))
                table.add_row("LinkedIn", person_data.get('linkedin_url', 'N/A'))
                table.add_row("City", person_data.get('city', 'N/A'))
                table.add_row("State", person_data.get('state', 'N/A'))
                table.add_row("Country", person_data.get('country', 'N/A'))

                if company_data:
                    table.add_row("Company", company_data.get('name', 'N/A'))
                    table.add_row("Industry", company_data.get('industry', 'N/A'))
                    table.add_row("Employees", f"{company_data.get('employee_count', 0):,}")

                console.print(table)
                console.print()
            else:
                console.print(f"[red]✗ Not found in Apollo database[/red]\n")

        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]\n")

    console.print("\n[bold green]Email search is working![/bold green]")
    console.print("\n[cyan]You can now:[/cyan]")
    console.print("  1. Use the Streamlit UI 'LinkedIn/Email Lookup' tab")
    console.print("  2. Create bulk email enrichment CSV with 'email' column")
    console.print("  3. Add emails to sample_contacts.csv")

    return 0


if __name__ == '__main__':
    sys.exit(test_email_search())
