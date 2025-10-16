#!/usr/bin/env python3
"""
Dynamic Company Enrichment
Supports multiple input methods: CSV, CLI arguments, or interactive mode
"""

import os
import sys
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.apollo_client import ApolloClient
from src.notion_sync_adapted import NotionClient
from src.processors import TierAssigner, PriorityScorer

# Load environment variables
load_dotenv()

console = Console()


def validate_config():
    """Validate that all required environment variables are set"""
    required = {
        'APOLLO_API_KEY': os.getenv('APOLLO_API_KEY'),
        'NOTION_TOKEN': os.getenv('NOTION_TOKEN'),
        'NOTION_DB_ID': os.getenv('NOTION_DB_ID')
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        console.print(f"\n[bold red]Error: Missing required environment variables:[/bold red]")
        for key in missing:
            console.print(f"  - {key}")
        console.print(f"\n[yellow]Please copy config/.env.example to .env and fill in your API keys[/yellow]\n")
        sys.exit(1)

    return required


def get_companies_from_csv(csv_file: str) -> list:
    """Load companies from CSV file"""
    try:
        df = pd.read_csv(csv_file)
        if 'company_name' not in df.columns:
            console.print("\n[bold red]Error: CSV must have 'company_name' column[/bold red]\n")
            return []

        return df['company_name'].dropna().tolist()
    except Exception as e:
        console.print(f"\n[bold red]Error reading CSV: {e}[/bold red]\n")
        return []


def get_companies_from_cli(args: list) -> list:
    """Get companies from command line arguments"""
    return args


def get_companies_interactive() -> list:
    """Interactive mode - ask user for companies"""
    console.print("\n[bold cyan]Interactive Mode[/bold cyan]")
    console.print("Enter company names (one per line)")
    console.print("Press Enter twice when done\n")

    companies = []
    while True:
        company = Prompt.ask("Company name", default="")
        if not company:
            if companies:
                break
            else:
                console.print("[yellow]Please enter at least one company[/yellow]")
                continue
        companies.append(company)

    return companies


def enrich_company(
    company_name: str,
    apollo: ApolloClient,
    notion: NotionClient,
    tier_assigner: TierAssigner,
    priority_scorer: PriorityScorer,
    skip_duplicates: bool = True
) -> dict:
    """
    Enrich a single company

    Args:
        company_name: Name of company to enrich
        apollo: Apollo API client
        notion: Notion API client
        tier_assigner: Tier assignment logic
        priority_scorer: Priority scoring logic
        skip_duplicates: Skip if already exists in Notion

    Returns:
        Result dict with status and details
    """
    result = {
        'company': company_name,
        'status': 'pending',
        'message': '',
        'priority': 0
    }

    try:
        # Check if exists
        if skip_duplicates and notion.page_exists(company_name):
            result['status'] = 'skipped'
            result['message'] = 'Already exists in Notion'
            return result

        # Search company in Apollo
        company_data = apollo.search_company(company_name)

        if not company_data:
            result['status'] = 'failed'
            result['message'] = 'Company not found in Apollo'
            return result

        # Get decision makers
        titles = apollo.get_target_titles(company_data.get('industry', ''))
        contacts = apollo.search_people(
            company_id=company_data['apollo_id'],
            titles=titles,
            max_results=10
        )

        # Assign tier and priority
        tier = tier_assigner.assign_tier(company_data)
        priority = priority_scorer.calculate_priority(company_data, contacts, tier)

        # Sync contacts to Notion (creates one page per contact)
        page_ids = notion.create_contact_pages(
            company_data=company_data,
            contacts=contacts,
            tier=tier,
            priority=priority
        )

        result['status'] = 'success'
        result['message'] = f'Added {len(page_ids)} contacts (Priority: {priority})'
        result['priority'] = priority
        result['contacts_found'] = len([c for c in contacts if c.get('email')])
        result['pages_created'] = len(page_ids)

    except Exception as e:
        result['status'] = 'failed'
        result['message'] = str(e)

    return result


def show_usage():
    """Show usage examples"""
    console.print(Panel.fit(
        "[bold blue]Dynamic Company Enrichment - Usage[/bold blue]\n\n"
        "[yellow]Method 1: From CSV file[/yellow]\n"
        "python scripts/enrich_dynamic.py companies.csv\n\n"
        "[yellow]Method 2: CLI arguments (dynamic list)[/yellow]\n"
        "python scripts/enrich_dynamic.py \"UnitedHealth Group\" \"CVS Health\" \"Anthem\"\n\n"
        "[yellow]Method 3: Interactive mode[/yellow]\n"
        "python scripts/enrich_dynamic.py\n"
        "(will prompt for company names)",
        border_style="blue"
    ))


def main():
    """Main enrichment flow with dynamic input"""
    console.print(Panel.fit(
        "[bold blue]HLTH 2025 CRM - Dynamic Enrichment[/bold blue]\n"
        "Flexible input: CSV, CLI arguments, or interactive",
        border_style="blue"
    ))

    # Validate configuration
    config = validate_config()

    # Determine input method
    companies = []

    if len(sys.argv) < 2:
        # No arguments - interactive mode
        companies = get_companies_interactive()

    elif sys.argv[1] in ['-h', '--help', 'help']:
        # Show help
        show_usage()
        return 0

    elif sys.argv[1].endswith('.csv'):
        # CSV file provided
        csv_file = sys.argv[1]
        if not os.path.exists(csv_file):
            console.print(f"\n[bold red]Error: File not found: {csv_file}[/bold red]\n")
            return 1
        companies = get_companies_from_csv(csv_file)
        if not companies:
            return 1

    else:
        # CLI arguments - treat all arguments as company names
        companies = get_companies_from_cli(sys.argv[1:])

    if not companies:
        console.print("\n[bold red]Error: No companies provided[/bold red]\n")
        show_usage()
        return 1

    # Show what we're going to process
    console.print(f"\n[bold green]Companies to enrich ({len(companies)}):[/bold green]")
    for i, company in enumerate(companies, 1):
        console.print(f"  {i}. {company}")

    # Confirm before proceeding
    console.print()
    if not Confirm.ask("Proceed with enrichment?", default=True):
        console.print("\n[yellow]Enrichment cancelled[/yellow]\n")
        return 0

    # Initialize clients
    apollo = ApolloClient(config['APOLLO_API_KEY'])
    notion = NotionClient(config['NOTION_TOKEN'], config['NOTION_DB_ID'])
    tier_assigner = TierAssigner()
    priority_scorer = PriorityScorer()

    # Results tracking
    results = {
        'success': 0,
        'failed': 0,
        'skipped': 0
    }

    details = []

    # Process companies with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:

        task = progress.add_task("[cyan]Enriching companies...", total=len(companies))

        for company_name in companies:
            progress.update(task, description=f"[cyan]Processing: {company_name[:40]}...")

            result = enrich_company(
                company_name=company_name,
                apollo=apollo,
                notion=notion,
                tier_assigner=tier_assigner,
                priority_scorer=priority_scorer,
                skip_duplicates=True
            )

            # Update stats
            results[result['status']] += 1
            details.append(result)

            # Rate limiting - be nice to APIs
            time.sleep(1.5)

            progress.update(task, advance=1)

    # Print results summary
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]Enrichment Complete![/bold green]",
        border_style="green"
    ))

    # Summary table
    table = Table(title="\nResults Summary", show_header=True, header_style="bold cyan")
    table.add_column("Status", style="cyan", width=15)
    table.add_column("Count", justify="right", style="magenta", width=10)

    table.add_row("✅ Success", str(results['success']))
    table.add_row("❌ Failed", str(results['failed']))
    table.add_row("⏭️  Skipped", str(results['skipped']))
    table.add_row("[bold]Total", f"[bold]{len(companies)}")

    console.print(table)

    # Details table for failed/skipped
    if results['failed'] > 0 or results['skipped'] > 0:
        console.print("\n")
        details_table = Table(title="Details", show_header=True, header_style="bold yellow")
        details_table.add_column("Company", style="white", width=30)
        details_table.add_column("Status", width=12)
        details_table.add_column("Message", width=40)

        for detail in details:
            if detail['status'] in ['failed', 'skipped']:
                status_style = "red" if detail['status'] == 'failed' else "yellow"
                details_table.add_row(
                    detail['company'][:30],
                    f"[{status_style}]{detail['status'].upper()}[/{status_style}]",
                    detail['message'][:40]
                )

        console.print(details_table)

    console.print("\n[bold green]Done! Check your Notion database for results.[/bold green]\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
