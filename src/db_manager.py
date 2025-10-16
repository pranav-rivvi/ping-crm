#!/usr/bin/env python3
"""
Database Manager for Ping CRM
Handles SQLite operations for user data
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import os


class DatabaseManager:
    """Manages SQLite database for user authentication and API keys"""

    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        if db_path is None:
            # Default to data directory
            db_dir = Path(__file__).parent.parent / 'data'
            db_dir.mkdir(exist_ok=True)
            db_path = db_dir / 'users.db'

        self.db_path = str(db_path)
        self.init_database()

    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                encrypted_apollo_key TEXT NOT NULL,
                encrypted_notion_token TEXT NOT NULL,
                encrypted_notion_db_id TEXT NOT NULL,
                encrypted_ai_key TEXT,
                ai_provider TEXT DEFAULT 'openai',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def user_exists(self, email: str) -> bool:
        """Check if user exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM users WHERE email = ?', (email.lower(),))
        result = cursor.fetchone()

        conn.close()
        return result is not None

    def create_user(self, email: str, password_hash: str,
                   encrypted_apollo: str, encrypted_notion_token: str,
                   encrypted_notion_db: str, encrypted_ai: str = None,
                   ai_provider: str = 'openai') -> bool:
        """Create new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO users (
                    email, password_hash,
                    encrypted_apollo_key, encrypted_notion_token,
                    encrypted_notion_db_id, encrypted_ai_key,
                    ai_provider
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                email.lower(), password_hash,
                encrypted_apollo, encrypted_notion_token,
                encrypted_notion_db, encrypted_ai,
                ai_provider
            ))

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError:
            # User already exists
            return False
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def get_user_by_email(self, email: str) -> dict:
        """Get user data by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, email, password_hash,
                   encrypted_apollo_key, encrypted_notion_token,
                   encrypted_notion_db_id, encrypted_ai_key,
                   ai_provider, created_at, last_login
            FROM users
            WHERE email = ?
        ''', (email.lower(),))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'id': result[0],
                'email': result[1],
                'password_hash': result[2],
                'encrypted_apollo_key': result[3],
                'encrypted_notion_token': result[4],
                'encrypted_notion_db_id': result[5],
                'encrypted_ai_key': result[6],
                'ai_provider': result[7],
                'created_at': result[8],
                'last_login': result[9]
            }
        return None

    def update_last_login(self, email: str):
        """Update user's last login timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE email = ?
        ''', (email.lower(),))

        conn.commit()
        conn.close()

    def update_user_keys(self, email: str,
                        encrypted_apollo: str = None,
                        encrypted_notion_token: str = None,
                        encrypted_notion_db: str = None,
                        encrypted_ai: str = None) -> bool:
        """Update user's encrypted API keys"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            updates = []
            params = []

            if encrypted_apollo:
                updates.append('encrypted_apollo_key = ?')
                params.append(encrypted_apollo)
            if encrypted_notion_token:
                updates.append('encrypted_notion_token = ?')
                params.append(encrypted_notion_token)
            if encrypted_notion_db:
                updates.append('encrypted_notion_db_id = ?')
                params.append(encrypted_notion_db)
            if encrypted_ai:
                updates.append('encrypted_ai_key = ?')
                params.append(encrypted_ai)

            if not updates:
                return False

            params.append(email.lower())
            query = f"UPDATE users SET {', '.join(updates)} WHERE email = ?"

            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error updating keys: {e}")
            return False

    def delete_user(self, email: str) -> bool:
        """Delete user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM users WHERE email = ?', (email.lower(),))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
