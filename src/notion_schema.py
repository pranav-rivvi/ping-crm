#!/usr/bin/env python3
"""
Notion Database Schema Management
Automatically validates and sets up Notion database schema
"""

from notion_client import Client
from typing import Tuple, List, Dict


# Required schema for Ping CRM
REQUIRED_SCHEMA = {
    'Contact Name': {
        'type': 'title',
        'description': 'Contact name (required)',
    },
    'Email': {
        'type': 'email',
        'description': 'Contact email address',
    },
    'Phone': {
        'type': 'phone_number',
        'description': 'Contact phone number',
    },
    'Company': {
        'type': 'rich_text',
        'description': 'Company name',
    },
    'Title': {
        'type': 'rich_text',
        'description': 'Job title',
    },
    'LinkedIn': {
        'type': 'url',
        'description': 'LinkedIn profile URL',
    },
    'City': {
        'type': 'rich_text',
        'description': 'City',
    },
    'State': {
        'type': 'rich_text',
        'description': 'State/Province',
    },
    'Country': {
        'type': 'rich_text',
        'description': 'Country',
    },
}

# Optional but recommended properties
OPTIONAL_SCHEMA = {
    'Seniority': {
        'type': 'select',
        'description': 'Seniority level',
        'options': [
            {'name': 'C-Suite', 'color': 'red'},
            {'name': 'VP', 'color': 'orange'},
            {'name': 'Director', 'color': 'yellow'},
            {'name': 'Manager', 'color': 'green'},
            {'name': 'Individual Contributor', 'color': 'blue'},
        ]
    },
    'Industry': {
        'type': 'select',
        'description': 'Company industry',
        'options': [
            {'name': 'Healthcare Tech', 'color': 'blue'},
            {'name': 'Pharma', 'color': 'purple'},
            {'name': 'Insurance', 'color': 'green'},
            {'name': 'Hospital & Health Systems', 'color': 'red'},
            {'name': 'Biotech', 'color': 'pink'},
            {'name': 'Medical Devices', 'color': 'orange'},
            {'name': 'Digital Health', 'color': 'blue'},
            {'name': 'Telehealth', 'color': 'green'},
            {'name': 'Health Services', 'color': 'yellow'},
        ]
    },
    'Outreach Context': {
        'type': 'rich_text',
        'description': 'AI-generated outreach context',
    },
    'Company Size': {
        'type': 'rich_text',
        'description': 'Number of employees',
    },
    'Company Website': {
        'type': 'url',
        'description': 'Company website',
    },
    'Notes': {
        'type': 'rich_text',
        'description': 'Additional notes',
    },
}


class NotionSchemaManager:
    """Manages Notion database schema validation and setup"""

    def __init__(self, notion_token: str, database_id: str):
        """Initialize schema manager"""
        self.client = Client(auth=notion_token)
        self.database_id = database_id

    def check_database_exists(self) -> Tuple[bool, str]:
        """Check if database exists and is accessible"""
        try:
            db = self.client.databases.retrieve(database_id=self.database_id)
            title = db.get('title', [{}])[0].get('plain_text', 'Untitled')
            return True, f"Database found: {title}"
        except Exception as e:
            error_msg = str(e)
            if 'object_not_found' in error_msg.lower():
                return False, "Database not found - check your database ID"
            elif 'unauthorized' in error_msg.lower():
                return False, "Access denied - make sure you've shared the database with your integration"
            else:
                return False, f"Error accessing database: {error_msg}"

    def get_current_schema(self) -> Dict:
        """Get current database properties"""
        try:
            db = self.client.databases.retrieve(database_id=self.database_id)
            return db.get('properties', {})
        except Exception as e:
            return {}

    def validate_schema(self) -> Tuple[bool, str, List[str]]:
        """
        Validate database schema against required properties

        Returns:
            (is_valid, message, missing_properties)
        """
        current_props = self.get_current_schema()

        if not current_props:
            return False, "Could not read database schema", []

        # Check for required properties
        missing = []
        mismatched = []

        for prop_name, prop_config in REQUIRED_SCHEMA.items():
            if prop_name not in current_props:
                missing.append(prop_name)
            else:
                # Check if type matches
                current_type = current_props[prop_name].get('type')
                required_type = prop_config['type']

                if current_type != required_type:
                    mismatched.append(
                        f"{prop_name} (expected {required_type}, found {current_type})"
                    )

        if missing or mismatched:
            issues = []
            if missing:
                issues.append(f"Missing properties: {', '.join(missing)}")
            if mismatched:
                issues.append(f"Type mismatches: {', '.join(mismatched)}")

            return False, "; ".join(issues), missing
        else:
            return True, "Schema valid - all required properties present", []

    def add_property(self, prop_name: str, prop_config: Dict) -> Tuple[bool, str]:
        """Add a single property to the database"""
        try:
            prop_type = prop_config['type']
            description = prop_config.get('description', '')

            # Build property configuration
            new_prop = {
                'type': prop_type,
            }

            # Add type-specific configuration
            if prop_type == 'select':
                new_prop['select'] = {
                    'options': prop_config.get('options', [])
                }
            elif prop_type == 'multi_select':
                new_prop['multi_select'] = {
                    'options': prop_config.get('options', [])
                }
            else:
                # For most types (rich_text, email, url, etc.), just the type is enough
                new_prop[prop_type] = {}

            # Add description if provided
            if description:
                new_prop['description'] = description

            # Update database
            self.client.databases.update(
                database_id=self.database_id,
                properties={
                    prop_name: new_prop
                }
            )

            return True, f"Added property: {prop_name}"

        except Exception as e:
            return False, f"Failed to add {prop_name}: {str(e)}"

    def setup_schema(self, include_optional: bool = True) -> Tuple[bool, str, List[str]]:
        """
        Setup database schema by adding missing properties

        Args:
            include_optional: Also add recommended optional properties

        Returns:
            (success, message, added_properties)
        """
        # Check if database exists first
        exists, msg = self.check_database_exists()
        if not exists:
            return False, msg, []

        # Get current schema
        current_props = self.get_current_schema()
        added = []
        failed = []

        # Add required properties
        for prop_name, prop_config in REQUIRED_SCHEMA.items():
            if prop_name not in current_props:
                success, msg = self.add_property(prop_name, prop_config)
                if success:
                    added.append(prop_name)
                else:
                    failed.append(msg)

        # Add optional properties if requested
        if include_optional:
            for prop_name, prop_config in OPTIONAL_SCHEMA.items():
                if prop_name not in current_props:
                    success, msg = self.add_property(prop_name, prop_config)
                    if success:
                        added.append(prop_name)
                    # Don't fail on optional properties

        if failed:
            return False, f"Setup incomplete: {'; '.join(failed)}", added

        if added:
            return True, f"Schema setup complete! Added {len(added)} properties", added
        else:
            return True, "Schema already complete - no changes needed", []

    def get_schema_report(self) -> str:
        """Generate a human-readable schema report"""
        exists, msg = self.check_database_exists()

        if not exists:
            return f"❌ {msg}"

        current_props = self.get_current_schema()
        is_valid, validation_msg, missing = self.validate_schema()

        report = []
        report.append("\n📊 Database Schema Report\n")

        # Required properties
        report.append("Required Properties:")
        for prop_name in REQUIRED_SCHEMA.keys():
            if prop_name in current_props:
                prop_type = current_props[prop_name].get('type', 'unknown')
                report.append(f"  ✅ {prop_name} ({prop_type})")
            else:
                report.append(f"  ❌ {prop_name} (missing)")

        # Optional properties
        report.append("\nRecommended Properties:")
        for prop_name in OPTIONAL_SCHEMA.keys():
            if prop_name in current_props:
                prop_type = current_props[prop_name].get('type', 'unknown')
                report.append(f"  ✅ {prop_name} ({prop_type})")
            else:
                report.append(f"  ⚠️  {prop_name} (optional, not added)")

        report.append(f"\n{validation_msg}")

        return "\n".join(report)
