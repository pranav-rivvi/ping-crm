#!/usr/bin/env python3
"""
Enrich Existing Contact in Notion
Updates an existing Notion contact with Apollo data
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
from src.notion_sync_updater import NotionUpdater

console = Console()


def enrich_contact(person_name: str, company_name: str, dry_run: bool = False):
    """
    Enrich existing contact in Notion with Apollo data

    Args:
        person_name: Full name of person
        company_name: Company name
        dry_run: If True, show what would be updated without actually updating
    """
    console.print(Panel.fit(
        f"[bold blue]Enrich Existing Contact[/bold blue]\n\n"
        f"Person: {person_name}\n"
        f"Company: {company_name}\n"
        f"Mode: {'DRY RUN (preview only)' if dry_run else 'LIVE UPDATE'}",
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
        # Initialize clients
        console.print("\n[cyan]1. Initializing clients...[/cyan]")
        apollo = ApolloClient(api_key)
        notion = NotionUpdater(token, db_id)
        console.print("   ✓ Clients initialized")

        # Find existing contact in Notion
        console.print(f"\n[cyan]2. Finding '{person_name}' at '{company_name}' in your Notion database...[/cyan]")
        existing_page = notion.find_contact(person_name, company_name)

        if not existing_page:
            console.print(f"   [red]✗ Contact not found in Notion database[/red]")
            console.print(f"\n[yellow]Tip: Make sure the contact exists in your database with:")
            console.print(f"  - Contact Name: {person_name}")
            console.print(f"  - Company: {company_name}[/yellow]")
            return 1

        console.print(f"   ✓ Found contact in Notion (Page ID: {existing_page['id'][:8]}...)")

        # Show current data
        current_props = existing_page['properties']
        console.print("\n   Current data in Notion:")

        current_email = current_props.get('Email', {}).get('email')
        current_title = current_props.get('Title', {}).get('rich_text', [{}])[0].get('text', {}).get('content') if current_props.get('Title', {}).get('rich_text') else None
        current_linkedin = current_props.get('LinkedIn', {}).get('url')
        current_phone = current_props.get('Phone', {}).get('phone_number')

        console.print(f"     • Email: {current_email or '[dim]missing[/dim]'}")
        console.print(f"     • Title: {current_title or '[dim]missing[/dim]'}")
        console.print(f"     • LinkedIn: {current_linkedin or '[dim]missing[/dim]'}")
        console.print(f"     • Phone: {current_phone or '[dim]missing[/dim]'}")

        # Search Apollo for person
        console.print(f"\n[cyan]3. Searching Apollo for '{person_name}' at '{company_name}'...[/cyan]")

        # Get company data first
        company_data = apollo.search_company(company_name)
        if not company_data:
            console.print(f"   [red]✗ Company '{company_name}' not found in Apollo[/red]")
            return 1

        console.print(f"   ✓ Found company: {company_data['name']}")

        # Search for person
        person_data = apollo.search_person_by_name(person_name, company_name)

        if not person_data:
            console.print(f"   [red]✗ Person not found in Apollo[/red]")
            console.print(f"\n[yellow]Note: This could mean:")
            console.print(f"  - Person doesn't exist in Apollo database")
            console.print(f"  - Name spelling is different")
            console.print(f"  - Person is at a different company[/yellow]")
            return 1

        console.print(f"   ✓ Found person: {person_data['name']}")

        # Show enriched data
        table = Table(title="\nEnriched Data from Apollo", show_header=True, header_style="bold green")
        table.add_column("Field", style="cyan", width=20)
        table.add_column("Current (Notion)", style="yellow", width=30)
        table.add_column("New (Apollo)", style="green", width=30)

        table.add_row(
            "Email",
            current_email or "missing",
            person_data.get('email', 'N/A')
        )
        table.add_row(
            "Title",
            current_title or "missing",
            person_data.get('title', 'N/A')
        )
        table.add_row(
            "LinkedIn",
            current_linkedin or "missing",
            person_data.get('linkedin_url', 'N/A')
        )
        table.add_row(
            "Phone",
            current_phone or "missing",
            person_data.get('phone', 'N/A')
        )
        table.add_row(
            "Seniority",
            "-",
            person_data.get('seniority', 'N/A')
        )

        console.print(table)

        # Show company data that will be added to notes
        console.print("\n[bold]Company info (will be added to Notes):[/bold]")
        console.print(f"  • Website: {company_data.get('domain', 'N/A')}")
        console.print(f"  • Size: {company_data.get('employee_count', 'N/A'):,} employees")
        console.print(f"  • Location: {company_data.get('location', 'N/A')}")
        console.print(f"  • Revenue: {company_data.get('revenue_range', 'N/A')}")
        console.print(f"  • Industry: {company_data.get('industry', 'N/A')}")

        if dry_run:
            console.print("\n[yellow]DRY RUN - No changes made to Notion[/yellow]")
            return 0

        # Confirm update
        console.print(f"\n[yellow]Ready to update Notion with Apollo data[/yellow]")
        response = input("Proceed with update? (yes/no): ").strip().lower()

        if response not in ['yes', 'y']:
            console.print("\n[yellow]Update cancelled[/yellow]")
            return 0

        # Update Notion
        console.print(f"\n[cyan]4. Updating Notion page...[/cyan]")
        success = notion.enrich_contact(
            page_id=existing_page['id'],
            enriched_data=person_data,
            company_data=company_data
        )

        if success:
            console.print("   ✓ Successfully updated Notion!")
            console.print("\n" + "=" * 60)
            console.print(Panel.fit(
                f"[bold green]✓ Enrichment Complete![/bold green]\n\n"
                f"Contact: {person_data['name']}\n"
                f"Company: {company_data['name']}\n"
                f"Updated: Email, Title, LinkedIn, Phone, Notes\n\n"
                f"[dim]Check your Notion database to see the results[/dim]",
                border_style="green"
            ))
            return 0
        else:
            console.print("   [red]✗ Failed to update Notion[/red]")
            return 1

    except Exception as e:
        console.print(f"\n[red]✗ Error during enrichment: {e}[/red]")
        import traceback
        console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        return 1


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        console.print(Panel.fit(
            "[bold red]Error: Missing arguments[/bold red]\n\n"
            "[yellow]Usage:[/yellow]\n"
            'python scripts/enrich_existing_contact.py "Person Name" "Company Name"\n\n'
            "[yellow]Examples:[/yellow]\n"
            'python scripts/enrich_existing_contact.py "John Smith" "Humana"\n'
            'python scripts/enrich_existing_contact.py "Sarah Johnson" "UnitedHealth Group"\n\n'
            "[yellow]Add --dry-run to preview without updating:[/yellow]\n"
            'python scripts/enrich_existing_contact.py "John Smith" "Humana" --dry-run',
            border_style="red"
        ))
        return 1

    person_name = sys.argv[1]
    company_name = sys.argv[2]
    dry_run = '--dry-run' in sys.argv

    return enrich_contact(person_name, company_name, dry_run)


if __name__ == '__main__':
    sys.exit(main())
