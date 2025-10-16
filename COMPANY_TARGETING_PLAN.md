# Company-Based Targeting Feature - Implementation Plan

## Feature Overview

**Goal:** Upload CSV of company names → Select roles & locations → Get top N people from each company → Add to Notion

**Example Use Case:**
- Upload: CVS Health, Humana, Elevance Health
- Select Roles: VP Sales, Director Marketing, Head of Operations
- Select Locations: New York, California, Remote
- Get top 5 people from each company matching criteria
- Result: 15 contacts added to Notion (5 per company)

---

## Apollo API Capabilities ✅

**Confirmed working filters:**

| Filter | Parameter | Example Values |
|--------|-----------|----------------|
| **Company** | `organization_ids` | `["company_id_1", "company_id_2"]` |
| **Job Titles** | `person_titles` | `["VP", "Director", "Head of"]` |
| **Locations** | `person_locations` | `["New York", "California", "United States"]` |
| **Seniority** | `person_seniorities` | `["c_suite", "vp", "director", "manager"]` |
| **Results** | `per_page` | `1-100` (max per request) |

**Test confirmed:** All filters work with people search endpoint.

---

## Architecture

### 1. CSV Format
```csv
company_name
CVS Health
Humana
Elevance Health
UnitedHealth Group
Cigna
```

### 2. User Interface (New Tab in Streamlit)

**Tab: "🎯 Company Targeting"**

```
┌─────────────────────────────────────────────────────┐
│ 1️⃣ Upload Companies CSV                            │
│    [Choose file: companies.csv]                     │
│    ✅ Loaded 5 companies                            │
│                                                      │
│ 2️⃣ Select Target Roles                             │
│    [Quick Presets]                                  │
│    • C-Suite Executives                             │
│    • Sales Leaders                                  │
│    • Marketing Leaders                              │
│    • Operations Leaders                             │
│    • Custom (AI-powered)                            │
│                                                      │
│    [Or enter custom roles:]                         │
│    VP Sales, Director Marketing, Head of Ops        │
│    💡 AI will expand these into variations          │
│                                                      │
│ 3️⃣ Select Locations (Optional)                     │
│    ☐ United States                                  │
│    ☐ New York                                       │
│    ☐ California                                     │
│    ☐ Texas                                          │
│    ☐ Remote                                         │
│    [+ Add custom location]                          │
│                                                      │
│ 4️⃣ Select Seniority Levels                         │
│    ☑ C-Suite                                        │
│    ☑ VP                                             │
│    ☑ Director                                       │
│    ☐ Manager                                        │
│    ☐ Senior                                         │
│                                                      │
│ 5️⃣ Number of People per Company                    │
│    [Slider: 1 ←―●―――――――――→ 20]                    │
│    Current: 5 people per company                    │
│                                                      │
│ 6️⃣ Start Search                                     │
│    [🚀 Find Decision Makers]                        │
│                                                      │
│ Expected Results: 25 contacts (5 companies × 5 each)│
└─────────────────────────────────────────────────────┘
```

### 3. OpenAI Integration (Optional but Powerful)

**Use Cases:**

#### A. Smart Role Expansion
```
User input: "sales leaders"

OpenAI expands to:
- VP Sales
- Vice President of Sales
- Director of Sales
- Head of Sales
- Chief Revenue Officer
- SVP Sales
- Sales Director
- Director Business Development
```

#### B. Custom Natural Language
```
User input: "people who make purchasing decisions for health tech software"

OpenAI suggests:
- CTO
- VP Technology
- Chief Digital Officer
- VP Innovation
- Director IT
- VP Product
- Chief Information Officer
```

#### C. Industry-Specific Titles
```
User: "decision makers for healthcare payers"
Company: Humana (detected as health insurance)

OpenAI suggests:
- CMO (Chief Medical Officer)
- VP Quality
- VP Medicare Advantage
- Director Star Ratings
- VP Member Services
- VP Clinical Operations
```

### 4. Processing Flow

```
┌──────────────────────────────────────────────────────┐
│ For Each Company:                                    │
│                                                       │
│ 1. Search Apollo for company → Get company_id       │
│ 2. Detect company industry                           │
│ 3. If AI enabled: Expand roles based on industry     │
│ 4. Search Apollo people with filters:                │
│    - organization_ids: [company_id]                  │
│    - person_titles: [expanded titles]                │
│    - person_locations: [selected locations]          │
│    - person_seniorities: [selected levels]           │
│    - per_page: N (user selected)                     │
│ 5. Get top N results                                 │
│ 6. For each person:                                  │
│    - Check if exists in Notion                       │
│    - If new → Add to Notion                          │
│    - If exists → Skip or update                      │
│ 7. Track stats per company                           │
└──────────────────────────────────────────────────────┘
```

### 5. Results Display

```
┌─────────────────────────────────────────────────────┐
│ 📊 Targeting Results                                │
│                                                      │
│ Company: CVS Health                                 │
│ ✅ Found: 5/5 people                                │
│   • Karen Lynch (CEO)                               │
│   • David Joyner (President)                        │
│   • Thomas Cowhey (CFO)                             │
│   • ... (3 more)                                    │
│                                                      │
│ Company: Humana                                     │
│ ✅ Found: 5/5 people                                │
│   • Bruce Broussard (CEO)                           │
│   • ... (4 more)                                    │
│                                                      │
│ Overall Stats:                                      │
│ • Companies processed: 5                            │
│ • Contacts found: 25                                │
│ • Added to Notion: 25                               │
│ • Already existed: 0                                │
│                                                      │
│ [📥 Download Results CSV]                           │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Basic Company Targeting (No AI)
**Estimated time: 2-3 hours**

**Features:**
- ✅ CSV upload (company names)
- ✅ Manual role input (text field)
- ✅ Location multi-select
- ✅ Seniority checkboxes
- ✅ Number slider
- ✅ Process companies → Apollo search → Notion write
- ✅ Progress tracking
- ✅ Results export

**Files to create:**
- Update `src/apollo_client.py` - Add `search_people_advanced()` method
- Update `app.py` - Add new tab "Company Targeting"
- Update `src/notion_client.py` - Handle bulk writes efficiently

### Phase 2: Role Presets
**Estimated time: 1 hour**

**Features:**
- ✅ Predefined role templates:
  - C-Suite: CEO, COO, CFO, CTO, CMO, etc.
  - Sales Leaders: VP Sales, Director Sales, etc.
  - Marketing Leaders: VP Marketing, CMO, etc.
  - Operations: VP Ops, Director Ops, etc.
- ✅ One-click selection

### Phase 3: OpenAI Smart Expansion
**Estimated time: 2 hours**

**Features:**
- ✅ Natural language role input
- ✅ AI expands roles to variations
- ✅ Industry-aware suggestions
- ✅ Custom targeting descriptions

**OpenAI Integration:**
```python
def expand_roles_with_ai(user_input, company_industry):
    """
    Use OpenAI to expand role descriptions into specific titles

    Args:
        user_input: "sales decision makers"
        company_industry: "Healthcare"

    Returns:
        ["VP Sales", "Director Sales", "Chief Revenue Officer", ...]
    """
    prompt = f"""
    Company Industry: {company_industry}
    User wants to target: {user_input}

    Generate a list of 10-15 specific job titles that match this description.
    Focus on decision-makers and influencers in this industry.
    Return as a Python list.
    """

    # Call OpenAI API
    # Parse response
    # Return expanded titles
```

---

## API Cost Analysis

### Apollo Credits
**People search:** Uses search credits

**Example scenario:**
- 10 companies × 5 people each = 50 searches
- Cost: ~50 credits (depends on your Apollo plan)

### OpenAI Costs (If Used)
**GPT-4o-mini:** ~$0.15 per 1M input tokens

**Example scenario:**
- 100 role expansions per session
- ~200 tokens per expansion
- Cost: ~$0.003 (negligible)

**Recommendation:** Use GPT-4o-mini for cost efficiency.

---

## Detailed Code Structure

### 1. New Method: `search_people_advanced()`

**File:** `src/apollo_client.py`

```python
def search_people_advanced(
    self,
    company_ids: List[str],
    titles: List[str] = None,
    locations: List[str] = None,
    seniorities: List[str] = None,
    max_results_per_company: int = 10
) -> Dict[str, List[Dict]]:
    """
    Search for people across multiple companies with advanced filters

    Args:
        company_ids: List of Apollo organization IDs
        titles: List of job titles (e.g., ["VP", "Director"])
        locations: List of locations (e.g., ["New York", "California"])
        seniorities: List of seniority levels (e.g., ["c_suite", "vp"])
        max_results_per_company: Max people to return per company

    Returns:
        {
            "company_id_1": [person1, person2, ...],
            "company_id_2": [person1, person2, ...],
        }
    """
```

### 2. OpenAI Role Expander

**File:** `src/openai_helper.py` (NEW)

```python
from openai import OpenAI

class RoleExpander:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def expand_roles(
        self,
        role_description: str,
        industry: str = None,
        count: int = 15
    ) -> List[str]:
        """Expand role description into specific job titles"""

    def get_preset_roles(self, preset_name: str) -> List[str]:
        """Get predefined role lists"""
```

### 3. UI Component

**File:** `app.py`

```python
with tab4:  # New tab: Company Targeting
    st.subheader("🎯 Find Decision Makers at Target Companies")

    # CSV upload
    uploaded_companies = st.file_uploader(...)

    # Role selection
    role_input_method = st.radio(
        "How do you want to select roles?",
        ["Preset Templates", "Custom List", "AI-Powered (Natural Language)"]
    )

    if role_input_method == "Preset Templates":
        preset = st.selectbox(...) # C-Suite, Sales, Marketing, etc.

    elif role_input_method == "Custom List":
        roles = st.text_area(...)

    else:  # AI-Powered
        natural_language = st.text_input(
            "Describe who you want to reach",
            "People who make purchasing decisions for healthcare software"
        )

    # Location filter
    locations = st.multiselect(...)

    # Seniority filter
    seniorities = st.multiselect(...)

    # Number per company
    num_people = st.slider(...)

    # Process button
    if st.button("Find Decision Makers"):
        # Process companies
        # Show progress
        # Display results
```

---

## Sample Presets

### C-Suite Executives
```python
[
    "CEO", "Chief Executive Officer",
    "COO", "Chief Operating Officer",
    "CFO", "Chief Financial Officer",
    "CTO", "Chief Technology Officer",
    "CMO", "Chief Marketing Officer",
    "CRO", "Chief Revenue Officer",
    "President", "Managing Director"
]
```

### Sales Leaders
```python
[
    "VP Sales", "Vice President of Sales",
    "SVP Sales", "Senior Vice President Sales",
    "Director of Sales", "Sales Director",
    "Head of Sales", "Chief Revenue Officer",
    "VP Business Development", "Director Business Development"
]
```

### Marketing Leaders
```python
[
    "CMO", "Chief Marketing Officer",
    "VP Marketing", "Vice President Marketing",
    "Director of Marketing", "Marketing Director",
    "Head of Marketing", "VP Brand",
    "VP Digital Marketing", "VP Growth"
]
```

### Operations Leaders
```python
[
    "COO", "Chief Operating Officer",
    "VP Operations", "Vice President Operations",
    "Director of Operations", "Operations Director",
    "VP Supply Chain", "Head of Operations",
    "VP Strategy", "Chief Strategy Officer"
]
```

### Healthcare-Specific (For Payers)
```python
[
    "CMO", "Chief Medical Officer",
    "VP Quality", "VP Medicare",
    "VP Medicare Advantage", "Director Star Ratings",
    "VP Member Services", "VP Clinical Operations",
    "VP Care Management", "VP Population Health"
]
```

---

## Error Handling

### Scenarios to Handle:
1. **Company not found in Apollo**
   - Log warning
   - Skip to next company
   - Show in results

2. **No people match criteria**
   - Show "0 found" for that company
   - Suggest broadening filters

3. **Rate limiting**
   - Add delays between companies
   - Show progress clearly
   - Allow pause/resume

4. **Duplicate detection**
   - Check Notion before adding
   - Option to update or skip

---

## Benefits of This Feature

1. **Time Savings**
   - Manual: 30 minutes per company to find 5 decision makers
   - Automated: 5 seconds per company
   - **For 20 companies:** 10 hours → 2 minutes

2. **Better Targeting**
   - Filter by exact roles needed
   - Geographic targeting
   - Seniority level filtering
   - Industry-specific roles (with AI)

3. **Scale**
   - Process 100+ companies in one batch
   - Consistent criteria across all companies
   - Track all results in Notion

4. **Conference Prep**
   - Upload exhibitor list
   - Get key contacts at each company
   - Personalized outreach before event

---

## Next Steps

**Option 1: Basic Implementation (Fastest)**
- Manual role input
- No AI, just Apollo filters
- 2-3 hours to implement

**Option 2: With Presets (Recommended)**
- Predefined role templates
- Quick selection
- 3-4 hours to implement

**Option 3: Full AI-Powered (Most Powerful)**
- Natural language role descriptions
- Industry-aware suggestions
- Smart title expansion
- 5-6 hours to implement

---

## Question for You

Which implementation do you prefer?

1. **Start Simple** - Basic company targeting with manual roles
2. **Add Presets** - Include role templates for quick selection
3. **Go Full AI** - Complete OpenAI integration for smart targeting

I can start with any of these and iterate from there. What works best for your HLTH 2025 timeline?
