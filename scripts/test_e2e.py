#!/usr/bin/env python3
"""
End-to-End Test
Tests the complete flow: Person + Company → Apollo → Notion

This will ACTUALLY write to your Notion database!
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

from src.apollo_client import ApolloClient
from src.notion_client import NotionClient

console = Console()


def test_single_person(person_name: str, company_name: str):
    """
    Test enrichment with a single person

    Args:
        person_name: Full name (e.g., "Bruce Broussard")
        company_name: Company name (e.g., "Humana")
    """
    console.print(Panel.fit(
        f"[bold blue]End-to-End Enrichment Test[/bold blue]\n\n"
        f"Person: {person_name}\n"
        f"Company: {company_name}\n\n"
        f"[yellow]⚠️  This will WRITE to your Notion database![/yellow]",
        border_style="blue"
    ))

    # Check environment
    api_key = os.getenv('APOLLO_API_KEY')
    token = os.getenv('NOTION_TOKEN')
    db_id = os.getenv('NOTION_DB_ID')

    if not all([api_key, token, db_id]):
        console.print("[red]Error: Missing environment variables[/red]")
        return 1

    try:
        # Step 1: Initialize clients
        console.print("\n[cyan]Step 1: Initializing clients...[/cyan]")
        apollo = ApolloClient(api_key)
        notion = NotionClient(token, db_id)
        console.print("   ✓ Clients ready")

        # Step 2: Search Apollo for person
        console.print(f"\n[cyan]Step 2: Searching Apollo for '{person_name}' at '{company_name}'...[/cyan]")

        # Get company data
        company_data = apollo.search_company(company_name)
        if not company_data:
            console.print(f"   [red]✗ Company not found[/red]")
            return 1

        console.print(f"   ✓ Found company: {company_data['name']}")
        console.print(f"     • Industry: {company_data.get('industry', 'N/A')}")
        console.print(f"     • Size: {company_data.get('employee_count', 0):,} employees")
        console.print(f"     • Location: {company_data.get('location', 'N/A')}")

        # Search for person
        person_data = apollo.search_person_by_name(person_name, company_name)
        if not person_data:
            console.print(f"   [red]✗ Person not found in Apollo[/red]")
            return 1

        console.print(f"   ✓ Found person: {person_data['name']}")

        # Show enriched data
        table = Table(title="\nEnriched Data from Apollo", show_header=True, header_style="bold green")
        table.add_column("Field", style="cyan", width=20)
        table.add_column("Value", style="green", width=50)

        table.add_row("Name", person_data.get('name', 'N/A'))
        table.add_row("Title", person_data.get('title', 'N/A'))
        table.add_row("Email", person_data.get('email', 'N/A'))
        table.add_row("Phone", person_data.get('phone', 'N/A'))
        linkedin_url = person_data.get('linkedin_url', 'N/A')
        linkedin_display = (linkedin_url[:50] + "...") if linkedin_url and linkedin_url != 'N/A' else 'N/A'
        table.add_row("LinkedIn", linkedin_display)
        table.add_row("Seniority", person_data.get('seniority', 'N/A'))
        table.add_row("State", person_data.get('state', 'N/A'))

        console.print(table)

        # Step 3: Check if exists in Notion
        console.print(f"\n[cyan]Step 3: Checking if contact exists in Notion...[/cyan]")
        existing_page = notion.find_contact(person_name, company_name)

        if existing_page:
            console.print(f"   ✓ Found existing contact (will update)")
            action = "update"
        else:
            console.print(f"   • Contact not found (will create new)")
            action = "create"

        # Step 4: Confirm before writing
        console.print(f"\n[yellow]Ready to {action} contact in Notion[/yellow]")
        response = input(f"Proceed with {action}? (yes/no): ").strip().lower()

        if response not in ['yes', 'y']:
            console.print("\n[yellow]Test cancelled[/yellow]")
            return 0

        # Step 5: Write to Notion
        console.print(f"\n[cyan]Step 4: Writing to Notion...[/cyan]")
        success, action_taken = notion.upsert_contact(
            contact_name=person_data['name'],
            company_name=company_data['name'],
            enriched_data=person_data,
            company_data=company_data
        )

        if success:
            console.print(f"   ✓ Successfully {action_taken} contact in Notion!")

            # Success summary
            console.print("\n" + "=" * 70)
            console.print(Panel.fit(
                f"[bold green]✓ End-to-End Test PASSED![/bold green]\n\n"
                f"Contact: {person_data['name']}\n"
                f"Company: {company_data['name']}\n"
                f"Action: {action_taken.upper()}\n\n"
                f"[bold]What was written to Notion:[/bold]\n"
                f"  • Contact Name: {person_data['name']}\n"
                f"  • Company: {company_data['name']}\n"
                f"  • Title: {person_data.get('title', 'N/A')}\n"
                f"  • Email: {person_data.get('email', 'N/A')}\n"
                f"  • LinkedIn: {person_data.get('linkedin_url', 'N/A')[:40]}...\n"
                f"  • Notes: Company info + enrichment data\n\n"
                f"[dim]Check your Notion database now to see the result![/dim]",
                border_style="green"
            ))
            return 0
        else:
            console.print(f"   [red]✗ Failed to {action} contact[/red]")
            return 1

    except Exception as e:
        console.print(f"\n[red]✗ Test failed with error: {e}[/red]")
        import traceback
        console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        return 1


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        console.print(Panel.fit(
            "[bold red]Error: Missing arguments[/bold red]\n\n"
            "[yellow]Usage:[/yellow]\n"
            'python scripts/test_e2e.py "Person Name" "Company Name"\n\n'
            "[yellow]Examples:[/yellow]\n"
            'python scripts/test_e2e.py "Bruce Broussard" "Humana"\n'
            'python scripts/test_e2e.py "Andrew Witty" "UnitedHealth Group"\n\n'
            "[red]Note: This will write to your Notion database![/red]",
            border_style="red"
        ))
        return 1

    person_name = sys.argv[1]
    company_name = sys.argv[2]

    return test_single_person(person_name, company_name)


if __name__ == '__main__':
    sys.exit(main())