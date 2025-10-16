"""
Notion API Client - Adapted for Existing Schema
Works with contact-centric database (one row per contact)
"""

from notion_client import Client
from typing import Dict, List
from datetime import datetime


class NotionClient:
    """Notion API wrapper adapted for existing contact-centric database"""

    def __init__(self, token: str, database_id: str):
        self.client = Client(auth=token)
        self.database_id = database_id

    def create_contact_pages(
        self,
        company_data: Dict,
        contacts: List[Dict],
        tier: str,
        priority: int
    ) -> List[str]:
        """
        Create pages for each contact in existing database format

        Args:
            company_data: Company information dict
            contacts: List of contact dicts
            tier: Assigned tier string
            priority: Priority score (1-10)

        Returns:
            List of created page IDs
        """
        page_ids = []

        for contact in contacts:
            # Check if contact already exists
            if not self.contact_exists(contact.get('name', ''), company_data.get('name', '')):
                page_id = self._create_single_contact(company_data, contact, tier, priority)
                page_ids.append(page_id)

        return page_ids

    def contact_exists(self, contact_name: str, company_name: str) -> bool:
        """
        Check if contact already exists in Notion

        Args:
            contact_name: Name of contact to check
            company_name: Company name for additional verification

        Returns:
            True if contact exists, False otherwise
        """
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "and": [
                        {
                            "property": "Contact Name",
                            "title": {
                                "contains": contact_name
                            }
                        },
                        {
                            "property": "Company",
                            "rich_text": {
                                "contains": company_name
                            }
                        }
                    ]
                }
            )

            return len(response['results']) > 0
        except Exception:
            return False

    def page_exists(self, company_name: str) -> bool:
        """
        Check if any contacts from company exist

        Args:
            company_name: Name of company to check

        Returns:
            True if company has contacts in database
        """
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Company",
                    "rich_text": {
                        "contains": company_name
                    }
                }
            )

            return len(response['results']) > 0
        except Exception:
            return False

    def _create_single_contact(
        self,
        company_data: Dict,
        contact: Dict,
        tier: str,
        priority: int
    ) -> str:
        """
        Create a single contact page in existing database format

        Args:
            company_data: Company information
            contact: Single contact dict
            tier: Assigned tier
            priority: Priority score

        Returns:
            Notion page ID
        """
        properties = {
            "Contact Name": {
                "title": [{"text": {"content": contact.get('name', 'Unknown')}}]
            },
            "Company": {
                "rich_text": [{"text": {"content": company_data.get('name', '')}}]
            },
            "Industry": {
                "select": {"name": self._map_industry(company_data.get('industry', ''))}
            },
            "Outreach Status": {
                "status": {"name": "Not started"}
            }
        }

        # Add contact title
        if contact.get('title'):
            properties["Title"] = {
                "rich_text": [{"text": {"content": contact['title']}}]
            }

        # Add email
        if contact.get('email'):
            properties["Email"] = {
                "email": contact['email']
            }

        # Add LinkedIn
        if contact.get('linkedin_url') and contact['linkedin_url'].startswith('http'):
            properties["LinkedIn"] = {
                "url": contact['linkedin_url']
            }

        # Add phone if available
        if contact.get('phone'):
            properties["Phone"] = {
                "phone_number": contact['phone']
            }

        # Add enrichment notes with company and tier info
        notes_content = self._build_notes(company_data, tier, priority)
        if notes_content:
            properties["Notes"] = {
                "rich_text": [{"text": {"content": notes_content}}]
            }

        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

        return response['id']

    def _build_notes(self, company_data: Dict, tier: str, priority: int) -> str:
        """
        Build notes field with enrichment data

        Args:
            company_data: Company information
            tier: Assigned tier
            priority: Priority score

        Returns:
            Notes text
        """
        notes_parts = [
            f"🎯 Enrichment Data (Auto-generated {datetime.now().strftime('%Y-%m-%d')})",
            f"",
            f"Tier: {tier}",
            f"Priority Score: {priority}/10",
            f""
        ]

        if company_data.get('domain'):
            notes_parts.append(f"Website: https://{company_data['domain']}")

        if company_data.get('linkedin_url'):
            notes_parts.append(f"Company LinkedIn: {company_data['linkedin_url']}")

        if company_data.get('employee_count'):
            size = self._map_size(company_data['employee_count'])
            notes_parts.append(f"Company Size: {size} ({company_data['employee_count']} employees)")

        if company_data.get('location'):
            notes_parts.append(f"Location: {company_data['location']}")

        if company_data.get('revenue_range'):
            notes_parts.append(f"Revenue: {company_data['revenue_range']}")

        if company_data.get('funding_stage') and company_data['funding_stage'] != 'Unknown':
            notes_parts.append(f"Funding Stage: {company_data['funding_stage']}")

        if company_data.get('apollo_id'):
            notes_parts.append(f"")
            notes_parts.append(f"Apollo ID: {company_data['apollo_id']}")

        return "\n".join(notes_parts)

    def _map_industry(self, industry: str) -> str:
        """Map Apollo industry to existing Notion options"""
        industry_lower = industry.lower()

        # Match to existing options in user's database
        if any(kw in industry_lower for kw in ['insurance', 'payer', 'health plan']):
            return "Insurance"
        elif any(kw in industry_lower for kw in ['hospital', 'health system', 'provider', 'clinic', 'medical center']):
            return "Hospital & Health Systems"
        elif any(kw in industry_lower for kw in ['pharmacy', 'pbm', 'drug']):
            return "Healthcare Tech"  # Closest match
        elif any(kw in industry_lower for kw in ['pharma', 'pharmaceutical']):
            return "Pharma"
        elif any(kw in industry_lower for kw in ['biotech', 'biotechnology']):
            return "Biotech"
        elif any(kw in industry_lower for kw in ['medical device', 'device']):
            return "Medical Devices"
        elif any(kw in industry_lower for kw in ['digital health', 'health tech']):
            return "Digital Health"
        elif any(kw in industry_lower for kw in ['telehealth', 'telemedicine']):
            return "Telehealth"
        elif any(kw in industry_lower for kw in ['health service', 'healthcare service']):
            return "Health Services"
        else:
            return "Healthcare Tech"  # Default

    def _map_size(self, employee_count: int) -> str:
        """Map employee count to size range"""
        if not employee_count or employee_count == 0:
            return "Unknown"
        elif employee_count < 50:
            return "1-50"
        elif employee_count < 200:
            return "51-200"
        elif employee_count < 1000:
            return "201-1000"
        elif employee_count < 5000:
            return "1000-5000"
        else:
            return "5000+"
