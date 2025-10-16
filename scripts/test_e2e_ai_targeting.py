#!/usr/bin/env python3
"""
End-to-End Test: AI Company Targeting → Notion
Tests the complete workflow from user goal to Notion database
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
import pandas as pd

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from src.apollo_client import ApolloClient
from src.notion_client import NotionClient
from src.llm_helper import AITargeting

console = Console()


def test_e2e_workflow():
    """Test complete AI targeting workflow"""

    console.print("\n[bold cyan]🧪 End-to-End Test: AI Company Targeting[/bold cyan]\n")

    # Step 1: Initialize clients
    console.print("[yellow]Step 1:[/yellow] Initializing Apollo, Notion, and AI...")

    try:
        # Load API keys from environment
        apollo_key = os.getenv('APOLLO_API_KEY')
        notion_token = os.getenv('NOTION_TOKEN')
        notion_db_id = os.getenv('NOTION_DB_ID')

        if not apollo_key:
            console.print(f"[red]❌ APOLLO_API_KEY not found in .env[/red]")
            return 1
        if not notion_token or not notion_db_id:
            console.print(f"[red]❌ Notion credentials not found in .env[/red]")
            return 1

        apollo = ApolloClient(apollo_key)
        notion = NotionClient(notion_token, notion_db_id)
        ai = AITargeting()

        provider = ai.get_provider_info()
        console.print(f"[green]✓ Apollo client ready[/green]")
        console.print(f"[green]✓ Notion client ready[/green]")
        console.print(f"[green]✓ AI ready ({provider['provider']}: {provider['model']})[/green]\n")
    except Exception as e:
        console.print(f"[red]❌ Failed to initialize: {e}[/red]")
        return 1

    # Step 2: Load test companies
    console.print("[yellow]Step 2:[/yellow] Loading test companies...")

    csv_path = Path(__file__).parent.parent / "test_companies.csv"
    if not csv_path.exists():
        console.print(f"[red]❌ test_companies.csv not found at {csv_path}[/red]")
        return 1

    df = pd.read_csv(csv_path)
    console.print(f"[green]✓ Loaded {len(df)} companies: {', '.join(df['company_name'].tolist())}[/green]\n")

    # Step 3: Generate AI strategy from user goal
    console.print("[yellow]Step 3:[/yellow] Analyzing user goal with AI...")

    user_goal = "I want to connect with C-suite executives and VPs for HLTH 2025 conference partnership discussions"
    console.print(f"[cyan]User Goal:[/cyan] \"{user_goal}\"\n")

    try:
        strategy = ai.analyze_targeting_request(user_goal, "Healthcare")

        console.print(f"[green]✓ AI Strategy:[/green] {strategy['explanation']}\n")

        console.print("[cyan]Job Titles:[/cyan]")
        for title in strategy['titles'][:8]:
            console.print(f"  • {title}")
        if len(strategy['titles']) > 8:
            console.print(f"  • ... and {len(strategy['titles']) - 8} more")

        console.print(f"\n[cyan]Seniorities:[/cyan] {', '.join(strategy['seniorities'])}")
        if strategy.get('locations'):
            console.print(f"[cyan]Locations:[/cyan] {', '.join(strategy['locations'])}")

        console.print()

    except Exception as e:
        console.print(f"[red]❌ AI strategy failed: {e}[/red]")
        return 1

    # Step 4: Process each company
    console.print("[yellow]Step 4:[/yellow] Finding people at target companies...\n")

    all_results = []
    company_cache = {}  # Cache company data for later use

    for idx, row in df.iterrows():
        company_name = row['company_name']
        console.print(f"[bold]Processing: {company_name}[/bold]")

        # Search company
        try:
            company_data = apollo.search_company(company_name)
            if not company_data:
                console.print(f"  [red]❌ Company not found[/red]\n")
                continue

            # Cache company data
            company_cache[company_name] = company_data

            console.print(f"  [green]✓ Found:[/green] {company_data['name']}")
            console.print(f"    Domain: {company_data.get('domain', 'N/A')}")
            console.print(f"    Industry: {company_data.get('industry', 'N/A')}")

        except Exception as e:
            console.print(f"  [red]❌ Error: {e}[/red]\n")
            continue

        # Search people with AI strategy
        try:
            people = apollo.search_people_by_company(
                company_id=company_data['apollo_id'],
                titles=strategy['titles'],
                seniorities=strategy['seniorities'],
                locations=strategy.get('locations'),
                max_results=5
            )

            console.print(f"  [green]✓ Found {len(people)} people[/green]\n")

            if people:
                # Show first 3 as preview
                for i, person in enumerate(people[:3], 1):
                    console.print(f"    {i}. {person['name']} - {person['title']}")
                if len(people) > 3:
                    console.print(f"    ... and {len(people) - 3} more")
                console.print()

            all_results.extend([(company_name, person) for person in people])

        except Exception as e:
            console.print(f"  [red]❌ Error searching people: {e}[/red]\n")
            continue

    if not all_results:
        console.print("[red]❌ No people found[/red]")
        return 1

    console.print(f"[green]✓ Total people found: {len(all_results)}[/green]\n")

    # Step 5: Add to Notion
    console.print("[yellow]Step 5:[/yellow] Adding contacts to Notion...\n")

    added_count = 0
    skipped_count = 0
    error_count = 0

    for company_name, person in all_results:
        try:
            # Check if contact already exists
            existing = notion.find_contact(person['name'], company_name)

            if existing:
                console.print(f"  [yellow]⊘ Skipped:[/yellow] {person['name']} (already exists)")
                skipped_count += 1
            else:
                # Get cached company data
                company_data = company_cache.get(company_name)

                success, action = notion.upsert_contact(
                    contact_name=person['name'],
                    company_name=company_name,
                    enriched_data=person,
                    company_data=company_data
                )

                if success:
                    console.print(f"  [green]✓ Added:[/green] {person['name']} - {person['title']}")
                    added_count += 1
                else:
                    console.print(f"  [red]❌ Failed to add:[/red] {person['name']}")
                    error_count += 1

        except Exception as e:
            console.print(f"  [red]❌ Error:[/red] {person['name']} - {e}")
            error_count += 1

    # Step 6: Summary
    console.print("\n" + "="*60)
    console.print("[bold green]✓ End-to-End Test Complete![/bold green]\n")

    # Results table
    table = Table(title="Test Results Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="white", justify="right")

    table.add_row("Companies processed", str(len(df)))
    table.add_row("People found", str(len(all_results)))
    table.add_row("Added to Notion", str(added_count), style="green")
    table.add_row("Skipped (duplicates)", str(skipped_count), style="yellow")
    table.add_row("Errors", str(error_count), style="red")

    console.print(table)
    console.print()

    # Verification steps
    console.print("[cyan]✅ Verification Steps:[/cyan]")
    console.print(f"  1. Open your Notion database: https://notion.so/{os.getenv('NOTION_DB_ID')}")
    console.print(f"  2. Look for {added_count} new contacts from {', '.join(df['company_name'].tolist())}")
    console.print("  3. Verify all fields are populated (name, title, email, LinkedIn, location)")
    console.print("  4. Try running this test again - should skip all as duplicates\n")

    return 0


if __name__ == '__main__':
    sys.exit(test_e2e_workflow())
