# Apollo.io Precise Filtering Guide

## Overview

Apollo allows **very precise** filtering to find specific subgroups of employees. You can combine multiple filters to narrow down exactly who you want to reach.

---

## Available Filters

### 1. Job Titles (Exact or Keywords)

**Examples:**
```python
titles = ["CEO", "Chief Executive Officer"]
titles = ["VP Sales", "Vice President of Sales", "Sales VP"]
titles = ["Director of Marketing", "Marketing Director"]
```

**How it works:**
- Searches job title field for matches
- Can use partial matches with keywords
- Case-insensitive

---

### 2. Seniority Level

**Options:**
- `Owner` - Founders, Owners
- `C-Level` - CEO, CFO, CTO, CMO, etc.
- `VP` - Vice Presidents
- `Director` - Directors
- `Manager` - Managers
- `Senior` - Senior ICs (Individual Contributors)
- `Entry` - Entry-level

**Example:**
```python
# Find all VPs and Directors
payload = {
    "organization_ids": [company_id],
    "seniority": ["vp", "director"],
    "per_page": 50
}
```

---

### 3. Department/Function

**Departments:**
- Sales
- Marketing
- Engineering
- Product
- Finance
- Human Resources
- Operations
- Customer Service/Success
- Legal
- IT
- Business Development

**Example - Find all VP+ in Sales & Marketing:**
```python
payload = {
    "organization_ids": [company_id],
    "person_departments": ["sales", "marketing"],
    "person_seniorities": ["vp", "c_suite"],
    "per_page": 50
}
```

---

### 4. Management Level

**Options:**
- People managers vs Individual contributors
- Number of direct reports

**Example:**
```python
# Find managers with teams
payload = {
    "organization_ids": [company_id],
    "management_level": ["manager"],  # Has direct reports
    "per_page": 50
}
```

---

### 5. Location

**Filter by:**
- City
- State
- Country
- Specific office locations

**Example:**
```python
# Find contacts in Bay Area
payload = {
    "organization_ids": [company_id],
    "person_locations": ["San Francisco", "Palo Alto", "San Jose"]
}
```

---

### 6. Employment Status

**Options:**
- Current employees only (default)
- Past employees
- Both

**Example:**
```python
# Only current employees
payload = {
    "organization_ids": [company_id],
    "employment_status": ["currently_employed"]
}
```

---

## Real-World Use Cases

### Use Case 1: Healthcare Insurance Decision Makers

**Goal:** Find senior decision makers at health insurance companies

```python
def find_insurance_decision_makers(apollo, company_name):
    company = apollo.search_company(company_name)

    endpoint = f"{apollo.BASE_URL}/people/search"
    payload = {
        "organization_ids": [company['apollo_id']],

        # Specific healthcare titles
        "person_titles": [
            "Chief Medical Officer",
            "CMO",
            "VP Quality",
            "VP Medicare Advantage",
            "VP Population Health",
            "Director Star Ratings"
        ],

        # Only senior level
        "person_seniorities": ["vp", "c_suite"],

        # Current employees
        "employment_status": ["currently_employed"],

        "per_page": 20
    }

    response = apollo.session.post(endpoint, json=payload)
    return response.json()
```

**Result:** Get exactly 15-20 senior healthcare decision makers

---

### Use Case 2: Hospital IT Decision Makers

**Goal:** Find people who make technology buying decisions at hospitals

```python
def find_hospital_it_buyers(apollo, company_name):
    company = apollo.search_company(company_name)

    payload = {
        "organization_ids": [company['apollo_id']],

        # IT + Operations leadership
        "person_departments": ["information_technology", "operations"],

        # Director level and above
        "person_seniorities": ["director", "vp", "c_suite"],

        # Include CIO, CMIO, CTO, VP IT
        "q_keywords": "information technology OR digital OR innovation",

        "per_page": 30
    }
```

**Result:** IT directors, VPs, CIOs who make purchasing decisions

---

### Use Case 3: Pharma Commercial Leadership

**Goal:** Find commercial team leaders at pharmaceutical companies

```python
def find_pharma_commercial_leaders(apollo, company_name):
    company = apollo.search_company(company_name)

    payload = {
        "organization_ids": [company['apollo_id']],

        # Commercial titles
        "person_titles": [
            "VP Commercial",
            "VP Market Access",
            "VP Business Development",
            "Head of Commercial",
            "Chief Commercial Officer"
        ],

        # VP and above
        "person_seniorities": ["vp", "c_suite"],

        "per_page": 15
    }
```

**Result:** 10-15 commercial leaders making partnership decisions

---

### Use Case 4: Startup Founders & Early Team

**Goal:** Get founders and first 10 employees at a startup

```python
def find_startup_founders(apollo, company_name):
    company = apollo.search_company(company_name)

    payload = {
        "organization_ids": [company['apollo_id']],

        # Founder titles
        "person_titles": [
            "Founder",
            "Co-Founder",
            "CEO",
            "CTO",
            "COO",
            "President"
        ],

        # Owner/C-Level only
        "person_seniorities": ["owner", "c_suite"],

        "per_page": 10
    }
```

**Result:** Founders and C-suite at startup

---

### Use Case 5: Sales Team (for recruiting/competitive intel)

**Goal:** Find sales reps and managers at a competitor

```python
def find_sales_team(apollo, company_name):
    company = apollo.search_company(company_name)

    payload = {
        "organization_ids": [company['apollo_id']],

        # Sales department
        "person_departments": ["sales"],

        # All levels
        "person_seniorities": ["entry", "senior", "manager", "director", "vp"],

        # Sales titles
        "q_keywords": "sales OR account executive OR business development",

        "per_page": 100  # Can get up to 100 per page
    }
```

**Result:** Entire sales org from AEs to SVPs

---

## Combining Filters - Advanced Examples

### Example 1: Senior Operations Leaders in West Coast

```python
payload = {
    "organization_ids": [company_id],
    "person_titles": ["VP Operations", "COO", "Director Operations"],
    "person_seniorities": ["director", "vp", "c_suite"],
    "person_locations": ["California", "Oregon", "Washington"],
    "per_page": 20
}
```

### Example 2: Marketing Team Excluding Junior Roles

```python
payload = {
    "organization_ids": [company_id],
    "person_departments": ["marketing"],
    "person_seniorities": ["director", "vp", "c_suite"],  # Exclude entry/senior
    "per_page": 30
}
```

### Example 3: Recent Hires in Leadership

```python
payload = {
    "organization_ids": [company_id],
    "person_seniorities": ["director", "vp", "c_suite"],
    # Can also filter by "recently_changed_jobs": true
    "per_page": 25
}
```

---

## Precision Levels

### ⭐ High Precision (90%+ match)
```python
# Very specific titles + seniority
payload = {
    "person_titles": ["Chief Medical Officer", "CMO"],
    "person_seniorities": ["c_suite"],
}
# Result: Only CMOs
```

### ⭐⭐ Medium Precision (70-90% match)
```python
# Department + seniority
payload = {
    "person_departments": ["sales"],
    "person_seniorities": ["vp", "director"],
}
# Result: Sales leadership, might include some BizDev
```

### ⭐⭐⭐ Broad Search (50-70% match)
```python
# Keywords only
payload = {
    "q_keywords": "healthcare operations",
}
# Result: Various roles mentioning healthcare + operations
```

---

## Best Practices

### 1. Start Narrow, Then Expand
```python
# Round 1: Very specific
titles = ["CMO", "Chief Medical Officer"]

# Round 2: If not enough results, expand
titles = ["CMO", "Chief Medical Officer", "VP Medical Affairs", "VP Clinical"]
```

### 2. Use Multiple Filters Together
```python
# ✅ Good: Combines multiple filters
payload = {
    "person_departments": ["sales"],
    "person_seniorities": ["vp"],
    "person_locations": ["United States"],
}

# ❌ Less precise: Only one filter
payload = {
    "q_keywords": "sales vp",  # Might get false matches
}
```

### 3. Check Company Size
```python
# Small company (<200): Focus on C-suite + Directors
# Medium company (200-1000): Focus on VPs + Directors
# Large company (1000+): Can target specific departments/functions
```

---

## Code Implementation

### Method 1: Add to ApolloClient

```python
# In src/apollo_client.py

def search_people_advanced(
    self,
    company_id: str,
    titles: List[str] = None,
    seniorities: List[str] = None,
    departments: List[str] = None,
    locations: List[str] = None,
    max_results: int = 25
) -> List[Dict]:
    """
    Advanced people search with multiple filters

    Args:
        company_id: Apollo organization ID
        titles: List of job titles (optional)
        seniorities: List of seniority levels: ['vp', 'director', 'c_suite'] (optional)
        departments: List of departments: ['sales', 'marketing'] (optional)
        locations: List of locations (optional)
        max_results: Max contacts to return

    Returns:
        List of contact dicts
    """
    endpoint = f"{self.BASE_URL}/people/search"

    payload = {
        "organization_ids": [company_id],
        "page": 1,
        "per_page": max_results
    }

    # Add optional filters
    if titles:
        payload["person_titles"] = titles
    if seniorities:
        payload["person_seniorities"] = seniorities
    if departments:
        payload["person_departments"] = departments
    if locations:
        payload["person_locations"] = locations

    response = self.session.post(endpoint, json=payload)
    response.raise_for_status()

    data = response.json()

    contacts = []
    for person in data.get('people', []):
        contacts.append(self._normalize_contact(person))

    return contacts
```

### Method 2: Use in Your Enrichment

```python
# Example: Find healthcare insurance VPs
apollo = ApolloClient(api_key)
company_data = apollo.search_company("Humana")

# Get senior healthcare decision makers
contacts = apollo.search_people_advanced(
    company_id=company_data['apollo_id'],
    titles=["CMO", "VP Quality", "VP Medicare"],
    seniorities=["vp", "c_suite"],
    max_results=20
)

print(f"Found {len(contacts)} senior healthcare leaders")
for contact in contacts:
    print(f"  - {contact['name']}: {contact['title']}")
```

---

## Summary

**Precision:**
- ✅ Job titles: Very precise
- ✅ Seniority + Department: Very precise
- ✅ Location: Precise
- ⚠️  Keywords only: Less precise

**Best for:**
- Finding specific decision makers (CMO, VP Quality, etc.)
- Filtering by org level (C-suite, VP, Director only)
- Targeting specific departments (Sales, Ops, IT)
- Geographic filtering (specific cities/states)

**Result Quality:**
- Small companies: 5-15 relevant contacts
- Medium companies: 15-30 relevant contacts
- Large companies: 30-50 relevant contacts (can get more with pagination)

---

*Last updated: October 15, 2025*
