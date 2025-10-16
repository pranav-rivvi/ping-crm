#!/usr/bin/env python3
"""
Delete and recreate admin user
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from src.auth_manager import AuthManager
from src.db_manager import DatabaseManager

def reset_admin():
    """Delete existing user and create new one"""
    print("\n" + "=" * 60)
    print("  Resetting Admin User")
    print("=" * 60 + "\n")

    email = "pranav@rivvi.ai"
    password = "admin123"

    db = DatabaseManager()

    # Delete existing user
    if db.user_exists(email):
        print(f"🗑️  Deleting existing user: {email}")
        db.delete_user(email)
        print("✅ User deleted\n")

    # Get API keys from .env
    apollo_key = os.getenv('APOLLO_API_KEY')
    notion_token = os.getenv('NOTION_TOKEN')
    notion_db_id = os.getenv('NOTION_DB_ID')
    openai_key = os.getenv('OPENAI_API_KEY')

    print("📋 Creating new admin user:")
    print(f"  Email: {email}")
    print(f"  Password: {password}\n")

    # Create user
    auth = AuthManager()
    success, message = auth.register_user(
        email=email,
        password=password,
        apollo_key=apollo_key,
        notion_token=notion_token,
        notion_db_id=notion_db_id,
        ai_key=openai_key,
        ai_provider='openai'
    )

    if success:
        print(f"✅ {message}\n")
        print("🎉 Admin user created successfully!")
        print(f"\n🔐 Login credentials:")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"\n✅ You can now login at: http://localhost:8506")
    else:
        print(f"❌ {message}")

if __name__ == "__main__":
    reset_admin()
