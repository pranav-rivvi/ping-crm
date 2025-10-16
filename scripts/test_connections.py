#!/usr/bin/env python3
"""
API Connection Test Script
Tests actual connections to Apollo.io and Notion APIs
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

console = Console()


def test_apollo_connection():
    """Test Apollo.io API connection"""
    try:
        from src.apollo_client import ApolloClient

        api_key = os.getenv('APOLLO_API_KEY')
        if not api_key:
            return False, "API key not found in .env"

        apollo = ApolloClient(api_key)

        # Try a simple company search
        console.print("\n[cyan]Testing Apollo.io connection...[/cyan]")
        result = apollo.search_company("Microsoft")

        if result and result.get('name'):
            return True, f"✓ Connected! Found: {result['name']}"
        else:
            return False, "API responded but no data returned"

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            return False, "✗ Invalid API key"
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            return False, "✗ Rate limit exceeded"
        else:
            return False, f"✗ Error: {error_msg[:50]}"


def test_notion_connection():
    """Test Notion API connection"""
    try:
        from src.notion_sync import NotionClient

        token = os.getenv('NOTION_TOKEN')
        db_id = os.getenv('NOTION_DB_ID')

        if not token:
            return False, "Token not found in .env"
        if not db_id:
            return False, "Database ID not found in .env"

        notion = NotionClient(token, db_id)

        # Try to check if a test company exists
        console.print("[cyan]Testing Notion connection...[/cyan]")
        exists = notion.page_exists("__TEST_CONNECTION__")

        # If we get here without error, connection works
        return True, "✓ Connected! Database accessible"

    except Exception as e:
        error_msg = str(e)
        if "unauthorized" in error_msg.lower():
            return False, "✗ Invalid integration token"
        elif "object not found" in error_msg.lower():
            return False, "✗ Database ID not found or integration not connected"
        elif "restricted" in error_msg.lower():
            return False, "✗ Integration not connected to database"
        else:
            return False, f"✗ Error: {error_msg[:50]}"


def main():
    """Run connection tests"""
    console.print(Panel.fit(
        "[bold blue]HLTH 2025 CRM - Connection Test[/bold blue]\n"
        "Testing API connections to Apollo.io and Notion",
        border_style="blue"
    ))

    # Test Apollo
    console.print("\n[bold]1. Apollo.io API[/bold]")
    apollo_ok, apollo_msg = test_apollo_connection()

    if apollo_ok:
        console.print(f"   [green]{apollo_msg}[/green]")
    else:
        console.print(f"   [red]{apollo_msg}[/red]")

    # Test Notion
    console.print("\n[bold]2. Notion API[/bold]")
    notion_ok, notion_msg = test_notion_connection()

    if notion_ok:
        console.print(f"   [green]{notion_msg}[/green]")
    else:
        console.print(f"   [red]{notion_msg}[/red]")

    # Summary
    console.print("\n" + "="*60)

    if apollo_ok and notion_ok:
        console.print(Panel.fit(
            "[bold green]✓ All connections successful![/bold green]\n\n"
            "You're ready to enrich companies!\n\n"
            "Next steps:\n"
            "1. Create companies.csv with your company list\n"
            "2. Run: python scripts/enrich.py companies.csv",
            border_style="green"
        ))
        return 0
    else:
        console.print(Panel.fit(
            "[bold red]✗ Some connections failed[/bold red]\n\n"
            "Please fix the issues above before proceeding.\n\n"
            "Common fixes:\n"
            "- Apollo: Check API key at https://app.apollo.io/#/settings/integrations/api\n"
            "- Notion: Ensure integration is connected to your database",
            border_style="red"
        ))

        # Detailed troubleshooting
        if not apollo_ok:
            console.print("\n[yellow]Apollo.io Troubleshooting:[/yellow]")
            console.print("1. Verify API key: https://app.apollo.io/#/settings/integrations/api")
            console.print("2. Make sure you copied the entire key")
            console.print("3. Check if you have credits remaining")

        if not notion_ok:
            console.print("\n[yellow]Notion Troubleshooting:[/yellow]")
            console.print("1. Verify integration token: https://www.notion.so/my-integrations")
            console.print("2. Check Database ID (32 characters from URL)")
            console.print("3. Connect integration to database:")
            console.print("   → Open database → ... → Connections → Connect 'HLTH 2025 CRM'")

        return 1


if __name__ == '__main__':
    sys.exit(main())
