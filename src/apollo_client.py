"""
Apollo.io API Client
Handles company and contact enrichment
"""

import requests
from typing import Optional, List, Dict
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type


class ApolloClient:
    """Apollo.io API client for company and contact enrichment"""

    BASE_URL = "https://api.apollo.io/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        })

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_company(self, company_name: str) -> Optional[Dict]:
        """
        Search for company by name

        Args:
            company_name: Name of the company to search

        Returns:
            Company data dict or None if not found
        """
        endpoint = f"{self.BASE_URL}/organizations/search"

        payload = {
            "q_organization_name": company_name,
            "page": 1,
            "per_page": 1
        }

        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        if data.get('organizations') and len(data['organizations']) > 0:
            org = data['organizations'][0]
            return self._normalize_company(org)

        return None

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_people(
        self,
        company_id: str,
        titles: List[str],
        max_results: int = 10
    ) -> List[Dict]:
        """
        Find decision makers at company

        Args:
            company_id: Apollo organization ID
            titles: List of job titles to search for
            max_results: Maximum number of contacts to return

        Returns:
            List of contact dicts
        """
        endpoint = f"{self.BASE_URL}/people/search"

        payload = {
            "organization_ids": [company_id],
            "person_titles": titles,
            "page": 1,
            "per_page": max_results
        }

        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        contacts = []
        for person in data.get('people', []):
            contacts.append(self._normalize_contact(person))

        return contacts

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_person_by_name(
        self,
        person_name: str,
        company_name: str
    ) -> Optional[Dict]:
        """
        Find specific person by name and company

        Args:
            person_name: Full name of the person
            company_name: Company name

        Returns:
            Contact dict or None if not found
        """
        endpoint = f"{self.BASE_URL}/people/search"

        # First get company to narrow search
        company_data = self.search_company(company_name)
        if not company_data:
            return None

        # Search for person at that company
        payload = {
            "q_keywords": person_name,
            "organization_ids": [company_data['apollo_id']],
            "page": 1,
            "per_page": 5  # Get top 5 matches
        }

        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        # Find best match by name
        people = data.get('people', [])
        if not people:
            return None

        # Try to find exact or close match
        person_name_lower = person_name.lower()
        for person in people:
            full_name = person.get('name', '').lower()
            if person_name_lower in full_name or full_name in person_name_lower:
                return self._normalize_contact(person)

        # If no close match, return first result
        return self._normalize_contact(people[0])

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_by_linkedin_url(self, linkedin_url: str) -> Optional[Dict]:
        """
        Find person by LinkedIn URL using enrichment endpoint (exact match)

        Args:
            linkedin_url: LinkedIn profile URL

        Returns:
            Tuple of (contact_dict, company_dict) or (None, None) if not found
        """
        # Use enrichment endpoint for exact LinkedIn matching
        endpoint = f"{self.BASE_URL}/people/match"

        # Clean URL
        linkedin_url = linkedin_url.strip()
        if not linkedin_url.startswith('http'):
            linkedin_url = f"https://{linkedin_url}"

        # Enrichment endpoint with LinkedIn URL
        payload = {
            "linkedin_url": linkedin_url
        }

        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        # Enrichment endpoint returns 'person' not 'people'
        person = data.get('person')
        if not person:
            return None, None

        person_data = self._normalize_contact(person)

        # Get company data if available
        company_data = None
        org = person.get('organization')
        if org:
            company_data = self._normalize_company(org)

        return person_data, company_data

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_by_email(self, email: str) -> Optional[Dict]:
        """
        Find person by email address using enrichment endpoint (exact match)

        Args:
            email: Email address

        Returns:
            Tuple of (contact_dict, company_dict) or (None, None) if not found
        """
        # Use enrichment endpoint for exact email matching
        endpoint = f"{self.BASE_URL}/people/match"

        # Enrichment endpoint with email
        payload = {
            "email": email.strip()
        }

        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        # Enrichment endpoint returns 'person' not 'people'
        person = data.get('person')
        if not person:
            return None, None

        person_data = self._normalize_contact(person)

        # Get company data if available
        company_data = None
        org = person.get('organization')
        if org:
            company_data = self._normalize_company(org)

        return person_data, company_data

    def _normalize_company(self, raw_data: Dict) -> Dict:
        """Convert Apollo response to internal format"""
        return {
            'apollo_id': raw_data.get('id'),
            'name': raw_data.get('name', ''),
            'domain': raw_data.get('website_url', '').replace('http://', '').replace('https://', '').rstrip('/'),
            'linkedin_url': raw_data.get('linkedin_url', ''),
            'industry': raw_data.get('industry', ''),
            'employee_count': raw_data.get('estimated_num_employees', 0),
            'revenue_range': self._format_revenue(raw_data.get('estimated_annual_revenue')),
            'location': self._format_location(raw_data),
            'technologies': raw_data.get('technologies', []),
            'funding_stage': raw_data.get('funding_stage', 'Unknown'),
        }

    def _normalize_contact(self, raw_data: Dict) -> Dict:
        """Convert Apollo contact response to internal format"""
        return {
            'apollo_id': raw_data.get('id'),
            'name': raw_data.get('name', ''),
            'first_name': raw_data.get('first_name', ''),
            'last_name': raw_data.get('last_name', ''),
            'title': raw_data.get('title', ''),
            'seniority': raw_data.get('seniority', ''),
            'email': raw_data.get('email'),
            'phone': raw_data.get('phone'),
            'linkedin_url': raw_data.get('linkedin_url', ''),
            'city': raw_data.get('city', ''),
            'state': raw_data.get('state', ''),
            'country': raw_data.get('country', ''),
        }

    def _format_revenue(self, revenue: Optional[int]) -> str:
        """Format revenue into ranges"""
        if not revenue:
            return "Unknown"

        if revenue < 1_000_000:
            return "<$1M"
        elif revenue < 10_000_000:
            return "$1-10M"
        elif revenue < 50_000_000:
            return "$10-50M"
        elif revenue < 200_000_000:
            return "$50-200M"
        else:
            return "$200M+"

    def _format_location(self, raw_data: Dict) -> str:
        """Format location from company data"""
        parts = []

        if raw_data.get('city'):
            parts.append(raw_data['city'])
        if raw_data.get('state'):
            parts.append(raw_data['state'])
        if raw_data.get('country'):
            parts.append(raw_data['country'])

        return ", ".join(parts) if parts else "Unknown"

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_people_by_company(
        self,
        company_id: str,
        titles: List[str],
        seniorities: List[str] = None,
        locations: List[str] = None,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for people at a specific company with advanced filters

        Args:
            company_id: Apollo organization ID
            titles: List of job titles to search for
            seniorities: List of seniority levels (optional)
            locations: List of locations (optional)
            max_results: Maximum number of people to return

        Returns:
            List of normalized contact dicts
        """
        endpoint = f"{self.BASE_URL}/people/search"

        payload = {
            "organization_ids": [company_id],
            "person_titles": titles,
            "page": 1,
            "per_page": min(max_results, 100)  # Apollo max is 100 per request
        }

        # Add optional filters
        if seniorities:
            payload["person_seniorities"] = seniorities

        if locations:
            payload["person_locations"] = locations

        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()

        # Normalize all contacts
        people = []
        for person in data.get('people', []):
            people.append(self._normalize_contact(person))

        return people

    def get_target_titles(self, industry: str) -> List[str]:
        """
        Determine which titles to search based on company industry

        Args:
            industry: Company industry string

        Returns:
            List of job titles to search for
        """
        industry_lower = industry.lower()

        # Base titles for everyone
        base_titles = ['CEO', 'COO', 'CFO', 'President', 'Founder']

        # Industry-specific titles
        if any(kw in industry_lower for kw in ['insurance', 'payer', 'health plan']):
            return base_titles + [
                'CMO', 'Chief Medical Officer',
                'VP Quality', 'VP Operations',
                'VP Medicare', 'VP Medicare Advantage',
                'Director Star Ratings', 'Director Quality',
                'VP Member Services'
            ]

        elif any(kw in industry_lower for kw in ['hospital', 'provider', 'health system', 'clinic', 'medical']):
            return base_titles + [
                'VP Operations', 'VP Care Management',
                'VP Population Health', 'Chief Clinical Officer',
                'Director Care Management', 'VP Quality',
                'Chief Nursing Officer'
            ]

        elif any(kw in industry_lower for kw in ['pharmacy', 'pbm', 'drug']):
            return base_titles + [
                'VP Pharmacy Operations', 'VP Clinical Programs',
                'Director Adherence', 'Chief Pharmacy Officer',
                'VP Pharmacy Services'
            ]

        elif any(kw in industry_lower for kw in ['pharma', 'biotech', 'pharmaceutical']):
            return base_titles + [
                'VP Commercial', 'VP Market Access',
                'Director Patient Services', 'VP Marketing'
            ]

        else:
            # Default for other industries
            return base_titles + [
                'CTO', 'VP Strategy', 'VP Innovation',
                'VP Business Development', 'VP Sales'
            ]
