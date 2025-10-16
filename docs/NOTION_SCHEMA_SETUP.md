# Notion Database Auto-Setup

## Overview

Ping CRM automatically validates and sets up your Notion database schema when you register. This ensures your database has all the required properties for contact enrichment to work seamlessly.

## What Happens During Registration

When you register with your Notion credentials, the system:

1. **Validates Access** - Confirms your Notion token and database ID are correct
2. **Checks Schema** - Examines your current database properties
3. **Auto-Adds Missing Properties** - Creates any missing required or optional fields
4. **Confirms Setup** - Shows you exactly what was validated and added

## Required Properties

These properties are **essential** for Ping CRM to function:

| Property | Type | Description |
|----------|------|-------------|
| Contact Name | Title | Contact name (primary field) |
| Email | Email | Contact email address |
| Phone | Phone Number | Contact phone number |
| Company | Rich Text | Company name |
| Title | Rich Text | Job title |
| LinkedIn | URL | LinkedIn profile URL |
| City | Rich Text | City |
| State | Rich Text | State/Province |
| Country | Rich Text | Country |

## Optional Properties

These properties are **recommended** but not required:

| Property | Type | Description |
|----------|------|-------------|
| Seniority | Select | Seniority level (C-Suite, VP, Director, Manager, IC) |
| Industry | Select | Company industry (Healthcare Tech, Pharma, Insurance, etc.) |
| Outreach Context | Rich Text | AI-generated outreach context |
| Company Size | Rich Text | Number of employees |
| Company Website | URL | Company website |
| Notes | Rich Text | Additional notes |

## Manual Setup (If Needed)

If you prefer to set up your Notion database manually before registering:

### Step 1: Create a Notion Database

1. Go to Notion and create a new database (table view)
2. Name it something like "CRM Contacts" or "HLTH Conference Tracker"

### Step 2: Add Properties

Add the properties listed above with the correct types:

- **Title** type for "Contact Name"
- **Email** type for "Email"
- **Phone** type for "Phone"
- **Rich Text** for text fields (Company, Title, City, State, Country, Notes, etc.)
- **URL** type for LinkedIn and Company Website
- **Select** type for Seniority and Industry (add the options listed above)

### Step 3: Share with Integration

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Copy the integration token (starts with `secret_`)
3. Open your database in Notion
4. Click "..." → "Add connections" → Select your integration

### Step 4: Get Database ID

From your database URL:
```
https://notion.so/workspace/DATABASE_ID?v=...
                          ^^^^^^^^^^^ (copy this part)
```

## Testing Schema Setup

You can test the schema setup independently:

```bash
# Test with your credentials
python scripts/test_notion_schema_setup.py

# This will:
# 1. Check database exists
# 2. Validate current schema
# 3. Add missing properties
# 4. Generate a report
```

## Checking Current Schema

To see what's currently in your Notion database:

```bash
python scripts/check_notion_schema.py
```

This shows:
- All property names
- Their types
- Options (for Select/Multi-select fields)
- Full JSON schema

## Troubleshooting

### "Database not found"
- Check your database ID is correct
- Ensure you've shared the database with your integration

### "Access denied"
- Verify your integration token is correct
- Make sure the integration has access to the database (use "Add connections")

### "Type mismatch"
If a property exists but has the wrong type, you'll need to:
1. Rename or delete the existing property in Notion
2. Re-run registration or the schema setup script

### "Schema setup failed"
- Check your integration has edit permissions
- Ensure the database isn't locked or archived
- Try the test script to see detailed error messages

## Benefits of Auto-Setup

✅ **No manual configuration** - Just provide your credentials, we handle the rest

✅ **Prevents errors** - Ensures all required fields exist before enrichment

✅ **Consistent schema** - All users have the same field structure

✅ **Upgradeable** - When we add new features, we can auto-add new properties

✅ **Safe** - Never deletes or modifies existing data, only adds missing properties

## Schema Manager API

For developers extending Ping CRM:

```python
from src.notion_schema import NotionSchemaManager

# Initialize
schema_manager = NotionSchemaManager(notion_token, database_id)

# Check if database exists
exists, message = schema_manager.check_database_exists()

# Validate schema
is_valid, message, missing_props = schema_manager.validate_schema()

# Setup schema (add missing properties)
success, message, added_props = schema_manager.setup_schema(include_optional=True)

# Get schema report
report = schema_manager.get_schema_report()
print(report)
```

## Related Files

- `src/notion_schema.py` - Schema manager implementation
- `scripts/test_notion_schema_setup.py` - Test script
- `scripts/check_notion_schema.py` - Schema inspection script
- `src/auth_manager.py` - Integrated into registration validation

## Questions?

If you encounter issues with schema setup:

1. Run the test script: `python scripts/test_notion_schema_setup.py`
2. Check the detailed error messages
3. Verify your Notion integration has proper permissions
4. Open an issue on GitHub with the error details
