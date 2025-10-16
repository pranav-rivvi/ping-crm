#!/usr/bin/env python3
"""
Test Single Company Enrichment
Verifies the adapted code works with existing Notion database
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
from src.notion_sync_adapted import NotionClient
from src.processors import TierAssigner, PriorityScorer

console = Console()


def test_enrichment(test_company: str = "Microsoft"):
    """Test enrichment with a sample company"""
    console.print(Panel.fit(
        f"[bold blue]Testing Company Enrichment[/bold blue]\n"
        f"Test company: {test_company}",
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
        notion = NotionClient(token, db_id)
        tier_assigner = TierAssigner()
        priority_scorer = PriorityScorer()
        console.print("   ✓ Clients initialized")

        # Search company
        console.print(f"\n[cyan]2. Searching for '{test_company}' in Apollo...[/cyan]")
        company_data = apollo.search_company(test_company)

        if not company_data:
            console.print("[red]   ✗ Company not found[/red]")
            return 1

        console.print(f"   ✓ Found: {company_data['name']}")
        console.print(f"   - Industry: {company_data.get('industry', 'Unknown')}")
        console.print(f"   - Employees: {company_data.get('employee_count', 0)}")
        console.print(f"   - Location: {company_data.get('location', 'Unknown')}")

        # Get contacts
        console.print(f"\n[cyan]3. Finding decision makers...[/cyan]")
        titles = apollo.get_target_titles(company_data.get('industry', ''))
        console.print(f"   - Searching for: {', '.join(titles[:3])}...")

        contacts = apollo.search_people(
            company_id=company_data['apollo_id'],
            titles=titles,
            max_results=5  # Limit for testing
        )

        console.print(f"   ✓ Found {len(contacts)} contacts")

        # Show contact preview
        if contacts:
            table = Table(title="Contacts Found", show_header=True, header_style="bold cyan")
            table.add_column("Name", style="yellow", width=25)
            table.add_column("Title", style="green", width=30)
            table.add_column("Email", style="cyan", width=25)

            for contact in contacts[:3]:  # Show first 3
                table.add_row(
                    contact.get('name', 'Unknown')[:25],
                    contact.get('title', 'N/A')[:30],
                    contact.get('email', 'N/A')[:25] if contact.get('email') else "❌ No email"
                )

            console.print(table)

        # Calculate tier and priority
        console.print(f"\n[cyan]4. Calculating tier and priority...[/cyan]")
        tier = tier_assigner.assign_tier(company_data)
        priority = priority_scorer.calculate_priority(company_data, contacts, tier)

        console.print(f"   ✓ Tier: {tier}")
        console.print(f"   ✓ Priority Score: {priority}/10")

        # Ask before syncing
        console.print(f"\n[yellow]Ready to sync {len(contacts)} contacts to Notion database[/yellow]")
        response = input("Proceed with sync? (yes/no): ").strip().lower()

        if response not in ['yes', 'y']:
            console.print("\n[yellow]Sync cancelled by user[/yellow]")
            return 0

        # Sync to Notion
        console.print(f"\n[cyan]5. Syncing to Notion...[/cyan]")
        page_ids = notion.create_contact_pages(
            company_data=company_data,
            contacts=contacts,
            tier=tier,
            priority=priority
        )

        console.print(f"   ✓ Created {len(page_ids)} pages in Notion")

        # Success summary
        console.print("\n" + "=" * 60)
        console.print(Panel.fit(
            f"[bold green]✓ Test Successful![/bold green]\n\n"
            f"Company: {company_data['name']}\n"
            f"Contacts Added: {len(page_ids)}\n"
            f"Tier: {tier}\n"
            f"Priority: {priority}/10\n\n"
            f"[dim]Check your Notion database to see the results[/dim]",
            border_style="green"
        ))

        return 0

    except Exception as e:
        console.print(f"\n[red]✗ Error during enrichment: {e}[/red]")
        import traceback
        console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        return 1


if __name__ == '__main__':
    # Use command line argument if provided, otherwise default to Microsoft
    test_company = sys.argv[1] if len(sys.argv) > 1 else "Microsoft"
    sys.exit(test_enrichment(test_company))
