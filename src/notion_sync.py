"""
Notion API Client
Handles syncing enriched data to Notion database
"""

from notion_client import Client
from typing import Dict, List
from datetime import datetime


class NotionClient:
    """Notion API wrapper for CRM operations"""

    def __init__(self, token: str, database_id: str):
        self.client = Client(auth=token)
        self.database_id = database_id

    def create_company_page(
        self,
        company_data: Dict,
        contacts: List[Dict],
        tier: str,
        priority: int
    ) -> str:
        """
        Create new page in Notion database

        Args:
            company_data: Company information dict
            contacts: List of contact dicts
            tier: Assigned tier string
            priority: Priority score (1-10)

        Returns:
            Notion page ID
        """
        properties = self._build_properties(company_data, contacts, tier, priority)

        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

        return response['id']

    def page_exists(self, company_name: str) -> bool:
        """
        Check if company already exists in Notion

        Args:
            company_name: Name of company to check

        Returns:
            True if page exists, False otherwise
        """
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Company Name",
                    "title": {
                        "equals": company_name
                    }
                }
            )

            return len(response['results']) > 0
        except Exception:
            return False

    def _build_properties(
        self,
        company_data: Dict,
        contacts: List[Dict],
        tier: str,
        priority: int
    ) -> Dict:
        """
        Build Notion properties object

        Args:
            company_data: Company information
            contacts: List of contacts
            tier: Assigned tier
            priority: Priority score

        Returns:
            Properties dict for Notion API
        """
        # Sort contacts by having email (prioritize those with emails)
        sorted_contacts = sorted(
            contacts,
            key=lambda c: (bool(c.get('email')), c.get('seniority', '') != ''),
            reverse=True
        )[:3]  # Top 3 contacts

        properties = {
            "Company Name": {
                "title": [{"text": {"content": company_data.get('name', '')}}]
            },
            "Status": {
                "select": {"name": "Not Contacted"}
            },
            "Industry": {
                "select": {"name": self._map_industry(company_data.get('industry', ''))}
            },
            "Tier": {
                "select": {"name": tier}
            },
            "Priority Score": {
                "number": priority
            },
            "Enrichment Date": {
                "date": {"start": datetime.now().isoformat()}
            },
            "Apollo ID": {
                "rich_text": [{"text": {"content": company_data.get('apollo_id', '')}}]
            }
        }

        # Add company website (validate URL)
        if company_data.get('domain'):
            domain = company_data['domain']
            # Ensure domain is valid and not empty
            if domain and domain.strip() and '.' in domain:
                properties["Company Website"] = {
                    "url": f"https://{domain}"
                }

        # Add LinkedIn (validate URL)
        if company_data.get('linkedin_url'):
            linkedin_url = company_data['linkedin_url']
            # Ensure URL is valid
            if linkedin_url and linkedin_url.strip() and linkedin_url.startswith('http'):
                properties["Company LinkedIn"] = {
                    "url": linkedin_url
                }

        # Add company size
        properties["Company Size"] = {
            "select": {"name": self._map_size(company_data.get('employee_count', 0))}
        }

        # Add location
        if company_data.get('location'):
            properties["Location"] = {
                "rich_text": [{"text": {"content": company_data['location']}}]
            }

        # Add revenue range
        if company_data.get('revenue_range'):
            properties["Revenue Range"] = {
                "select": {"name": company_data['revenue_range']}
            }

        # Add funding stage
        if company_data.get('funding_stage'):
            properties["Funding Stage"] = {
                "select": {"name": company_data['funding_stage']}
            }

        # Add primary contact (if exists)
        if len(sorted_contacts) > 0:
            contact = sorted_contacts[0]
            properties["Primary Contact Name"] = {
                "rich_text": [{"text": {"content": contact.get('name', '')}}]
            }
            properties["Primary Contact Title"] = {
                "rich_text": [{"text": {"content": contact.get('title', '')}}]
            }
            if contact.get('email'):
                properties["Primary Contact Email"] = {
                    "email": contact['email']
                }
            if contact.get('linkedin_url') and contact['linkedin_url'].startswith('http'):
                properties["Primary Contact LinkedIn"] = {
                    "url": contact['linkedin_url']
                }

        # Add secondary contact (if exists)
        if len(sorted_contacts) > 1:
            contact = sorted_contacts[1]
            properties["Secondary Contact Name"] = {
                "rich_text": [{"text": {"content": contact.get('name', '')}}]
            }
            properties["Secondary Contact Title"] = {
                "rich_text": [{"text": {"content": contact.get('title', '')}}]
            }
            if contact.get('email'):
                properties["Secondary Contact Email"] = {
                    "email": contact['email']
                }

        # Add tertiary contact (if exists)
        if len(sorted_contacts) > 2:
            contact = sorted_contacts[2]
            properties["Tertiary Contact Name"] = {
                "rich_text": [{"text": {"content": contact.get('name', '')}}]
            }
            properties["Tertiary Contact Title"] = {
                "rich_text": [{"text": {"content": contact.get('title', '')}}]
            }
            if contact.get('email'):
                properties["Tertiary Contact Email"] = {
                    "email": contact['email']
                }

        return properties

    def _map_industry(self, industry: str) -> str:
        """Map Apollo industry to Notion options"""
        industry_lower = industry.lower()

        if any(kw in industry_lower for kw in ['insurance', 'payer', 'health plan']):
            return "Insurance / Payer"
        elif any(kw in industry_lower for kw in ['hospital', 'health system', 'provider', 'clinic', 'medical']):
            return "Healthcare Provider / Health System"
        elif any(kw in industry_lower for kw in ['pharmacy', 'pbm']):
            return "Pharmacy / PBM"
        elif any(kw in industry_lower for kw in ['pharma', 'biotech', 'pharmaceutical']):
            return "Pharma / Biotech"
        else:
            return "Other"

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
