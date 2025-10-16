#!/usr/bin/env python3
"""
Create admin user in database
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

def check_users():
    """List all users in database"""
    print("\n=== Current Database Users ===\n")

    db = DatabaseManager()

    # Direct SQL query to list all users
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT id, email, created_at, last_login FROM users')
    users = cursor.fetchall()

    if not users:
        print("No users found in database.\n")
    else:
        print(f"Found {len(users)} user(s):\n")
        for user in users:
            user_id, email, created_at, last_login = user
            print(f"  ID: {user_id}")
            print(f"  Email: {email}")
            print(f"  Created: {created_at}")
            print(f"  Last Login: {last_login}")
            print()

    conn.close()
    return len(users)

def create_admin():
    """Create admin user with keys from .env"""
    print("\n=== Creating Admin User ===\n")

    # Get keys from environment
    apollo_key = os.getenv('APOLLO_API_KEY')
    notion_token = os.getenv('NOTION_TOKEN')
    notion_db_id = os.getenv('NOTION_DB_ID')
    openai_key = os.getenv('OPENAI_API_KEY')

    if not all([apollo_key, notion_token, notion_db_id, openai_key]):
        print("❌ Error: Missing API keys in .env file")
        return False

    print("✅ API keys loaded from .env")
    print(f"  Apollo: {apollo_key[:10]}...")
    print(f"  Notion: {notion_token[:15]}...")
    print(f"  Notion DB: {notion_db_id}")
    print(f"  OpenAI: {openai_key[:15]}...\n")

    # Create admin user
    admin_email = "pranav@rivvi.ai"
    admin_password = "admin123"

    try:
        auth = AuthManager()

        # Check if user already exists
        db = DatabaseManager()
        if db.user_exists(admin_email):
            print(f"⚠️  User {admin_email} already exists!")
            print("   Use a different email or delete the existing user.\n")
            return False

        print("🔐 Registering user...")
        success, message = auth.register_user(
            email=admin_email,
            password=admin_password,
            apollo_key=apollo_key,
            notion_token=notion_token,
            notion_db_id=notion_db_id,
            ai_key=openai_key,
            ai_provider='openai'
        )

        if success:
            print(f"✅ {message}")
            print(f"\n🎉 Admin user created successfully!")
            print(f"\nLogin credentials:")
            print(f"  Email: {admin_email}")
            print(f"  Password: {admin_password}")
            print(f"\n🔒 All API keys have been encrypted and stored securely.")
            return True
        else:
            print(f"❌ {message}")
            return False

    except Exception as e:
        print(f"❌ Error creating user: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  HLTH 2025 CRM - Create Admin User")
    print("=" * 60)

    # Check existing users
    num_users = check_users()

    # Create admin if needed
    if input("\nCreate admin user? (y/n): ").lower() == 'y':
        create_admin()

        # Show updated user list
        print("\n" + "=" * 60)
        check_users()
