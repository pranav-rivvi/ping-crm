# What You Need to Provide

## ✅ System Ready

Your Mac is fully set up and ready! Here's what we've validated:

- ✓ Python 3.13.5 installed
- ✓ Virtual environment created
- ✓ All dependencies installed
- ✓ All code validated and working

---

## 🔑 API Keys Required

You need to provide 3 API keys. Here's how to get them:

### 1. Apollo.io API Key

**What it does**: Finds company information and decision-maker contacts

**How to get it**:
1. Go to https://app.apollo.io
2. Sign up for a free account (or log in)
3. Navigate to Settings → Integrations → API
4. Copy your API key
5. **Free tier**: 50 credits/month (sufficient for testing ~10-20 companies)

**Paste into `.env` as**: `APOLLO_API_KEY=your_key_here`

---

### 2. Notion Integration Token

**What it does**: Syncs enriched data to your Notion database

**How to get it**:
1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Name it: "HLTH 2025 CRM"
4. Select your workspace
5. Click "Submit"
6. Copy the "Internal Integration Token" (starts with `secret_`)

**Paste into `.env` as**: `NOTION_TOKEN=secret_your_token_here`

---

### 3. Notion Database ID

**What it does**: Identifies where to sync your data

**How to get it**:
1. Open Notion and create a new page called "HLTH 2025 Outreach"
2. Add a table database (type `/database` → select "Table - Inline")
3. Add all required properties (see `NOTION_SETUP.md` for full list)
4. Connect your integration:
   - Click "..." (three dots) in top right
   - Go to "Connections"
   - Select "HLTH 2025 CRM"
5. Open database as full page
6. Look at the URL in your browser:
   ```
   https://www.notion.so/workspace/DATABASE_ID?v=VIEW_ID
   ```
7. Copy the 32-character string (DATABASE_ID)

**Paste into `.env` as**: `NOTION_DB_ID=your_database_id_here`

---

## 📄 CSV File Required

Create a file called `companies.csv` with this format:

```csv
company_name
UnitedHealth Group
Humana
Cigna
CVS Health
Elevance Health
```

**Requirements**:
- Must have header row with `company_name`
- One company per line
- Use full legal names for best Apollo.io matches

---

## 🚀 Setup Steps

### Step 1: Create .env File

```bash
cd /Users/pranavarora99/Desktop/HLTH2025_CRM
cp .env.example .env
nano .env  # or use any text editor
```

Add your 3 API keys:
```bash
APOLLO_API_KEY=your_apollo_key_here
NOTION_TOKEN=secret_your_notion_token_here
NOTION_DB_ID=your_database_id_here
```

Save and exit (Ctrl+X, then Y, then Enter if using nano)

### Step 2: Setup Notion Database

Follow the detailed guide in `NOTION_SETUP.md` to:
- Create the database with all required properties
- Connect your integration
- Get the database ID

### Step 3: Create companies.csv

```bash
nano companies.csv
```

Add your company list (see format above)

### Step 4: Validate Setup

```bash
source venv/bin/activate
python validate_setup.py
```

You should see:
```
✓ All checks passed!
You're ready to run: python enrich.py companies.csv
```

### Step 5: Run Enrichment

```bash
source venv/bin/activate
python enrich.py companies.csv
```

---

## 📊 Expected Results

After running, your Notion database will have:

**For each company**:
- Company name, industry, size, revenue, location
- LinkedIn and website URLs
- Top 3 decision-maker contacts with emails
- Auto-assigned tier (1-4)
- Priority score (1-10)
- Enrichment timestamp

**Processing time**: ~5-10 seconds per company (with rate limiting)

---

## 💰 API Credit Usage

### Apollo.io Free Tier
- **50 credits/month** free
- **1 credit per company search**
- **1 credit per contact email reveal** (we limit to 5 per company)
- **Estimated**: ~6-10 credits per company
- **Free tier capacity**: ~5-10 companies/month

**Tip**: Start with 3-5 test companies before buying credits

### Notion
- **Free forever** for personal use
- Unlimited API calls
- No credit limits

---

## ⚠️ Important Notes

1. **Apollo.io Credits**: Monitor your usage at https://app.apollo.io/#/settings/credits

2. **Notion Database**: Must be created BEFORE running the script

3. **Company Names**: Use exact legal names for best results:
   - ✓ "UnitedHealth Group"
   - ✗ "UnitedHealthcare"
   - ✓ "Cigna"
   - ✗ "Cigna Health"

4. **Rate Limiting**: Script includes 1.5-second delays between companies

5. **Duplicates**: Automatically skips companies already in Notion

---

## 🔧 Troubleshooting

### "Error: Missing required environment variables"
→ Your `.env` file is missing or incomplete. Check all 3 keys are filled in.

### "Company not found in Apollo"
→ Try the full legal name. Check Apollo.io directly to see how they list the company.

### "Notion API error"
→ Make sure you connected your integration to the database (Step 4 in Notion setup)

### "Database ID invalid"
→ Double-check you copied the full 32-character ID from the URL (no spaces)

---

## 📞 Need Help?

1. Run validation: `python validate_setup.py`
2. Check detailed guides:
   - `NOTION_SETUP.md` - Notion database setup
   - `README.md` - Full documentation
   - `QUICKSTART.md` - 5-minute quick start
3. Verify API keys work by logging into Apollo.io and Notion

---

**You're all set!** Just provide the 3 API keys and you're ready to enrich your HLTH 2025 prospects.
