#!/usr/bin/env python3
"""
Add Location Columns to Notion Database
Programmatically adds City, State, Country columns
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

from notion_client import Client

console = Console()


def add_location_columns():
    """Add City, State, Country columns to Notion database"""
    token = os.getenv('NOTION_TOKEN')
    db_id = os.getenv('NOTION_DB_ID')

    if not token or not db_id:
        console.print("[red]Error: Missing NOTION_TOKEN or NOTION_DB_ID[/red]")
        return 1

    client = Client(auth=token)

    console.print("[cyan]Adding location columns to Notion database...[/cyan]\n")

    try:
        # Update database schema to add new properties
        response = client.databases.update(
            database_id=db_id,
            properties={
                "City": {
                    "rich_text": {}
                },
                "State": {
                    "rich_text": {}
                },
                "Country": {
                    "rich_text": {}
                }
            }
        )

        console.print("[green]✓ Successfully added location columns![/green]\n")
        console.print("Added columns:")
        console.print("  • City (Text)")
        console.print("  • State (Text)")
        console.print("  • Country (Text)")
        console.print("\n[bold]Ready to enrich contacts with location data![/bold]")

        return 0

    except Exception as e:
        console.print(f"[red]✗ Error adding columns: {e}[/red]")
        return 1


if __name__ == '__main__':
    sys.exit(add_location_columns())
