"""
Tier Assignment and Priority Scoring
Simple rule-based logic for MVP
"""

from typing import Dict, List


class TierAssigner:
    """Auto-assign tier based on company characteristics"""

    TIER_1_KEYWORDS = ['imo', 'agent', 'broker', 'medicare advisor', 'insurance marketing']
    TIER_2_KEYWORDS = ['medicare advantage', 'health plan', 'insurance', 'payer', 'medicaid']
    TIER_3_KEYWORDS = ['aco', 'mso', 'provider', 'medical group', 'health system', 'hospital', 'clinic']
    TIER_4_KEYWORDS = ['pharma', 'pharmaceutical', 'biotech', 'drug']

    def assign_tier(self, company_data: Dict) -> str:
        """
        Assign tier based on industry and keywords

        Args:
            company_data: Company information dict

        Returns:
            Tier string (e.g., "Tier 1 - AEP Urgent")
        """
        industry = company_data.get('industry', '').lower()
        name = company_data.get('name', '').lower()

        search_text = f"{industry} {name}"

        # Check Tier 1 (AEP Urgent - IMOs, Agents, Brokers)
        if any(kw in search_text for kw in self.TIER_1_KEYWORDS):
            return "Tier 1 - AEP Urgent"

        # Check Tier 2 (Strategic - Health Plans)
        if any(kw in search_text for kw in self.TIER_2_KEYWORDS):
            return "Tier 2 - Strategic"

        # Check Tier 3 (Providers)
        if any(kw in search_text for kw in self.TIER_3_KEYWORDS):
            return "Tier 3 - Proven Vertical"

        # Check Tier 4 (Pharma)
        if any(kw in search_text for kw in self.TIER_4_KEYWORDS):
            return "Tier 4 - Exploratory"

        # Default to Tier 3
        return "Tier 3 - Proven Vertical"


class PriorityScorer:
    """Calculate priority score (1-10) for each company"""

    def calculate_priority(self, company_data: Dict, contacts: List[Dict], tier: str) -> int:
        """
        Score based on multiple factors

        Scoring factors:
        - Company size (larger = higher)
        - Revenue (higher = higher)
        - Contact quality (verified emails = higher)
        - Tier (Tier 1 gets boost)

        Args:
            company_data: Company information
            contacts: List of contacts
            tier: Assigned tier

        Returns:
            Priority score (1-10)
        """
        score = 5.0  # Base score

        # Factor 1: Company size (+0 to +2)
        size = company_data.get('employee_count', 0)
        if size > 5000:
            score += 2
        elif size > 1000:
            score += 1.5
        elif size > 200:
            score += 1
        elif size > 50:
            score += 0.5
        elif size < 10:
            score -= 0.5  # Very small companies

        # Factor 2: Revenue (+0 to +2)
        revenue = company_data.get('revenue_range', '')
        if '$200M+' in revenue:
            score += 2
        elif '$50-200M' in revenue:
            score += 1.5
        elif '$10-50M' in revenue:
            score += 1
        elif '$1-10M' in revenue:
            score += 0.5

        # Factor 3: Contact quality (+0 to +2)
        emails_found = sum(1 for c in contacts if c.get('email'))
        if emails_found >= 3:
            score += 2
        elif emails_found >= 2:
            score += 1.5
        elif emails_found >= 1:
            score += 1
        else:
            score -= 0.5  # No emails found

        # Factor 4: Tier boost
        if 'Tier 1' in tier:
            score += 2  # AEP urgent
        elif 'Tier 2' in tier:
            score += 1  # Strategic

        # Clamp to 1-10
        return max(1, min(10, int(round(score))))
