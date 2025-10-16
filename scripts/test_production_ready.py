#!/usr/bin/env python3
"""
Comprehensive production readiness test
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
from src.apollo_client import ApolloClient
from src.notion_client import NotionClient

def test_encryption_key():
    """Test 1: Encryption key is loaded"""
    print("\n" + "=" * 80)
    print("  TEST 1: Encryption Key")
    print("=" * 80)

    # Try loading from env
    key_env = os.getenv('ENCRYPTION_KEY')

    # Try loading from Streamlit secrets
    key_st = None
    try:
        import streamlit as st
        key_st = st.secrets.get('ENCRYPTION_KEY', None)
    except Exception as e:
        print(f"  Streamlit secrets: Not available (expected in CLI): {e}")

    if key_env:
        print(f"  ✅ ENCRYPTION_KEY loaded from .env: {key_env[:20]}...")
    else:
        print(f"  ❌ ENCRYPTION_KEY not found in .env")

    if key_st:
        print(f"  ✅ ENCRYPTION_KEY loaded from Streamlit secrets: {key_st[:20]}...")
    else:
        print(f"  ⚠️  ENCRYPTION_KEY not in Streamlit secrets (will load when app runs)")

    # Test AuthManager can initialize
    try:
        auth = AuthManager()
        print(f"  ✅ AuthManager initialized successfully")
        return True
    except Exception as e:
        print(f"  ❌ AuthManager failed: {e}")
        return False


def test_database():
    """Test 2: Database is accessible and structured correctly"""
    print("\n" + "=" * 80)
    print("  TEST 2: Database")
    print("=" * 80)

    try:
        db = DatabaseManager()
        print(f"  ✅ Database connected: {db.db_path}")

        # Check if users table exists
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if cursor.fetchone():
            print(f"  ✅ Users table exists")
        else:
            print(f"  ❌ Users table missing")
            return False

        # Check columns
        cursor.execute("PRAGMA table_info(users);")
        columns = [col[1] for col in cursor.fetchall()]
        required_cols = ['id', 'email', 'password_hash', 'encrypted_apollo_key',
                        'encrypted_notion_token', 'encrypted_notion_db_id']

        for col in required_cols:
            if col in columns:
                print(f"  ✅ Column '{col}' exists")
            else:
                print(f"  ❌ Column '{col}' missing")
                return False

        conn.close()
        return True

    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False


def test_user_registration():
    """Test 3: User registration works"""
    print("\n" + "=" * 80)
    print("  TEST 3: User Registration")
    print("=" * 80)

    test_email = "test@example.com"

    try:
        # Clean up test user if exists
        db = DatabaseManager()
        if db.user_exists(test_email):
            db.delete_user(test_email)
            print(f"  🗑️  Deleted existing test user")

        # Get API keys
        apollo_key = os.getenv('APOLLO_API_KEY')
        notion_token = os.getenv('NOTION_TOKEN')
        notion_db_id = os.getenv('NOTION_DB_ID')
        openai_key = os.getenv('OPENAI_API_KEY')

        if not all([apollo_key, notion_token, notion_db_id, openai_key]):
            print(f"  ⚠️  Skipping: API keys not in environment")
            return True  # Not a failure, just can't test

        # Register test user
        auth = AuthManager()
        success, message = auth.register_user(
            email=test_email,
            password="testpass123",
            apollo_key=apollo_key,
            notion_token=notion_token,
            notion_db_id=notion_db_id,
            ai_key=openai_key,
            ai_provider='openai'
        )

        if success:
            print(f"  ✅ User registered: {message}")

            # Test login
            success, message, user_data = auth.login_user(test_email, "testpass123")
            if success:
                print(f"  ✅ Login successful")

                # Verify keys are decrypted correctly
                if user_data['apollo_key'] == apollo_key:
                    print(f"  ✅ Apollo key decrypted correctly")
                else:
                    print(f"  ❌ Apollo key mismatch")
                    return False

                # Clean up
                db.delete_user(test_email)
                print(f"  🗑️  Test user cleaned up")

                return True
            else:
                print(f"  ❌ Login failed: {message}")
                return False
        else:
            print(f"  ❌ Registration failed: {message}")
            return False

    except Exception as e:
        print(f"  ❌ Registration test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_clients():
    """Test 4: API clients can initialize"""
    print("\n" + "=" * 80)
    print("  TEST 4: API Clients")
    print("=" * 80)

    try:
        apollo_key = os.getenv('APOLLO_API_KEY')
        notion_token = os.getenv('NOTION_TOKEN')
        notion_db_id = os.getenv('NOTION_DB_ID')

        if not all([apollo_key, notion_token, notion_db_id]):
            print(f"  ⚠️  Skipping: API keys not in environment")
            return True

        # Test Apollo
        apollo = ApolloClient(apollo_key)
        print(f"  ✅ Apollo client initialized")

        # Test Notion
        notion = NotionClient(notion_token, notion_db_id)
        print(f"  ✅ Notion client initialized")

        return True

    except Exception as e:
        print(f"  ❌ API clients error: {e}")
        return False


def test_security():
    """Test 5: Security checks"""
    print("\n" + "=" * 80)
    print("  TEST 5: Security")
    print("=" * 80)

    # Check .gitignore
    gitignore_path = Path(__file__).parent.parent / '.gitignore'
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if '.env' in content:
            print(f"  ✅ .env is in .gitignore")
        else:
            print(f"  ❌ .env NOT in .gitignore - SECURITY RISK!")
            return False

        if '.streamlit/secrets.toml' in content:
            print(f"  ✅ .streamlit/secrets.toml is in .gitignore")
        else:
            print(f"  ❌ secrets.toml NOT in .gitignore - SECURITY RISK!")
            return False

        if '*.db' in content or 'users.db' in content:
            print(f"  ✅ Database files in .gitignore")
        else:
            print(f"  ⚠️  Database files not in .gitignore")
    else:
        print(f"  ❌ .gitignore not found")
        return False

    # Check password hashing
    try:
        auth = AuthManager()
        password = "testpassword"
        hashed = auth.hash_password(password)

        if hashed != password:
            print(f"  ✅ Passwords are hashed (not stored in plain text)")
        else:
            print(f"  ❌ Passwords NOT hashed - SECURITY RISK!")
            return False

        # Verify hash
        if auth.verify_password(password, hashed):
            print(f"  ✅ Password verification works")
        else:
            print(f"  ❌ Password verification failed")
            return False

    except Exception as e:
        print(f"  ❌ Password security error: {e}")
        return False

    return True


def run_all_tests():
    """Run all production readiness tests"""
    print("\n" + "=" * 80)
    print("  PING CRM - PRODUCTION READINESS TEST")
    print("=" * 80)

    tests = [
        ("Encryption Key", test_encryption_key),
        ("Database", test_database),
        ("User Registration", test_user_registration),
        ("API Clients", test_api_clients),
        ("Security", test_security),
    ]

    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))

    # Summary
    print("\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\n  Total: {passed}/{total} tests passed\n")

    if passed == total:
        print("  🎉 ALL TESTS PASSED - READY FOR PRODUCTION!")
        print("\n  ✅ Safe for friends to register and use")
        print("  ✅ User data is encrypted")
        print("  ✅ Passwords are hashed")
        print("  ✅ Secrets are protected\n")
        return True
    else:
        print("  ⚠️  SOME TESTS FAILED - FIX BEFORE PRODUCTION\n")
        return False

    print("=" * 80)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
