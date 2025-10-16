# Email-Based Enrichment Guide

## Overview
You can now enrich contacts using **email addresses** in addition to name + company searches.

---

## Methods Available

### 1. Single Email Lookup (UI Tab 2)
**Location:** Streamlit UI → "🔗 LinkedIn/Email Lookup" tab

**How to Use:**
1. Open http://localhost:8501
2. Go to "LinkedIn/Email Lookup" tab
3. Paste email address (e.g., `karen@cvshealth.com`)
4. Click "🔍 Get Details"
5. Review enriched data
6. Click "➕ Add to Notion"

**What You Get:**
- Full contact profile from Apollo
- Company information
- LinkedIn URL (if available)
- Title, seniority, location
- Automatic duplicate detection

---

### 2. Bulk Email Enrichment (UI Tab 1)
**Location:** Streamlit UI → "📤 Bulk Upload" tab

**CSV Format:**
```csv
email
karen@cvshealth.com
bruce@humana.com
gail@elevancehealth.com
```

**How to Use:**
1. Create CSV with single `email` column
2. Upload to "Bulk Upload" tab
3. System auto-detects EMAIL mode
4. Click "🚀 Start Enrichment"
5. Watch live progress
6. Export results

**Features:**
- Auto-detection of CSV format
- Live progress tracking
- Rate limiting (0.5-5s delay)
- Results export
- Duplicate handling

---

### 3. Programmatic Email Search
**For Developers:**

```python
from src.apollo_client import ApolloClient
from src.notion_client import NotionClient

# Initialize
apollo = ApolloClient(api_key)
notion = NotionClient(token, db_id)

# Search by email
person_data, company_data = apollo.search_by_email("email@company.com")

# Add to Notion
if person_data:
    success, action = notion.upsert_contact(
        contact_name=person_data['name'],
        company_name=company_data['name'] if company_data else '',
        enriched_data=person_data,
        company_data=company_data
    )
```

---

## CSV Format Options

### Option 1: Name + Company
```csv
person_name,company_name
Karen Lynch,CVS Health
Bruce Broussard,Humana
```

### Option 2: Email Only
```csv
email
karen@cvshealth.com
bruce@humana.com
```

**Note:** CSV must have **either** format, not both.

---

## How It Works

### Apollo Email Search
- Uses Apollo's People Search API
- Searches by `q_keywords` parameter with email
- Returns contact + company data
- No company lookup needed (included in response)

### Notion Integration
- Checks for existing contacts (by name + company)
- Creates new contact or updates existing
- Populates all standard fields:
  - Contact Name
  - Company
  - Title
  - Email
  - LinkedIn URL (validated)
  - City, State, Country
  - Seniority
  - Relationship Type (auto-tagged)

---

## Templates

Download CSV templates from the sidebar:
- **📄 Name + Company** - Traditional format
- **📧 Email Only** - Email enrichment format

---

## When to Use Email vs Name

### Use Email When:
- You have email lists from events/conferences
- More accurate than fuzzy name matching
- Direct lookup (faster)
- Email is the unique identifier

### Use Name + Company When:
- You don't have email addresses
- Building prospect lists from research
- Email not available in Apollo

---

## API Details

### Apollo Endpoint
```
POST https://api.apollo.io/v1/people/search
```

### Request Payload
```json
{
  "q_keywords": "email@company.com",
  "page": 1,
  "per_page": 1
}
```

### Response
Returns person object with:
- Personal info (name, title, email, phone)
- LinkedIn URL
- Location (city, state, country)
- Seniority level
- Organization object (company data)

---

## Error Handling

**Email Not Found:**
- Returns status: "failed"
- Message: "Email not found in Apollo"
- No Notion write occurs

**Already Exists:**
- Returns status: "skipped"
- Message: "Already exists in Notion"
- Can force update via UI checkbox

**API Errors:**
- Automatic retry (3 attempts with exponential backoff)
- Error logged in results
- Processing continues to next email

---

## Best Practices

1. **Rate Limiting**: Use 1.5-2s delay for bulk uploads
2. **Data Quality**: Emails must be in Apollo database
3. **Duplicates**: System checks before writing
4. **Validation**: Only valid LinkedIn URLs saved
5. **Exports**: Download results for record-keeping

---

## Testing

Test email search:
```bash
python scripts/test_email_search.py
```

Test samples provided:
- `sample_contacts.csv` - Name + Company format
- `sample_emails.csv` - Email format

---

## Troubleshooting

**"Email not found"**
- Email may not be in Apollo's database
- Try name + company search instead
- Check spelling of email

**Rate limiting errors**
- Increase delay slider in sidebar
- Reduce batch size
- Wait before retrying

**Notion write fails**
- Check Notion token/permissions
- Verify database ID
- Check field mappings

---

## Summary

**3 Ways to Enrich:**
1. Single person: Name + Company (Tab 1 or CLI)
2. Single person: LinkedIn/Email (Tab 2)
3. Bulk upload: CSV with names OR emails (Tab 1)

**All methods:**
- Search Apollo.io
- Enrich with full data
- Sync to Notion CRM
- Handle duplicates
- Track results
