#!/usr/bin/env python3
"""
Test LinkedIn URL Search
Debug why wrong person is being returned
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from src.apollo_client import ApolloClient

console = Console()


def test_linkedin_search():
    """Test LinkedIn URL search with Sandeep Dadlani"""

    api_key = os.getenv('APOLLO_API_KEY')
    if not api_key:
        console.print("[red]Error: APOLLO_API_KEY not found[/red]")
        return 1

    apollo = ApolloClient(api_key)

    # Test URL
    test_url = "https://www.linkedin.com/in/sandeepdadlani/"

    console.print(f"\n[cyan]Testing LinkedIn Search[/cyan]")
    console.print(f"URL: {test_url}\n")

    try:
        # Make raw API call to see exact response
        import requests

        endpoint = f"{apollo.BASE_URL}/people/search"

        payload = {
            "linkedin_url": test_url,
            "page": 1,
            "per_page": 3  # Get top 3 to see if there are multiple results
        }

        console.print("[yellow]Raw API Request:[/yellow]")
        console.print(json.dumps(payload, indent=2))

        response = apollo.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        console.print(f"\n[yellow]API Response:[/yellow]")
        console.print(f"Total results: {len(data.get('people', []))}")

        if data.get('people'):
            console.print("\n[cyan]Results:[/cyan]\n")

            for idx, person in enumerate(data['people'], 1):
                console.print(f"[bold]Result {idx}:[/bold]")
                console.print(f"  Name: {person.get('name')}")
                console.print(f"  Title: {person.get('title')}")
                console.print(f"  LinkedIn: {person.get('linkedin_url')}")
                console.print(f"  Email: {person.get('email')}")

                org = person.get('organization', {})
                if org:
                    console.print(f"  Company: {org.get('name')}")

                console.print()

            # Now test through our client
            console.print("[cyan]Testing through ApolloClient:[/cyan]\n")
            person_data, company_data = apollo.search_by_linkedin_url(test_url)

            if person_data:
                table = Table(title="Returned Contact")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Name", person_data.get('name', 'N/A'))
                table.add_row("Title", person_data.get('title', 'N/A'))
                table.add_row("LinkedIn", person_data.get('linkedin_url', 'N/A'))
                table.add_row("Email", person_data.get('email', 'N/A'))

                if company_data:
                    table.add_row("Company", company_data.get('name', 'N/A'))

                console.print(table)
            else:
                console.print("[red]No person data returned[/red]")

        else:
            console.print("[red]No results found[/red]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()

    return 0


if __name__ == '__main__':
    sys.exit(test_linkedin_search())
