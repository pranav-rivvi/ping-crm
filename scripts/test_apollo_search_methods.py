#!/usr/bin/env python3
"""
Test different Apollo search methods for Sandeep Dadlani
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

from src.apollo_client import ApolloClient

console = Console()


def test_all_search_methods():
    """Try all possible search methods for Sandeep Dadlani"""

    api_key = os.getenv('APOLLO_API_KEY')
    apollo = ApolloClient(api_key)

    console.print("\n[bold cyan]Testing Multiple Search Methods for Sandeep Dadlani[/bold cyan]\n")

    # Method 1: Search by Name + Company
    console.print("[yellow]Method 1: Name + Company Search[/yellow]")
    try:
        person_data = apollo.search_person_by_name("Sandeep Dadlani", "UnitedHealth Group")
        if person_data:
            console.print(f"✅ Found: {person_data['name']} - {person_data.get('title', 'N/A')}")
            console.print(f"   LinkedIn: {person_data.get('linkedin_url', 'N/A')}")
            console.print(f"   Email: {person_data.get('email', 'N/A')}\n")
        else:
            console.print("❌ Not found\n")
    except Exception as e:
        console.print(f"❌ Error: {e}\n")

    # Method 2: Try enrichment endpoint with name + domain
    console.print("[yellow]Method 2: Enrichment API (name + domain)[/yellow]")
    try:
        endpoint = f"{apollo.BASE_URL}/people/match"
        payload = {
            "first_name": "Sandeep",
            "last_name": "Dadlani",
            "organization_name": "UnitedHealth Group"
        }

        console.print(f"Request: {json.dumps(payload, indent=2)}")

        response = apollo.session.post(endpoint, json=payload)
        console.print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('person'):
                person = data['person']
                console.print(f"✅ Found: {person.get('name')} - {person.get('title', 'N/A')}")
                console.print(f"   LinkedIn: {person.get('linkedin_url', 'N/A')}")
                console.print(f"   Email: {person.get('email', 'N/A')}\n")
            else:
                console.print("❌ No person in response\n")
                console.print(f"Response: {json.dumps(data, indent=2)}\n")
        else:
            console.print(f"❌ Error: {response.text}\n")

    except Exception as e:
        console.print(f"❌ Error: {e}\n")

    # Method 3: General keyword search
    console.print("[yellow]Method 3: Keyword Search (name only)[/yellow]")
    try:
        endpoint = f"{apollo.BASE_URL}/people/search"
        payload = {
            "q_keywords": "Sandeep Dadlani UnitedHealth",
            "page": 1,
            "per_page": 3
        }

        response = apollo.session.post(endpoint, json=payload)
        data = response.json()

        if data.get('people'):
            console.print(f"✅ Found {len(data['people'])} results:")
            for person in data['people']:
                console.print(f"  - {person.get('name')} at {person.get('organization', {}).get('name', 'Unknown')}")
                console.print(f"    LinkedIn: {person.get('linkedin_url', 'N/A')}")
            console.print()
        else:
            console.print("❌ No results\n")

    except Exception as e:
        console.print(f"❌ Error: {e}\n")

    # Method 4: Try with exact LinkedIn URL using match endpoint
    console.print("[yellow]Method 4: Match endpoint with LinkedIn URL (if supported)[/yellow]")
    try:
        endpoint = f"{apollo.BASE_URL}/people/match"
        payload = {
            "linkedin_url": "https://www.linkedin.com/in/sandeepdadlani/"
        }

        console.print(f"Request: {json.dumps(payload, indent=2)}")

        response = apollo.session.post(endpoint, json=payload)
        console.print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            console.print(f"Response keys: {list(data.keys())}")

            if data.get('person'):
                person = data['person']
                console.print(f"✅ Found: {person.get('name')} - {person.get('title', 'N/A')}")
                console.print(f"   LinkedIn: {person.get('linkedin_url', 'N/A')}")
                console.print(f"   Email: {person.get('email', 'N/A')}\n")
            else:
                console.print("❌ No person in response")
                console.print(f"Full response: {json.dumps(data, indent=2)}\n")
        else:
            console.print(f"❌ Error: {response.text}\n")

    except Exception as e:
        console.print(f"❌ Error: {e}\n")


if __name__ == '__main__':
    test_all_search_methods()
