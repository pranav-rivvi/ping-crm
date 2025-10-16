# 5-Minute Quick Start

Get your CRM running in 5 minutes!

---

## Step 1: Install Dependencies (1 min)

```bash
cd HLTH2025_CRM
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step 2: Get API Keys (2 min)

### Apollo.io
1. Go to https://app.apollo.io/#/settings/integrations/api
2. Copy your API key
3. Paste into `.env` file

### Notion
1. Go to https://www.notion.so/my-integrations
2. Create integration named "HLTH CRM"
3. Copy the token (starts with `secret_`)
4. Paste into `.env` file

---

## Step 3: Setup Notion Database (2 min)

1. Create new Notion page
2. Add table database
3. Add these properties:

**Required columns** (in this order):
- Company Name (Title) - already there
- Status (Select) - add options: Not Contacted, Email Sent, Replied, Meeting Booked
- Industry (Select) - add options: Insurance / Payer, Healthcare Provider / Health System, Pharmacy / PBM, Pharma / Biotech, Other
- Tier (Select) - add options: Tier 1 - AEP Urgent, Tier 2 - Strategic, Tier 3 - Proven Vertical, Tier 4 - Exploratory
- Priority Score (Number)
- Company Website (URL)
- Company LinkedIn (URL)
- Company Size (Select) - add options: 1-50, 51-200, 201-1000, 1000-5000, 5000+, Unknown
- Location (Text)
- Revenue Range (Select) - add options: <$1M, $1-10M, $10-50M, $50-200M, $200M+, Unknown
- Funding Stage (Select) - add options: Seed, Series A, Series B, Series C+, Public, Private, Unknown
- Primary Contact Name (Text)
- Primary Contact Title (Text)
- Primary Contact Email (Email)
- Primary Contact LinkedIn (URL)
- Secondary Contact Name (Text)
- Secondary Contact Title (Text)
- Secondary Contact Email (Email)
- Tertiary Contact Name (Text)
- Tertiary Contact Title (Text)
- Tertiary Contact Email (Email)
- Enrichment Date (Date)
- Apollo ID (Text)

4. Click "..." → Connections → Connect to "HLTH CRM"
5. Copy database ID from URL (32-char string)
6. Paste into `.env` file

---

## Step 4: Configure Environment

```bash
cp .env.example .env
nano .env
```

Fill in:
```bash
APOLLO_API_KEY=your_key_here
NOTION_TOKEN=secret_your_token_here
NOTION_DB_ID=your_database_id_here
```

---

## Step 5: Create Company List

Create `companies.csv`:
```csv
company_name
UnitedHealth Group
Humana
Cigna
```

---

## Step 6: Run!

```bash
python enrich.py companies.csv
```

**That's it!** Watch the magic happen. ✨

---

## Next Steps

- Check your Notion database for results
- Add more companies to CSV and re-run
- Filter by Priority Score > 7 for high-value prospects
- Create views in Notion by Tier or Status

---

## Need Help?

See full documentation:
- [README.md](README.md) - Full usage guide
- [NOTION_SETUP.md](NOTION_SETUP.md) - Detailed Notion setup
- `quick_CRM_Plan.txt` - Full architecture docs
