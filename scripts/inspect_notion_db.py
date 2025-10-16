#!/usr/bin/env python3
"""
Inspect Notion Database Schema
Shows actual database properties and compares with code expectations
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

from src.notion_sync import NotionClient

console = Console()


def main():
    """Inspect Notion database structure"""
    console.print(Panel.fit(
        "[bold blue]Notion Database Schema Inspector[/bold blue]\n"
        "Analyzing your database structure",
        border_style="blue"
    ))

    token = os.getenv('NOTION_TOKEN')
    db_id = os.getenv('NOTION_DB_ID')

    if not token or not db_id:
        console.print("[red]Error: Missing NOTION_TOKEN or NOTION_DB_ID in .env[/red]")
        return 1

    notion = NotionClient(token, db_id)

    # Fetch database schema
    try:
        db_info = notion.client.databases.retrieve(database_id=db_id)
        console.print(f"\n[green]✓ Database found: {db_info.get('title', [{}])[0].get('text', {}).get('content', 'Untitled')}[/green]\n")

        properties = db_info.get('properties', {})

        # Create table of existing properties
        table = Table(title="Existing Database Properties", show_header=True, header_style="bold cyan")
        table.add_column("Property Name", style="yellow", width=30)
        table.add_column("Type", style="green", width=15)
        table.add_column("Options (if select)", style="dim", width=40)

        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get('type', 'unknown')
            options = ""

            # Get select options if it's a select type
            if prop_type == 'select':
                select_options = prop_info.get('select', {}).get('options', [])
                options = ", ".join([opt.get('name', '') for opt in select_options])

            table.add_row(prop_name, prop_type, options)

        console.print(table)

        # Expected properties from our code
        expected_properties = {
            "Company Name": "title",
            "Status": "select",
            "Industry": "select",
            "Tier": "select",
            "Priority Score": "number",
            "Enrichment Date": "date",
            "Apollo ID": "rich_text",
            "Company Website": "url",
            "Company LinkedIn": "url",
            "Company Size": "select",
            "Location": "rich_text",
            "Revenue Range": "select",
            "Funding Stage": "select",
            "Primary Contact Name": "rich_text",
            "Primary Contact Title": "rich_text",
            "Primary Contact Email": "email",
            "Primary Contact LinkedIn": "url",
            "Secondary Contact Name": "rich_text",
            "Secondary Contact Title": "rich_text",
            "Secondary Contact Email": "email",
            "Tertiary Contact Name": "rich_text",
            "Tertiary Contact Title": "rich_text",
            "Tertiary Contact Email": "email"
        }

        # Compare expected vs actual
        console.print("\n[bold]Validation Results:[/bold]\n")

        missing_properties = []
        type_mismatches = []
        extra_properties = []

        # Check for missing properties
        for expected_name, expected_type in expected_properties.items():
            if expected_name not in properties:
                missing_properties.append((expected_name, expected_type))
            elif properties[expected_name].get('type') != expected_type:
                actual_type = properties[expected_name].get('type')
                type_mismatches.append((expected_name, expected_type, actual_type))

        # Check for extra properties (in DB but not in code)
        for prop_name in properties:
            if prop_name not in expected_properties:
                extra_properties.append((prop_name, properties[prop_name].get('type')))

        # Report findings
        if missing_properties:
            console.print("[yellow]⚠ Missing Properties (need to add to Notion):[/yellow]")
            for name, ptype in missing_properties:
                console.print(f"   - {name} ({ptype})")
            console.print()

        if type_mismatches:
            console.print("[red]✗ Type Mismatches:[/red]")
            for name, expected, actual in type_mismatches:
                console.print(f"   - {name}: expected {expected}, got {actual}")
            console.print()

        if extra_properties:
            console.print("[cyan]ℹ Extra Properties (in DB but not in code):[/cyan]")
            for name, ptype in extra_properties:
                console.print(f"   - {name} ({ptype})")
            console.print()

        if not missing_properties and not type_mismatches:
            console.print("[green]✓ All required properties exist with correct types![/green]\n")

            # Check select options for key fields
            console.print("[bold]Checking select field options:[/bold]\n")

            # Status options
            if 'Status' in properties:
                status_options = [opt.get('name') for opt in properties['Status'].get('select', {}).get('options', [])]
                console.print(f"Status options: {', '.join(status_options) if status_options else 'None'}")
                if 'Not Contacted' not in status_options:
                    console.print("[yellow]   ⚠ Missing 'Not Contacted' option (will be auto-created)[/yellow]")

            # Industry options
            if 'Industry' in properties:
                industry_options = [opt.get('name') for opt in properties['Industry'].get('select', {}).get('options', [])]
                console.print(f"Industry options: {', '.join(industry_options) if industry_options else 'None'}")
                expected_industries = ["Insurance / Payer", "Healthcare Provider / Health System", "Pharmacy / PBM", "Pharma / Biotech", "Other"]
                for exp in expected_industries:
                    if exp not in industry_options:
                        console.print(f"[yellow]   ⚠ Missing '{exp}' option (will be auto-created)[/yellow]")

            # Tier options
            if 'Tier' in properties:
                tier_options = [opt.get('name') for opt in properties['Tier'].get('select', {}).get('options', [])]
                console.print(f"Tier options: {', '.join(tier_options) if tier_options else 'None'}")
                expected_tiers = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]
                for exp in expected_tiers:
                    if exp not in tier_options:
                        console.print(f"[yellow]   ⚠ Missing '{exp}' option (will be auto-created)[/yellow]")

            console.print("\n[dim]Note: Missing select options will be auto-created by Notion API[/dim]")

        return 0 if not missing_properties and not type_mismatches else 1

    except Exception as e:
        console.print(f"[red]Error inspecting database: {e}[/red]")
        return 1


if __name__ == '__main__':
    sys.exit(main())
