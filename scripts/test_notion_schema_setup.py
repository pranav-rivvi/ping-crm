#!/usr/bin/env python3
"""
Test Notion database schema auto-setup
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from src.notion_schema import NotionSchemaManager


def test_schema_setup():
    """Test schema validation and auto-setup"""
    print("\n" + "=" * 80)
    print("  NOTION SCHEMA AUTO-SETUP TEST")
    print("=" * 80)

    notion_token = os.getenv('NOTION_TOKEN')
    notion_db_id = os.getenv('NOTION_DB_ID')

    if not notion_token or not notion_db_id:
        print("❌ NOTION_TOKEN or NOTION_DB_ID not found in .env")
        return False

    print(f"\n📋 Database ID: {notion_db_id}")
    print()

    try:
        # Initialize schema manager
        schema_manager = NotionSchemaManager(notion_token, notion_db_id)

        # Step 1: Check if database exists
        print("Step 1: Checking database exists...")
        exists, exist_msg = schema_manager.check_database_exists()
        if exists:
            print(f"  ✅ {exist_msg}")
        else:
            print(f"  ❌ {exist_msg}")
            return False

        # Step 2: Get current schema
        print("\nStep 2: Getting current schema...")
        current_props = schema_manager.get_current_schema()
        print(f"  ✅ Found {len(current_props)} existing properties")

        # Step 3: Validate schema
        print("\nStep 3: Validating schema...")
        is_valid, validation_msg, missing = schema_manager.validate_schema()

        if is_valid:
            print(f"  ✅ {validation_msg}")
        else:
            print(f"  ⚠️  {validation_msg}")
            print(f"  📝 Missing properties: {', '.join(missing)}")

        # Step 4: Setup schema (add missing properties)
        print("\nStep 4: Setting up schema (adding missing properties)...")
        success, setup_msg, added = schema_manager.setup_schema(include_optional=True)

        if success:
            print(f"  ✅ {setup_msg}")
            if added:
                print(f"  📝 Added properties:")
                for prop in added:
                    print(f"     • {prop}")
            else:
                print(f"  ℹ️  No properties needed to be added")
        else:
            print(f"  ❌ {setup_msg}")
            return False

        # Step 5: Generate full schema report
        print("\nStep 5: Generating schema report...")
        report = schema_manager.get_schema_report()
        print(report)

        # Step 6: Validate again to confirm all properties are present
        print("\nStep 6: Final validation...")
        is_valid, validation_msg, missing = schema_manager.validate_schema()

        if is_valid:
            print(f"  ✅ {validation_msg}")
            print("\n" + "=" * 80)
            print("  🎉 ALL TESTS PASSED - SCHEMA IS READY!")
            print("=" * 80)
            return True
        else:
            print(f"  ❌ {validation_msg}")
            print(f"  ⚠️  Still missing: {', '.join(missing)}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_schema_setup()
    sys.exit(0 if success else 1)
