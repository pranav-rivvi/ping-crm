#!/usr/bin/env python3
"""
Check Apollo Fields
See what location/state data Apollo returns for contacts
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich import print_json
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

from src.apollo_client import ApolloClient

console = Console()


def check_fields(company_name: str = "Humana"):
    """Check what fields Apollo returns"""
    console.print(f"[cyan]Checking Apollo fields for company: {company_name}[/cyan]\n")

    api_key = os.getenv('APOLLO_API_KEY')
    apollo = ApolloClient(api_key)

    # Get company
    company = apollo.search_company(company_name)
    console.print(f"[green]Company found: {company['name']}[/green]\n")

    # Get a contact
    endpoint = f"{apollo.BASE_URL}/people/search"
    payload = {
        "organization_ids": [company['apollo_id']],
        "per_page": 1
    }

    response = apollo.session.post(endpoint, json=payload)
    data = response.json()

    if data.get('people'):
        person = data['people'][0]

        console.print("[bold yellow]Raw Apollo Person Data:[/bold yellow]\n")

        # Print all fields
        console.print(f"[cyan]Basic Info:[/cyan]")
        console.print(f"  name: {person.get('name')}")
        console.print(f"  first_name: {person.get('first_name')}")
        console.print(f"  last_name: {person.get('last_name')}")
        console.print(f"  title: {person.get('title')}")

        console.print(f"\n[cyan]Contact Info:[/cyan]")
        console.print(f"  email: {person.get('email')}")
        console.print(f"  phone: {person.get('phone')}")
        console.print(f"  linkedin_url: {person.get('linkedin_url')}")

        console.print(f"\n[cyan]Location Data:[/cyan]")
        console.print(f"  city: {person.get('city')}")
        console.print(f"  state: {person.get('state')}")
        console.print(f"  country: {person.get('country')}")

        console.print(f"\n[cyan]Other Fields:[/cyan]")
        console.print(f"  seniority: {person.get('seniority')}")
        console.print(f"  departments: {person.get('departments')}")
        console.print(f"  functions: {person.get('functions')}")

        console.print(f"\n[bold green]Full JSON:[/bold green]")
        print_json(json.dumps(person, indent=2))


if __name__ == '__main__':
    company = sys.argv[1] if len(sys.argv) > 1 else "Humana"
    check_fields(company)
