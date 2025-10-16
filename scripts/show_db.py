#!/usr/bin/env python3
"""
Display database structure and data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db_manager import DatabaseManager
import sqlite3

def show_database():
    """Display database structure and all data"""
    print("\n" + "=" * 80)
    print("  DATABASE STRUCTURE & DATA")
    print("=" * 80 + "\n")

    db = DatabaseManager()
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()

    print(f"📁 Database Location: {db.db_path}")
    print()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print(f"📊 Tables: {len(tables)}\n")

    for table in tables:
        table_name = table[0]
        print("─" * 80)
        print(f"📋 Table: {table_name}")
        print("─" * 80)

        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        print("\n  Columns:")
        for col in columns:
            col_id, name, col_type, not_null, default, pk = col
            pk_marker = " [PRIMARY KEY]" if pk else ""
            null_marker = " NOT NULL" if not_null else ""
            print(f"    • {name}: {col_type}{pk_marker}{null_marker}")

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"\n  Total Rows: {count}")

        # Show data
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Get column names
            col_names = [desc[1] for desc in columns]

            print("\n  Data:")
            for idx, row in enumerate(rows, 1):
                print(f"\n    Row {idx}:")
                for col_name, value in zip(col_names, row):
                    # Mask sensitive data
                    if 'password' in col_name.lower() or 'encrypted' in col_name.lower():
                        display_value = value[:20] + "..." if value and len(str(value)) > 20 else value
                    else:
                        display_value = value

                    print(f"      {col_name}: {display_value}")

        print()

    # Database file size
    import os
    db_size = os.path.getsize(db.db_path)
    if db_size < 1024:
        size_str = f"{db_size} bytes"
    elif db_size < 1024 * 1024:
        size_str = f"{db_size / 1024:.2f} KB"
    else:
        size_str = f"{db_size / (1024 * 1024):.2f} MB"

    print("─" * 80)
    print(f"💾 Database Size: {size_str}")
    print("=" * 80)

    conn.close()

if __name__ == "__main__":
    show_database()
