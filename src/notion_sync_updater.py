"""
Notion API Client - Update Mode
Enriches existing contacts in your Notion database
"""

from notion_client import Client
from typing import Dict, Optional
from datetime import datetime


class NotionUpdater:
    """Updates existing Notion contacts with enriched data"""

    def __init__(self, token: str, database_id: str):
        self.client = Client(auth=token)
        self.database_id = database_id

    def find_contact(self, contact_name: str, company_name: str) -> Optional[Dict]:
        """
        Find existing contact in Notion database

        Args:
            contact_name: Name of person
            company_name: Company name

        Returns:
            Page object if found, None otherwise
        """
        try:
            # Search by contact name
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Contact Name",
                    "title": {
                        "contains": contact_name
                    }
                }
            )

            # If we have results, check for company match
            for page in response['results']:
                page_company = self._get_company_from_page(page)
                if company_name.lower() in page_company.lower():
                    return page

            return None

        except Exception as e:
            print(f"Error finding contact: {e}")
            return None

    def enrich_contact(
        self,
        page_id: str,
        enriched_data: Dict,
        company_data: Optional[Dict] = None
    ) -> bool:
        """
        Update existing contact page with enriched data

        Args:
            page_id: Notion page ID to update
            enriched_data: Contact data from Apollo
            company_data: Optional company data for notes

        Returns:
            True if successful, False otherwise
        """
        try:
            properties = {}

            # Update Title if missing
            if enriched_data.get('title'):
                properties["Title"] = {
                    "rich_text": [{"text": {"content": enriched_data['title']}}]
                }

            # Update Email if missing
            if enriched_data.get('email'):
                properties["Email"] = {
                    "email": enriched_data['email']
                }

            # Update Phone if available
            if enriched_data.get('phone'):
                properties["Phone"] = {
                    "phone_number": enriched_data['phone']
                }

            # Update LinkedIn if available
            if enriched_data.get('linkedin_url') and enriched_data['linkedin_url'].startswith('http'):
                properties["LinkedIn"] = {
                    "url": enriched_data['linkedin_url']
                }

            # Add enrichment notes
            if company_data:
                notes_content = self._build_enrichment_notes(enriched_data, company_data)
                properties["Notes"] = {
                    "rich_text": [{"text": {"content": notes_content}}]
                }

            # Update the page
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )

            return True

        except Exception as e:
            print(f"Error updating contact: {e}")
            return False

    def create_contact(
        self,
        contact_name: str,
        company_name: str,
        enriched_data: Dict,
        company_data: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Create new contact page with enriched data

        Args:
            contact_name: Full name of person
            company_name: Company name
            enriched_data: Contact data from Apollo
            company_data: Optional company data for notes

        Returns:
            Page ID if successful, None otherwise
        """
        try:
            properties = {
                "Contact Name": {
                    "title": [{"text": {"content": contact_name}}]
                },
                "Company": {
                    "rich_text": [{"text": {"content": company_name}}]
                },
                "Outreach Status": {
                    "status": {"name": "Not started"}
                }
            }

            # Add Title
            if enriched_data.get('title'):
                properties["Title"] = {
                    "rich_text": [{"text": {"content": enriched_data['title']}}]
                }

            # Add Email
            if enriched_data.get('email'):
                properties["Email"] = {
                    "email": enriched_data['email']
                }

            # Add Phone
            if enriched_data.get('phone'):
                properties["Phone"] = {
                    "phone_number": enriched_data['phone']
                }

            # Add LinkedIn
            if enriched_data.get('linkedin_url') and enriched_data['linkedin_url'].startswith('http'):
                properties["LinkedIn"] = {
                    "url": enriched_data['linkedin_url']
                }

            # Add enrichment notes
            if company_data:
                notes_content = self._build_enrichment_notes(enriched_data, company_data)
                properties["Notes"] = {
                    "rich_text": [{"text": {"content": notes_content}}]
                }

            # Create the page
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )

            return response['id']

        except Exception as e:
            print(f"Error creating contact: {e}")
            return None

    def upsert_contact(
        self,
        contact_name: str,
        company_name: str,
        enriched_data: Dict,
        company_data: Optional[Dict] = None
    ) -> tuple[bool, str]:
        """
        Update if exists, create if not (upsert operation)

        Args:
            contact_name: Full name of person
            company_name: Company name
            enriched_data: Contact data from Apollo
            company_data: Optional company data for notes

        Returns:
            Tuple of (success: bool, action: str) where action is 'updated' or 'created'
        """
        # Try to find existing contact
        existing_page = self.find_contact(contact_name, company_name)

        if existing_page:
            # Update existing
            success = self.enrich_contact(
                page_id=existing_page['id'],
                enriched_data=enriched_data,
                company_data=company_data
            )
            return (success, 'updated')
        else:
            # Create new
            page_id = self.create_contact(
                contact_name=contact_name,
                company_name=company_name,
                enriched_data=enriched_data,
                company_data=company_data
            )
            return (page_id is not None, 'created')

    def _get_company_from_page(self, page: Dict) -> str:
        """Extract company name from page object"""
        try:
            company_prop = page['properties'].get('Company', {})
            if company_prop.get('rich_text'):
                return company_prop['rich_text'][0]['text']['content']
        except Exception:
            pass
        return ""

    def _build_enrichment_notes(self, contact_data: Dict, company_data: Dict) -> str:
        """
        Build enrichment notes with all data

        Args:
            contact_data: Contact information from Apollo
            company_data: Company information from Apollo

        Returns:
            Formatted notes text
        """
        notes_parts = [
            f"🎯 Enriched on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "📧 Contact Info:",
        ]

        if contact_data.get('email'):
            notes_parts.append(f"  • Email: {contact_data['email']}")
        if contact_data.get('phone'):
            notes_parts.append(f"  • Phone: {contact_data['phone']}")
        if contact_data.get('linkedin_url'):
            notes_parts.append(f"  • LinkedIn: {contact_data['linkedin_url']}")
        if contact_data.get('title'):
            notes_parts.append(f"  • Title: {contact_data['title']}")
        if contact_data.get('seniority'):
            notes_parts.append(f"  • Level: {contact_data['seniority']}")

        notes_parts.append("")
        notes_parts.append("🏢 Company Info:")

        if company_data.get('domain'):
            notes_parts.append(f"  • Website: https://{company_data['domain']}")
        if company_data.get('linkedin_url'):
            notes_parts.append(f"  • Company LinkedIn: {company_data['linkedin_url']}")
        if company_data.get('employee_count'):
            notes_parts.append(f"  • Size: {company_data['employee_count']:,} employees")
        if company_data.get('location'):
            notes_parts.append(f"  • Location: {company_data['location']}")
        if company_data.get('revenue_range'):
            notes_parts.append(f"  • Revenue: {company_data['revenue_range']}")
        if company_data.get('industry'):
            notes_parts.append(f"  • Industry: {company_data['industry']}")

        if company_data.get('apollo_id'):
            notes_parts.append("")
            notes_parts.append(f"Apollo IDs: {contact_data.get('apollo_id', 'N/A')} (contact), {company_data['apollo_id']} (company)")

        return "\n".join(notes_parts)
