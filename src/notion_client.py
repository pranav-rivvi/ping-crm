"""
Notion API Client - Unified
Handles contact enrichment in your existing Notion database

Features:
- Find existing contacts by name + company
- Update existing contacts with Apollo data
- Create new contacts if not found
- Upsert operation (update or create)
"""

from notion_client import Client
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os


class NotionClient:
    """Unified Notion client for contact enrichment"""

    def __init__(self, token: str, database_id: str):
        self.client = Client(auth=token)
        self.database_id = database_id

    # ============================================================
    # READ OPERATIONS
    # ============================================================

    def find_contact(self, contact_name: str, company_name: str) -> Optional[Dict]:
        """
        Find existing contact in Notion database

        Args:
            contact_name: Full name of person
            company_name: Company name

        Returns:
            Page object if found, None otherwise
        """
        try:
            # Search by contact name (title field)
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Contact Name",
                    "title": {
                        "contains": contact_name
                    }
                }
            )

            # Check for company match in results
            for page in response['results']:
                page_company = self._get_company_from_page(page)
                if company_name.lower() in page_company.lower():
                    return page

            return None

        except Exception as e:
            print(f"Error finding contact: {e}")
            return None

    def page_exists(self, company_name: str) -> bool:
        """
        Check if any contacts from company exist

        Args:
            company_name: Company name to check

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

    # ============================================================
    # WRITE OPERATIONS - Single Contact
    # ============================================================

    def upsert_contact(
        self,
        contact_name: str,
        company_name: str,
        enriched_data: Dict,
        company_data: Optional[Dict] = None,
        outreach_context: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Update if exists, create if not (upsert operation)

        Args:
            contact_name: Full name of person
            company_name: Company name
            enriched_data: Contact data from Apollo
            company_data: Optional company data for notes
            outreach_context: Optional personalized outreach context from AI

        Returns:
            Tuple of (success: bool, action: str) where action is 'updated' or 'created'
        """
        # Try to find existing contact
        existing_page = self.find_contact(contact_name, company_name)

        if existing_page:
            # Update existing
            success = self._update_page(
                page_id=existing_page['id'],
                enriched_data=enriched_data,
                company_data=company_data,
                outreach_context=outreach_context
            )
            return (success, 'updated')
        else:
            # Create new
            page_id = self._create_page(
                contact_name=contact_name,
                company_name=company_name,
                enriched_data=enriched_data,
                company_data=company_data,
                outreach_context=outreach_context
            )
            return (page_id is not None, 'created')

    # ============================================================
    # WRITE OPERATIONS - Bulk (for company enrichment)
    # ============================================================

    def create_contact_pages(
        self,
        company_data: Dict,
        contacts: List[Dict],
        tier: str,
        priority: int
    ) -> List[str]:
        """
        Create pages for multiple contacts from a company

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
                page_id = self._create_page(
                    contact_name=contact.get('name', 'Unknown'),
                    company_name=company_data.get('name', ''),
                    enriched_data=contact,
                    company_data=company_data,
                    tier=tier,
                    priority=priority
                )
                if page_id:
                    page_ids.append(page_id)

        return page_ids

    def contact_exists(self, contact_name: str, company_name: str) -> bool:
        """Check if specific contact exists"""
        return self.find_contact(contact_name, company_name) is not None

    # ============================================================
    # INTERNAL METHODS
    # ============================================================

    def _update_page(
        self,
        page_id: str,
        enriched_data: Dict,
        company_data: Optional[Dict] = None,
        outreach_context: Optional[str] = None
    ) -> bool:
        """Update existing page with enriched data"""
        try:
            properties = {}

            # Update Title if available
            if enriched_data.get('title'):
                properties["Title"] = {
                    "rich_text": [{"text": {"content": enriched_data['title']}}]
                }

            # Update Email if available
            if enriched_data.get('email'):
                properties["Email"] = {
                    "email": enriched_data['email']
                }

            # Update Phone if available
            if enriched_data.get('phone'):
                properties["Phone"] = {
                    "phone_number": enriched_data['phone']
                }

            # Update LinkedIn - only if it's a real LinkedIn URL
            if enriched_data.get('linkedin_url'):
                linkedin_url = enriched_data['linkedin_url']
                # Only update if it's a real LinkedIn URL
                if linkedin_url.startswith('http') and 'linkedin.com' in linkedin_url.lower():
                    properties["LinkedIn"] = {
                        "url": linkedin_url
                    }
                # If no valid LinkedIn, leave field null (don't update)

            # Add location fields (City, State, Country) - nullable
            if enriched_data.get('city'):
                properties["City"] = {
                    "rich_text": [{"text": {"content": enriched_data['city']}}]
                }

            if enriched_data.get('state'):
                properties["State"] = {
                    "rich_text": [{"text": {"content": enriched_data['state']}}]
                }

            if enriched_data.get('country'):
                properties["Country"] = {
                    "rich_text": [{"text": {"content": enriched_data['country']}}]
                }

            # Add enrichment notes with outreach context
            if company_data:
                notes_content = self._build_enrichment_notes(
                    enriched_data,
                    company_data,
                    outreach_context=outreach_context
                )
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
            print(f"Error updating page: {e}")
            return False

    def _create_page(
        self,
        contact_name: str,
        company_name: str,
        enriched_data: Dict,
        company_data: Optional[Dict] = None,
        tier: Optional[str] = None,
        priority: Optional[int] = None,
        outreach_context: Optional[str] = None
    ) -> Optional[str]:
        """Create new page with enriched data"""
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

            # Add LinkedIn - only if it's a real LinkedIn URL
            if enriched_data.get('linkedin_url'):
                linkedin_url = enriched_data['linkedin_url']
                # Only add if it's a real LinkedIn URL (not empty, contains 'linkedin.com')
                if linkedin_url.startswith('http') and 'linkedin.com' in linkedin_url.lower():
                    properties["LinkedIn"] = {
                        "url": linkedin_url
                    }
                # If no valid LinkedIn, leave field null (don't set anything)

            # Add location fields (City, State, Country) - nullable
            if enriched_data.get('city'):
                properties["City"] = {
                    "rich_text": [{"text": {"content": enriched_data['city']}}]
                }

            if enriched_data.get('state'):
                properties["State"] = {
                    "rich_text": [{"text": {"content": enriched_data['state']}}]
                }

            if enriched_data.get('country'):
                properties["Country"] = {
                    "rich_text": [{"text": {"content": enriched_data['country']}}]
                }

            # Add Industry if company data available
            if company_data and company_data.get('industry'):
                properties["Industry"] = {
                    "select": {"name": self._map_industry(company_data['industry'])}
                }

            # Add Relationship Type based on data completeness
            linkedin_url = enriched_data.get('linkedin_url', '')
            has_linkedin = linkedin_url and 'linkedin.com' in linkedin_url.lower()
            has_email = enriched_data.get('email') and 'email_not_unlocked' not in enriched_data.get('email', '')

            # Try to set Relationship Type (optional field - won't fail if doesn't exist)
            try:
                if has_linkedin or has_email:
                    properties["Relationship Type"] = {
                        "select": {"name": "Prospect"}
                    }
                else:
                    # No direct contact method - needs alternative approach
                    properties["Relationship Type"] = {
                        "select": {"name": "Industry Expert"}  # Or could be custom status
                    }
            except Exception:
                pass  # Skip if field doesn't exist or wrong options

            # Add enrichment notes with outreach context
            if company_data:
                notes_content = self._build_enrichment_notes(
                    enriched_data,
                    company_data,
                    tier,
                    priority,
                    outreach_context=outreach_context
                )
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
            print(f"Error creating page: {e}")
            return None

    def _get_company_from_page(self, page: Dict) -> str:
        """Extract company name from page object"""
        try:
            company_prop = page['properties'].get('Company', {})
            if company_prop.get('rich_text'):
                return company_prop['rich_text'][0]['text']['content']
        except Exception:
            pass
        return ""

    def _generate_ai_personalized_note(
        self,
        contact_data: Dict,
        company_data: Dict,
        outreach_context: str
    ) -> str:
        """Generate AI-powered personalized note for outreach"""
        try:
            # Check if AI is available
            if not os.getenv('OPENAI_API_KEY') and not os.getenv('GEMINI_API_KEY'):
                return None

            from llm_helper import AITargeting
            ai = AITargeting()

            # Build context for AI
            person_name = contact_data.get('name', 'this contact')
            title = contact_data.get('title', 'unknown role')
            company = company_data.get('name', 'the company') if company_data else 'the company'
            industry = company_data.get('industry', '') if company_data else ''
            company_size = company_data.get('employee_count', '') if company_data else ''

            prompt = f"""Write a brief, actionable note for a sales/outreach team about why they should connect with this person.

**Contact**: {person_name}
**Title**: {title}
**Company**: {company}
**Industry**: {industry}
**Company Size**: {company_size} employees
**Outreach Goal**: {outreach_context}

Write 2-3 sentences explaining:
1. Why this person is relevant for the outreach goal
2. What value proposition to lead with
3. One specific talking point or hook

Keep it professional, concise, and actionable. No fluff."""

            # Get AI response
            if os.getenv('OPENAI_API_KEY'):
                import openai
                client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=200
                )

                return response.choices[0].message.content.strip()

            elif os.getenv('GEMINI_API_KEY'):
                import google.generativeai as genai
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                model = genai.GenerativeModel('gemini-1.5-flash')

                response = model.generate_content(prompt)
                return response.text.strip()

        except Exception as e:
            print(f"AI note generation failed: {e}")
            return None

    def _build_enrichment_notes(
        self,
        contact_data: Dict,
        company_data: Dict,
        tier: Optional[str] = None,
        priority: Optional[int] = None,
        outreach_context: Optional[str] = None
    ) -> str:
        """Build enrichment notes with all data"""
        notes_parts = []

        # AI-Generated Personalized Note (if outreach context provided)
        if outreach_context and company_data:
            ai_note = self._generate_ai_personalized_note(contact_data, company_data, outreach_context)
            if ai_note:
                notes_parts.append(f"🤖 AI-Powered Outreach Strategy:")
                notes_parts.append(f"  {ai_note}")
                notes_parts.append("")

        # Personalized outreach context
        if outreach_context:
            notes_parts.append(f"💡 Outreach Context:")
            notes_parts.append(f"  {outreach_context}")
            notes_parts.append("")

        notes_parts.append(f"🎯 Enriched on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        notes_parts.append("")

        # Add tier/priority if available
        if tier or priority:
            notes_parts.append("📊 Scoring:")
            if tier:
                notes_parts.append(f"  • Tier: {tier}")
            if priority:
                notes_parts.append(f"  • Priority: {priority}/10")
            notes_parts.append("")

        # Contact info
        notes_parts.append("📧 Contact Info:")
        if contact_data.get('email'):
            notes_parts.append(f"  • Email: {contact_data['email']}")
        if contact_data.get('phone'):
            notes_parts.append(f"  • Phone: {contact_data['phone']}")

        # LinkedIn handling - track availability
        linkedin_url = contact_data.get('linkedin_url', '')
        if linkedin_url and 'linkedin.com' in linkedin_url.lower():
            notes_parts.append(f"  • LinkedIn: {linkedin_url}")
        else:
            notes_parts.append(f"  • LinkedIn: Not available - use email or phone for outreach")

        if contact_data.get('title'):
            notes_parts.append(f"  • Title: {contact_data['title']}")
        if contact_data.get('seniority'):
            notes_parts.append(f"  • Level: {contact_data['seniority']}")

        # Personal location (if different from company)
        contact_location_parts = []
        if contact_data.get('city'):
            contact_location_parts.append(contact_data['city'])
        if contact_data.get('state'):
            contact_location_parts.append(contact_data['state'])
        if contact_data.get('country'):
            contact_location_parts.append(contact_data['country'])

        if contact_location_parts:
            notes_parts.append(f"  • Location: {', '.join(contact_location_parts)}")

        # Company info
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

        # Apollo IDs
        if contact_data.get('apollo_id') or company_data.get('apollo_id'):
            notes_parts.append("")
            apollo_info = f"Apollo IDs: {contact_data.get('apollo_id', 'N/A')} (contact)"
            if company_data.get('apollo_id'):
                apollo_info += f", {company_data['apollo_id']} (company)"
            notes_parts.append(apollo_info)

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
            return "Healthcare Tech"
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
