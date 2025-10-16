#!/usr/bin/env python3
"""
Test Apollo People Search Filters
Explore what filters are available for targeting people
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

from src.apollo_client import ApolloClient

console = Console()


def test_people_search_filters():
    """Test Apollo people search with various filters"""

    api_key = os.getenv('APOLLO_API_KEY')
    apollo = ApolloClient(api_key)

    # First, get a company to test with
    console.print("\n[cyan]Step 1: Getting company ID for testing[/cyan]\n")
    company_data = apollo.search_company("UnitedHealth Group")

    if not company_data:
        console.print("[red]Could not find test company[/red]")
        return 1

    company_id = company_data['apollo_id']
    console.print(f"Company: {company_data['name']}")
    console.print(f"Apollo ID: {company_id}\n")

    # Test 1: Basic search with titles
    console.print("[yellow]Test 1: Basic title search[/yellow]")
    endpoint = f"{apollo.BASE_URL}/people/search"

    payload = {
        "organization_ids": [company_id],
        "person_titles": ["CEO", "CTO", "VP"],
        "page": 1,
        "per_page": 5
    }

    console.print(f"Request: {json.dumps(payload, indent=2)}")

    response = apollo.session.post(endpoint, json=payload)
    data = response.json()

    console.print(f"Results found: {len(data.get('people', []))}\n")

    # Test 2: Add location filter
    console.print("[yellow]Test 2: Title + Location filter[/yellow]")

    payload_with_location = {
        "organization_ids": [company_id],
        "person_titles": ["CEO", "CTO", "VP", "Director"],
        "person_locations": ["Minnesota", "New York"],  # Try location filter
        "page": 1,
        "per_page": 10
    }

    console.print(f"Request: {json.dumps(payload_with_location, indent=2)}")

    response = apollo.session.post(endpoint, json=payload_with_location)
    data = response.json()

    console.print(f"Results found: {len(data.get('people', []))}")

    if data.get('people'):
        for person in data['people'][:3]:
            console.print(f"  - {person.get('name')} | {person.get('title')} | {person.get('city')}, {person.get('state')}")
    console.print()

    # Test 3: Seniority filter
    console.print("[yellow]Test 3: Seniority filter[/yellow]")

    payload_seniority = {
        "organization_ids": [company_id],
        "person_seniorities": ["c_suite", "vp", "director"],  # Try seniority levels
        "page": 1,
        "per_page": 10
    }

    console.print(f"Request: {json.dumps(payload_seniority, indent=2)}")

    response = apollo.session.post(endpoint, json=payload_seniority)
    data = response.json()

    console.print(f"Results found: {len(data.get('people', []))}")

    if data.get('people'):
        for person in data['people'][:3]:
            console.print(f"  - {person.get('name')} | {person.get('title')} | Seniority: {person.get('seniority')}")
    console.print()

    # Test 4: Combined filters
    console.print("[yellow]Test 4: Combined (titles + location + seniority)[/yellow]")

    payload_combined = {
        "organization_ids": [company_id],
        "person_titles": ["VP", "Vice President", "Director"],
        "person_locations": ["United States"],
        "person_seniorities": ["vp", "director"],
        "page": 1,
        "per_page": 10
    }

    console.print(f"Request: {json.dumps(payload_combined, indent=2)}")

    response = apollo.session.post(endpoint, json=payload_combined)
    data = response.json()

    console.print(f"Results found: {len(data.get('people', []))}")

    if data.get('people'):
        table = Table(title="Sample Results")
        table.add_column("Name", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Location", style="yellow")
        table.add_column("Seniority", style="green")

        for person in data['people'][:5]:
            location = f"{person.get('city', '')}, {person.get('state', '')}"
            table.add_row(
                person.get('name', 'N/A'),
                person.get('title', 'N/A'),
                location.strip(', '),
                person.get('seniority', 'N/A')
            )

        console.print(table)

    console.print("\n[green]✓ Apollo supports these filters:[/green]")
    console.print("  • organization_ids (required)")
    console.print("  • person_titles (list of job titles)")
    console.print("  • person_locations (list of locations)")
    console.print("  • person_seniorities (c_suite, vp, director, etc.)")
    console.print("  • per_page (max results)")

    return 0


if __name__ == '__main__':
    sys.exit(test_people_search_filters())
