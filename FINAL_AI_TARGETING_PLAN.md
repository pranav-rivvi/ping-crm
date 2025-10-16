# AI-Powered Company Targeting - Final Simple Plan

## Core Principle: Keep It Stupid Simple

**One input, AI does everything:**
```
User: "people who make purchasing decisions for healthcare software at these companies"
AI: Figures out titles, seniority, locations → Apollo search → Notion
```

---

## Simplified UI (Single Tab)

```
┌───────────────────────────────────────────────────────┐
│ 🎯 AI-Powered Company Targeting                      │
├───────────────────────────────────────────────────────┤
│                                                        │
│ 1️⃣ Upload Companies                                  │
│    [companies.csv] ✅ Loaded 5 companies              │
│                                                        │
│ 2️⃣ Describe Who You Want to Reach                    │
│    ┌──────────────────────────────────────────────┐  │
│    │ People who make purchasing decisions for     │  │
│    │ healthcare technology at these companies     │  │
│    └──────────────────────────────────────────────┘  │
│                                                        │
│    💡 Examples:                                        │
│    • "C-suite executives"                             │
│    • "sales and marketing leaders in New York"       │
│    • "operations directors who manage supply chain"  │
│    • "people who buy enterprise software"            │
│                                                        │
│ 3️⃣ How Many People per Company?                      │
│    [1 ←───●─────→ 20]  Current: 5                    │
│                                                        │
│ 4️⃣ [🚀 Find People] [Preview AI Search Strategy]     │
│                                                        │
└───────────────────────────────────────────────────────┘

After clicking "Preview AI Search Strategy":

┌───────────────────────────────────────────────────────┐
│ 🤖 AI Search Strategy                                 │
├───────────────────────────────────────────────────────┤
│                                                        │
│ AI will search for:                                   │
│                                                        │
│ Titles:                                               │
│ • CTO, Chief Technology Officer                       │
│ • VP Technology, VP IT                                │
│ • Chief Information Officer, CIO                      │
│ • VP Digital Transformation                           │
│ • Director of IT, Director Technology                 │
│                                                        │
│ Seniority Levels:                                     │
│ • C-Suite, VP, Director                               │
│                                                        │
│ Locations (if specified):                             │
│ • United States (default if not specified)            │
│                                                        │
│ [✅ Looks Good - Start Search] [✏️ Edit Strategy]     │
│                                                        │
└───────────────────────────────────────────────────────┘
```

---

## Simple 3-File Implementation

### File 1: `src/openai_helper.py` (NEW)

**Single function that does everything:**

```python
from openai import OpenAI
import json

class AITargeting:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze_targeting_request(
        self,
        user_description: str,
        company_industry: str = None
    ) -> dict:
        """
        Convert natural language to Apollo search parameters

        Args:
            user_description: "people who buy enterprise software"
            company_industry: "Healthcare" (optional, for context)

        Returns:
            {
                "titles": ["CTO", "VP IT", "CIO", ...],
                "seniorities": ["c_suite", "vp", "director"],
                "locations": ["United States"] or None,
                "explanation": "Searching for technology decision-makers..."
            }
        """

        prompt = f"""
You are an expert at identifying job titles for B2B sales targeting.

USER REQUEST: "{user_description}"
COMPANY INDUSTRY: {company_industry or "Not specified"}

Your task:
1. Generate 10-15 specific job titles that match this request
2. Determine appropriate seniority levels
3. Extract any location requirements (or return null if none)
4. Provide a brief explanation

Return ONLY valid JSON in this exact format:
{{
  "titles": ["exact", "job", "titles"],
  "seniorities": ["c_suite", "vp", "director", "manager", "senior"],
  "locations": ["City/State/Country"] or null,
  "explanation": "Brief explanation of targeting strategy"
}}

SENIORITY OPTIONS (only use these):
- "c_suite" (CEO, CTO, CFO, etc.)
- "vp" (Vice Presidents)
- "director" (Directors)
- "manager" (Managers)
- "senior" (Senior level individual contributors)
- "entry" (Entry level)

IMPORTANT:
- Be specific with titles (not generic)
- Consider variations (VP Sales, Vice President of Sales, SVP Sales)
- If user mentions location, include it in "locations" array
- If no location mentioned, set "locations" to null
- Match seniority to the request (C-suite for execs, vp/director for leaders)

EXAMPLES:

Request: "c-suite executives"
Response:
{{
  "titles": ["CEO", "Chief Executive Officer", "COO", "Chief Operating Officer", "CFO", "Chief Financial Officer", "CTO", "Chief Technology Officer", "CMO", "Chief Marketing Officer", "CRO", "Chief Revenue Officer", "President", "Managing Director"],
  "seniorities": ["c_suite"],
  "locations": null,
  "explanation": "Targeting top-level executive decision makers across all functions"
}}

Request: "sales leaders in New York"
Response:
{{
  "titles": ["VP Sales", "Vice President of Sales", "SVP Sales", "Senior Vice President Sales", "Director of Sales", "Sales Director", "Head of Sales", "Chief Revenue Officer", "VP Business Development", "Director Business Development"],
  "seniorities": ["c_suite", "vp", "director"],
  "locations": ["New York"],
  "explanation": "Targeting senior sales leadership based in New York"
}}

Request: "people who make technology purchasing decisions"
Response:
{{
  "titles": ["CTO", "Chief Technology Officer", "VP Technology", "VP IT", "Chief Information Officer", "CIO", "VP Engineering", "Director of Technology", "Director IT", "VP Digital Transformation", "Chief Digital Officer"],
  "seniorities": ["c_suite", "vp", "director"],
  "locations": null,
  "explanation": "Targeting technology leadership who typically control software/IT budgets"
}}

Now process this request:
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cheap
            messages=[
                {"role": "system", "content": "You are a B2B sales targeting expert. Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low temp for consistency
            max_tokens=500
        )

        # Parse JSON response
        result = json.loads(response.choices[0].message.content)

        return result
```

---

### File 2: `src/apollo_client.py` (UPDATE)

**Add one new method:**

```python
def search_people_by_company(
    self,
    company_id: str,
    titles: List[str],
    seniorities: List[str] = None,
    locations: List[str] = None,
    max_results: int = 10
) -> List[Dict]:
    """
    Search for people at a specific company with filters

    Args:
        company_id: Apollo organization ID
        titles: List of job titles
        seniorities: List of seniority levels (optional)
        locations: List of locations (optional)
        max_results: Max number of people to return

    Returns:
        List of person dicts
    """
    endpoint = f"{self.BASE_URL}/people/search"

    payload = {
        "organization_ids": [company_id],
        "person_titles": titles,
        "page": 1,
        "per_page": max_results
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
```

---

### File 3: `app.py` (ADD NEW TAB)

**Simple implementation:**

```python
# At top of file, add import
from src.openai_helper import AITargeting

# In main(), add new tab
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Bulk Upload",
    "🔗 LinkedIn/Email Lookup",
    "📊 Results",
    "🎯 AI Company Targeting"  # NEW
])

with tab4:
    st.subheader("🎯 AI-Powered Company Targeting")
    st.markdown("Find the right people at target companies using natural language")

    # Initialize OpenAI (if API key provided)
    openai_key = st.text_input(
        "OpenAI API Key (optional)",
        type="password",
        help="Enables AI-powered role expansion. Get key at platform.openai.com"
    )

    if not openai_key:
        st.warning("⚠️ Enter OpenAI API key to enable AI targeting")
        st.stop()

    # CSV upload
    st.markdown("### 1️⃣ Upload Companies")
    uploaded_companies = st.file_uploader(
        "Choose CSV with company names",
        type=['csv'],
        key="companies_csv",
        help="CSV with 'company_name' column"
    )

    if uploaded_companies:
        df_companies = pd.read_csv(uploaded_companies)

        if 'company_name' not in df_companies.columns:
            st.error("❌ CSV must have 'company_name' column")
            st.stop()

        st.success(f"✅ Loaded {len(df_companies)} companies")
        st.dataframe(df_companies, use_container_width=True)

        # Natural language input
        st.markdown("### 2️⃣ Describe Who You Want to Reach")

        user_description = st.text_area(
            "Use natural language to describe your target audience",
            placeholder="Examples:\n• C-suite executives\n• Sales and marketing leaders in New York\n• People who buy enterprise software\n• Operations managers who handle supply chain",
            height=100
        )

        # Number slider
        st.markdown("### 3️⃣ How Many People per Company?")
        num_people = st.slider(
            "Number of contacts per company",
            min_value=1,
            max_value=20,
            value=5
        )

        st.info(f"📊 Expected results: ~{len(df_companies) * num_people} contacts ({len(df_companies)} companies × {num_people} each)")

        # Preview strategy button
        col1, col2 = st.columns([1, 1])

        with col1:
            preview_button = st.button("🔍 Preview AI Strategy", type="secondary", use_container_width=True)

        with col2:
            start_button = st.button("🚀 Find People", type="primary", use_container_width=True, disabled=not user_description)

        # Preview AI strategy
        if preview_button and user_description:
            with st.spinner("🤖 AI is analyzing your request..."):
                try:
                    ai = AITargeting(openai_key)

                    # Get first company's industry for context
                    if 'apollo' not in st.session_state:
                        st.session_state.apollo = ApolloClient(os.getenv('APOLLO_API_KEY'))

                    first_company = df_companies.iloc[0]['company_name']
                    company_data = st.session_state.apollo.search_company(first_company)
                    industry = company_data.get('industry', '') if company_data else ''

                    # Get AI targeting strategy
                    strategy = ai.analyze_targeting_request(user_description, industry)

                    # Store in session
                    st.session_state.ai_strategy = strategy

                    # Display strategy
                    st.markdown("### 🤖 AI Search Strategy")

                    st.markdown(f"**Explanation:** {strategy['explanation']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Job Titles:**")
                        for title in strategy['titles'][:10]:
                            st.markdown(f"• {title}")
                        if len(strategy['titles']) > 10:
                            st.markdown(f"• ... and {len(strategy['titles']) - 10} more")

                    with col2:
                        st.markdown("**Seniority Levels:**")
                        for seniority in strategy['seniorities']:
                            st.markdown(f"• {seniority.replace('_', ' ').title()}")

                        if strategy.get('locations'):
                            st.markdown("**Locations:**")
                            for loc in strategy['locations']:
                                st.markdown(f"• {loc}")

                    st.success("✅ Strategy looks good! Click 'Find People' to start.")

                except Exception as e:
                    st.error(f"❌ AI Error: {e}")

        # Start search
        if start_button and user_description:
            # Get strategy (either from preview or generate new)
            if 'ai_strategy' not in st.session_state:
                with st.spinner("🤖 Generating AI strategy..."):
                    ai = AITargeting(openai_key)

                    # Get industry context from first company
                    if 'apollo' not in st.session_state:
                        st.session_state.apollo = ApolloClient(os.getenv('APOLLO_API_KEY'))
                        st.session_state.notion = NotionClient(
                            os.getenv('NOTION_TOKEN'),
                            os.getenv('NOTION_DB_ID')
                        )

                    first_company = df_companies.iloc[0]['company_name']
                    company_data = st.session_state.apollo.search_company(first_company)
                    industry = company_data.get('industry', '') if company_data else ''

                    st.session_state.ai_strategy = ai.analyze_targeting_request(user_description, industry)

            strategy = st.session_state.ai_strategy

            # Show strategy summary
            st.markdown("### 🤖 Using AI Strategy:")
            st.info(strategy['explanation'])

            # Initialize tracking
            if 'company_results' not in st.session_state:
                st.session_state.company_results = []
                st.session_state.company_stats = {
                    'companies_processed': 0,
                    'total_found': 0,
                    'total_added': 0,
                    'total_skipped': 0
                }

            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Stats display
            col1, col2, col3, col4 = st.columns(4)
            stat_companies = col1.empty()
            stat_found = col2.empty()
            stat_added = col3.empty()
            stat_skipped = col4.empty()

            # Results display
            results_container = st.empty()

            # Process each company
            total_companies = len(df_companies)

            for idx, row in df_companies.iterrows():
                company_name = row['company_name']

                status_text.info(f"Processing {idx + 1}/{total_companies}: {company_name}")

                try:
                    # Search company
                    company_data = st.session_state.apollo.search_company(company_name)

                    if not company_data:
                        st.session_state.company_results.append({
                            'company': company_name,
                            'status': 'not_found',
                            'found': 0,
                            'added': 0,
                            'people': []
                        })
                        continue

                    # Search people with AI strategy
                    people = st.session_state.apollo.search_people_by_company(
                        company_id=company_data['apollo_id'],
                        titles=strategy['titles'],
                        seniorities=strategy['seniorities'],
                        locations=strategy.get('locations'),
                        max_results=num_people
                    )

                    # Add to Notion
                    added_count = 0
                    skipped_count = 0

                    for person in people:
                        # Check if exists
                        existing = st.session_state.notion.find_contact(
                            person['name'],
                            company_data['name']
                        )

                        if existing:
                            skipped_count += 1
                            continue

                        # Add to Notion
                        success, action = st.session_state.notion.upsert_contact(
                            contact_name=person['name'],
                            company_name=company_data['name'],
                            enriched_data=person,
                            company_data=company_data
                        )

                        if success:
                            added_count += 1

                    # Store results
                    st.session_state.company_results.append({
                        'company': company_name,
                        'status': 'success',
                        'found': len(people),
                        'added': added_count,
                        'skipped': skipped_count,
                        'people': people
                    })

                    # Update stats
                    st.session_state.company_stats['companies_processed'] += 1
                    st.session_state.company_stats['total_found'] += len(people)
                    st.session_state.company_stats['total_added'] += added_count
                    st.session_state.company_stats['total_skipped'] += skipped_count

                except Exception as e:
                    st.session_state.company_results.append({
                        'company': company_name,
                        'status': 'error',
                        'found': 0,
                        'added': 0,
                        'error': str(e),
                        'people': []
                    })

                # Update progress
                progress = (idx + 1) / total_companies
                progress_bar.progress(progress)

                # Update stats
                stat_companies.metric("Companies", st.session_state.company_stats['companies_processed'])
                stat_found.metric("Found", st.session_state.company_stats['total_found'])
                stat_added.metric("Added", st.session_state.company_stats['total_added'])
                stat_skipped.metric("Skipped", st.session_state.company_stats['total_skipped'])

                # Show recent results
                with results_container.container():
                    st.markdown("### Recent Results")
                    for result in st.session_state.company_results[-3:]:
                        if result['status'] == 'success':
                            st.success(f"✅ **{result['company']}**: Found {result['found']}, Added {result['added']}, Skipped {result['skipped']}")
                            for person in result['people'][:2]:
                                st.markdown(f"  • {person['name']} - {person.get('title', 'N/A')}")
                        elif result['status'] == 'not_found':
                            st.warning(f"⚠️ **{result['company']}**: Not found in Apollo")
                        else:
                            st.error(f"❌ **{result['company']}**: {result.get('error', 'Error')}")

                # Rate limiting
                if idx < total_companies - 1:
                    time.sleep(1.5)

            # Completion
            status_text.success("✅ All companies processed!")
            st.balloons()

            # Final summary
            st.markdown("### 🎉 Targeting Complete!")
            st.markdown(f"""
            - **Companies processed:** {st.session_state.company_stats['companies_processed']}
            - **Total people found:** {st.session_state.company_stats['total_found']}
            - **Added to Notion:** {st.session_state.company_stats['total_added']}
            - **Already existed:** {st.session_state.company_stats['total_skipped']}
            """)

            # Export option
            if st.session_state.company_results:
                # Create export DataFrame
                export_data = []
                for result in st.session_state.company_results:
                    for person in result.get('people', []):
                        export_data.append({
                            'Company': result['company'],
                            'Name': person['name'],
                            'Title': person.get('title', 'N/A'),
                            'Email': person.get('email', 'N/A'),
                            'LinkedIn': person.get('linkedin_url', 'N/A'),
                            'Location': f"{person.get('city', '')}, {person.get('state', '')}".strip(', ')
                        })

                export_df = pd.DataFrame(export_data)

                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results CSV",
                    data=csv,
                    file_name=f"ai_targeting_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

            # Reset button
            if st.button("🔄 Start New Search"):
                for key in ['company_results', 'company_stats', 'ai_strategy']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
```

---

## Environment Setup

**Update `.env.example`:**

```bash
# Required
APOLLO_API_KEY=your_apollo_key
NOTION_TOKEN=your_notion_token
NOTION_DB_ID=your_database_id

# Optional (for AI targeting)
OPENAI_API_KEY=your_openai_key
```

---

## CSV Format

**Simple one-column CSV:**

```csv
company_name
CVS Health
Humana
Elevance Health
UnitedHealth Group
Cigna
Anthem
Aetna
Kaiser Permanente
Molina Healthcare
Centene
```

---

## Example User Flows

### Flow 1: C-Suite Targeting
```
Input: "c-suite executives"
AI expands to: CEO, COO, CFO, CTO, CMO, President, etc.
Seniority: c_suite
Location: None (searches all)
Result: Top 5 C-suite from each company
```

### Flow 2: Geographic Targeting
```
Input: "sales leaders in New York and California"
AI expands to: VP Sales, Director Sales, Head of Sales, etc.
Seniority: vp, director
Location: New York, California
Result: Top 5 sales leaders in those states
```

### Flow 3: Functional Targeting
```
Input: "people who make technology purchasing decisions"
AI expands to: CTO, CIO, VP IT, VP Technology, etc.
Seniority: c_suite, vp, director
Location: None
Result: Tech decision-makers at each company
```

### Flow 4: Industry-Specific
```
Input: "healthcare operations executives"
Company: Humana (healthcare payer)
AI expands to: COO, VP Operations, VP Clinical Ops, etc.
Result: Operations leaders in healthcare
```

---

## Cost Estimate

### Per 100 Companies Search:

**Apollo:**
- 100 company lookups: ~100 credits
- 500 people searches (5 per company): ~500 credits
- Total: ~600 Apollo credits

**OpenAI:**
- 1 AI strategy call: ~$0.001 (negligible)
- Total: <$0.01

**Very affordable for conference prep!**

---

## Implementation Checklist

- [ ] Create `src/openai_helper.py` with `AITargeting` class
- [ ] Add `search_people_by_company()` to `src/apollo_client.py`
- [ ] Add new tab in `app.py`
- [ ] Update `.env.example` with OpenAI key
- [ ] Create sample `companies.csv`
- [ ] Test with 2-3 companies first
- [ ] Add error handling
- [ ] Add export functionality
- [ ] Test end-to-end

**Estimated time: 3-4 hours**

---

## Key Simplifications

1. ✅ **Single AI call** - One prompt does everything
2. ✅ **No manual filters** - AI figures out seniorities/locations
3. ✅ **Natural language only** - Users describe in plain English
4. ✅ **Preview before search** - User can validate AI strategy
5. ✅ **One CSV column** - Just company names
6. ✅ **Auto-detect industry** - Uses first company's industry for context

---

## Next Step

Ready to implement? I'll:

1. Create `src/openai_helper.py`
2. Update `src/apollo_client.py`
3. Add the new tab to `app.py`
4. Test with a few companies

**Should I start building now?**
