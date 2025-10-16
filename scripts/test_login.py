#!/usr/bin/env python3
"""
Test login with credentials
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

def test_login(email, password):
    """Test login with given credentials"""
    print("\n" + "=" * 60)
    print("  Testing Login")
    print("=" * 60 + "\n")

    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)}\n")

    # Check if ENCRYPTION_KEY is loaded
    enc_key = os.getenv('ENCRYPTION_KEY')
    if enc_key:
        print(f"✅ ENCRYPTION_KEY loaded: {enc_key[:20]}...\n")
    else:
        print("❌ ENCRYPTION_KEY not found in environment!\n")
        return

    try:
        auth = AuthManager()
        print("🔐 Attempting login...\n")

        success, message, user_data = auth.login_user(email, password)

        if success:
            print(f"✅ {message}\n")
            print("🎉 Login successful!")
            print("\n📋 User Data:")
            print(f"  Email: {user_data['email']}")
            print(f"  AI Provider: {user_data['ai_provider']}")
            print(f"  Created: {user_data['created_at']}")
            print(f"  Last Login: {user_data['last_login']}")
            print("\n🔑 API Keys (decrypted):")
            print(f"  Apollo: {user_data['apollo_key'][:15]}...")
            print(f"  Notion: {user_data['notion_token'][:20]}...")
            print(f"  Notion DB: {user_data['notion_db_id']}")
            print(f"  AI Key: {user_data['ai_key'][:20]}...")
        else:
            print(f"❌ {message}")
            print("\n💡 Possible issues:")
            print("  1. Wrong password")
            print("  2. User doesn't exist")
            print("  3. Database corruption")

    except Exception as e:
        print(f"❌ Error during login: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with your credentials
    test_login("pranav@rivvi.ai", "admin123")
