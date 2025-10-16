#!/usr/bin/env python3
"""
Check current Notion database schema
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from notion_client import Client
import json

def check_notion_schema():
    """Display current Notion database schema"""
    print("\n" + "=" * 80)
    print("  CURRENT NOTION DATABASE SCHEMA")
    print("=" * 80 + "\n")

    notion_token = os.getenv('NOTION_TOKEN')
    notion_db_id = os.getenv('NOTION_DB_ID')

    if not notion_token or not notion_db_id:
        print("❌ NOTION_TOKEN or NOTION_DB_ID not found in .env")
        return

    print(f"📋 Database ID: {notion_db_id}")
    print()

    try:
        client = Client(auth=notion_token)

        # Get database info
        db = client.databases.retrieve(database_id=notion_db_id)

        print(f"📊 Database Title: {db.get('title', [{}])[0].get('plain_text', 'Untitled')}")
        print()

        # Get properties
        properties = db.get('properties', {})

        print(f"🏗️  Properties ({len(properties)} total):\n")

        for prop_name, prop_config in properties.items():
            prop_type = prop_config.get('type', 'unknown')
            prop_id = prop_config.get('id', 'N/A')

            print(f"  📌 {prop_name}")
            print(f"     Type: {prop_type}")
            print(f"     ID: {prop_id}")

            # Show additional config for specific types
            if prop_type == 'select':
                options = prop_config.get('select', {}).get('options', [])
                if options:
                    print(f"     Options: {[opt['name'] for opt in options]}")

            if prop_type == 'multi_select':
                options = prop_config.get('multi_select', {}).get('options', [])
                if options:
                    print(f"     Options: {[opt['name'] for opt in options]}")

            print()

        # Also show as JSON for reference
        print("─" * 80)
        print("\n📄 Full Schema (JSON):\n")
        print(json.dumps(properties, indent=2))

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_notion_schema()
