# Schema Adaptation Summary

## Overview

Successfully adapted the CRM enrichment system to work with your existing **contact-centric** Notion database instead of creating a new company-centric database.

---

## What Was Done

### 1. Schema Analysis

**Your Existing Database Schema:**
- **Database Name**: HLTH Conference Outreach Tracker
- **Primary Entity**: Individual contacts/people
- **Title Field**: "Contact Name" (person's name)
- **Company Field**: "Company" (text field)

**Existing Fields:**
- Contact Name (title)
- Company (rich_text)
- Email (email)
- Phone (phone_number)
- LinkedIn (url)
- Title (rich_text) - job title
- Industry (select)
- Outreach Status (status)
- Meeting Date/Time (date)
- Meeting Location (rich_text)
- Relationship Type (select)
- Notes (rich_text)

### 2. Code Adaptation

**Created**: `src/notion_sync_adapted.py`

**Key Changes:**
- **Creates one page per contact** instead of one page per company
- Maps to your existing field structure
- Stores enrichment data (tier, priority, company info) in the **Notes** field
- Handles duplicate detection by contact name + company name

**Field Mapping:**
| Apollo Data | Your Notion Field | Notes |
|-------------|-------------------|-------|
| Contact name | Contact Name (title) | ✓ Main identifier |
| Company name | Company (text) | ✓ From company_data |
| Contact email | Email | ✓ If available |
| Contact phone | Phone | ✓ If available |
| LinkedIn URL | LinkedIn | ✓ Contact LinkedIn |
| Job title | Title | ✓ Contact's position |
| Industry | Industry | ✓ Mapped to your options |
| - | Outreach Status | Set to "Not started" |
| Enrichment data | Notes | Tier, priority, company details |

**Industry Mapping:**
Apollo industries are intelligently mapped to your existing options:
- Insurance/Payer → "Insurance"
- Hospital/Health System → "Hospital & Health Systems"
- Pharma → "Pharma"
- Biotech → "Biotech"
- Medical Devices → "Medical Devices"
- Digital Health/Health Tech → "Digital Health"
- Telehealth → "Telehealth"
- Health Services → "Health Services"
- Default → "Healthcare Tech"

### 3. Updated Files

**Modified:**
- `scripts/enrich.py` - Now imports `notion_sync_adapted` and uses `create_contact_pages()`

**Created:**
- `src/notion_sync_adapted.py` - Adapted Notion client
- `scripts/inspect_notion_db.py` - Database schema inspector
- `scripts/test_enrichment.py` - End-to-end enrichment tester

**Original files preserved:**
- `src/notion_sync.py` - Original company-centric version (kept for reference)

---

## How It Works Now

### Enrichment Flow

1. **Search Company** in Apollo.io
   - Get company profile (industry, size, revenue, location, etc.)

2. **Find Decision Makers**
   - Search for relevant job titles based on industry
   - Get up to 10 contacts per company

3. **Calculate Metrics**
   - Assign tier (1-4) based on industry and company profile
   - Calculate priority score (1-10) based on size, revenue, contacts

4. **Sync to Notion**
   - Create **one page per contact** (not per company)
   - Fill in: Contact Name, Company, Email, Phone, LinkedIn, Title, Industry
   - Set "Outreach Status" to "Not started"
   - Add enrichment data to "Notes" field

### Example Result

For company "UnitedHealth Group":
- **5 contacts found** → **5 new pages created**
- Each page has:
  - Contact Name: "Laura Karkula"
  - Company: "UnitedHealth Group"
  - Title: "Vice President, Population Health"
  - Industry: "Hospital & Health Systems"
  - Outreach Status: "Not started"
  - Notes: Contains tier, priority, company size, revenue, location, etc.

---

## How to Use

### 1. Test with Single Company

```bash
source venv/bin/activate
python scripts/test_enrichment.py "UnitedHealth Group"
```

This will:
- Search Apollo for the company
- Find decision makers
- Show preview of contacts
- Ask for confirmation before syncing
- Create pages in Notion

### 2. Enrich Multiple Companies

**Step 1**: Create `companies.csv`
```csv
company_name
UnitedHealth Group
CVS Health
Anthem
Cigna
Humana
```

**Step 2**: Run enrichment
```bash
source venv/bin/activate
python scripts/enrich.py companies.csv
```

The script will:
- Process each company
- Find 5-10 decision makers per company
- Create contact pages in Notion
- Show progress and summary

### 3. Inspect Database Schema

```bash
source venv/bin/activate
python scripts/inspect_notion_db.py
```

Shows:
- All database properties
- Property types
- Select field options
- Validation against code expectations

---

## What You Get

### Enriched Contact Data

Each contact page in your Notion database will have:

**Basic Info:**
- Full name
- Company name
- Job title
- Email (if available from Apollo)
- Phone (if available)
- LinkedIn profile

**Enrichment Data (in Notes):**
```
🎯 Enrichment Data (Auto-generated 2025-10-15)

Tier: Tier 3 - Proven Vertical
Priority Score: 9/10

Website: https://unitedhealthgroup.com
Company LinkedIn: https://linkedin.com/company/...
Company Size: 5000+ (400000 employees)
Location: Phoenix, Arizona, United States
Revenue: $200M+

Apollo ID: 5f7b8c9d...
```

**Your Existing Workflow Fields:**
- Outreach Status: "Not started" (ready for you to track)
- Meeting Date/Time: Empty (ready for you to schedule)
- Meeting Location: Empty
- Relationship Type: Empty (you can categorize)

---

## Important Notes

### Apollo Email Access

Apollo shows `email_not_unlocked@domain.com` for emails you haven't unlocked with credits.

**Options:**
1. **Use LinkedIn URLs** - Reach out via LinkedIn (no credits needed)
2. **Unlock emails in Apollo** - When you need to email someone
3. **Upgrade Apollo plan** - For more email credits

The contacts are still valuable even without emails!

### Duplicate Prevention

The system checks before creating pages:
- Looks for existing contact name + company combination
- Skips if already exists
- You can safely re-run enrichment without creating duplicates

### Rate Limiting

Built-in rate limiting to respect API limits:
- 1.5 second delay between companies
- Retry logic with exponential backoff
- Graceful error handling

---

## Validation Results

✅ **All connections working:**
- Apollo.io API: Connected
- Notion API: Connected

✅ **Test enrichment successful:**
- Company search: Working
- Contact search: Working
- Tier assignment: Working
- Priority scoring: Working
- Notion sync: Working

✅ **Code validation:**
- No syntax errors
- All imports working
- Schema properly adapted
- Field mapping tested

---

## Next Steps

### Ready to Use

1. **Create your company list**: `companies.csv` with target companies
2. **Run enrichment**: `python scripts/enrich.py companies.csv`
3. **Review in Notion**: Check your database for new contacts
4. **Start outreach**: Use Outreach Status to track progress

### Optional Enhancements

**Add to Notion** (if desired):
- Tier field (select) - for filtering by tier
- Priority Score field (number) - for sorting
- Company Website field (url) - quick access
- Company Size field (select) - for filtering

Currently these are in the Notes field, but you can add dedicated fields if you want to filter/sort by them.

### Future Features

**Potential additions:**
- Email enrichment service (Hunter.io, Clearbit)
- Automatic LinkedIn URL scraping
- Meeting scheduler integration
- Email template generator
- Follow-up reminders
- Analytics dashboard

---

## File Structure

```
HLTH2025_CRM/
├── src/
│   ├── apollo_client.py           # ✅ Fixed Apollo authentication
│   ├── notion_sync.py             # Original (company-centric)
│   ├── notion_sync_adapted.py     # ✅ NEW: Adapted for your schema
│   └── processors.py              # Tier & priority logic
│
├── scripts/
│   ├── enrich.py                  # ✅ Updated: Uses adapted sync
│   ├── test_enrichment.py         # ✅ NEW: Single company test
│   ├── inspect_notion_db.py       # ✅ NEW: Schema inspector
│   ├── test_connections.py        # API connection test
│   └── validate_setup.py          # System validation
│
├── .env                            # ✅ Fixed: Removed quotes
└── companies.csv                   # Create this with your targets
```

---

## Issues Fixed

### 1. Apollo.io Authentication ✅
**Problem**: API returned 422 error
**Cause**: Apollo changed to header-based auth
**Fix**: Added `X-Api-Key` header, removed from request body
**Status**: RESOLVED

### 2. Notion Schema Mismatch ✅
**Problem**: Code expected company-centric, database is contact-centric
**Cause**: Different use case assumptions
**Fix**: Created adapted client for existing schema
**Status**: RESOLVED

### 3. .env File Format ✅
**Problem**: API keys had quotes
**Cause**: User added quotes (not needed)
**Fix**: Removed quotes from all keys
**Status**: RESOLVED

---

## Summary

✅ **System is ready to use**
✅ **All APIs connected and working**
✅ **Code adapted to your existing database**
✅ **End-to-end flow tested successfully**
✅ **Enrichment preserves your existing workflow**

You can now:
1. ✅ Test with single company: `python scripts/test_enrichment.py "Company Name"`
2. ✅ Enrich company list: `python scripts/enrich.py companies.csv`
3. ✅ Track outreach in your existing Notion database

---

**Last validated**: October 15, 2025
**System status**: 🟢 Fully operational
