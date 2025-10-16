#!/usr/bin/env python3
"""Debug Apollo.io connection"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment
load_dotenv()

api_key = os.getenv('APOLLO_API_KEY')

print(f"API Key loaded: {api_key[:10]}... (length: {len(api_key)})")
print(f"\nTesting direct API call to Apollo.io...\n")

# Try direct API call without tenacity retry
endpoint = "https://api.apollo.io/v1/organizations/search"

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": api_key
}

payload = {
    "q_organization_name": "Microsoft",
    "page": 1,
    "per_page": 1
}

try:
    response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    if response.status_code == 200:
        data = response.json()
        if data.get('organizations'):
            print(f"\n✓ SUCCESS! Found: {data['organizations'][0].get('name')}")
        else:
            print(f"\n✗ API responded but no organizations found")
            print(f"Full response: {data}")
    elif response.status_code == 401:
        print("\n✗ AUTHENTICATION ERROR: Invalid API key")
        print("Please check your API key at: https://app.apollo.io/#/settings/integrations/api")
    elif response.status_code == 429:
        print("\n✗ RATE LIMIT: Too many requests")
        print("Wait a bit and try again")
    else:
        print(f"\n✗ ERROR: Unexpected status code")

except requests.exceptions.Timeout:
    print("\n✗ TIMEOUT: Request took too long")
    print("Check your internet connection")
except requests.exceptions.ConnectionError:
    print("\n✗ CONNECTION ERROR: Cannot reach Apollo.io")
    print("Check your internet connection")
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {str(e)}")
