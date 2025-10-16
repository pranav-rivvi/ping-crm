# 🚀 Quick Start Guide - For New Users
**Get started with HLTH 2025 CRM in 5 minutes**

---

## Welcome! 👋

This CRM helps you:
- 🎯 **AI Company Targeting** - Find decision-makers at target companies
- 👥 **Bulk Enrichment** - Enrich contact lists from CSV
- 💼 **Quick Lookup** - Search single contacts by LinkedIn/Email
- 📊 **Auto-sync to Notion** - All data flows to your Notion database

---

## 📋 What You Need

1. **API Keys** (get these first):
   - ✅ Apollo.io API key
   - ✅ Notion integration token
   - ✅ Notion database ID
   - ✅ OpenAI API key (or Gemini)

2. **5 minutes** to set up

---

## 🔑 Step 1: Get Your API Keys

### Apollo.io API Key

1. Go to: https://app.apollo.io/#/settings/integrations/api
2. Sign in to your Apollo account
3. Click **"Create API Key"**
4. Copy the key (looks like: `abc123...`)
5. **Save it somewhere safe!**

**Cost**: Apollo subscription required ($49-79/month per user)

---

### Notion Integration Token

1. Go to: https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Name it: "HLTH 2025 CRM"
4. Select your workspace
5. Click **"Submit"**
6. Copy the **"Internal Integration Secret"** (starts with `secret_`)
7. **Save it!**

---

### Notion Database ID

1. Open your **Notion CRM database** in browser
2. Look at the URL: `https://www.notion.so/workspace/DATABASE_ID?v=...`
3. Copy the `DATABASE_ID` part (32 characters, mix of letters/numbers)
4. Example: `abc123def456...`
5. **Save it!**

**Important**: Share your database with the integration:
- Open your Notion database
- Click **"..."** menu → **"Add connections"**
- Select **"HLTH 2025 CRM"** integration
- Click **"Confirm"**

---

### OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign in (or create account)
3. Click **"+ Create new secret key"**
4. Name it: "HLTH CRM"
5. Copy the key (starts with `sk-`)
6. **Save it!**

**Cost**: ~$0.50-$2/month (GPT-4o-mini is very cheap)

---

## 🌐 Step 2: Access the App

### If Using Streamlit Cloud (Deployed App)

1. Go to: **[YOUR_APP_URL_HERE]**
   (Your friend will give you this link)

2. Sign in (if it's a private app):
   - Use GitHub, Google, or email
   - You'll need an invite from the app owner

3. **That's it!** The app loads in your browser

---

### If Running Locally (On Your Computer)

1. **Clone the repo**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hlth-2025-crm.git
   cd hlth-2025-crm
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API keys**:
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
   - Edit `.streamlit/secrets.toml` and paste your keys:

   ```toml
   APOLLO_API_KEY = "your_apollo_key_here"
   NOTION_TOKEN = "your_notion_token_here"
   NOTION_DB_ID = "your_notion_db_id_here"
   OPENAI_API_KEY = "your_openai_key_here"
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**: http://localhost:8501

---

## ⚙️ Step 3: Configure Your API Keys (Cloud Deployment)

If using deployed app on Streamlit Cloud:

1. **Go to app settings** (click ⚙️ icon in top-right)

2. **Navigate to "Secrets"** tab

3. **Paste this** (with your actual keys):

```toml
APOLLO_API_KEY = "your_apollo_key"
NOTION_TOKEN = "secret_your_notion_token"
NOTION_DB_ID = "your_database_id"
OPENAI_API_KEY = "sk-your_openai_key"
```

4. **Click "Save"**

5. **Reload the app**

---

## 🎯 Step 4: Start Using It!

### Feature 1: AI Company Targeting

**Use case**: Find C-suite executives at healthcare companies

1. Go to **"AI Company Targeting"** tab
2. Enter what you're looking for:
   ```
   C-suite executives for partnership discussions at HLTH 2025
   ```
3. Add companies:
   - Single company: Type "CVS Health" or paste website URL
   - OR upload CSV with company names
4. Click **"Find & Add to Notion"**
5. Watch it work! 🚀

Results appear in your Notion database automatically.

---

### Feature 2: Bulk Enrichment

**Use case**: Enrich a list of contacts from LinkedIn/email

1. Go to **"Enrich Profiles"** tab
2. Upload CSV with contacts:
   - Must have: `linkedin_url`, `email`, or `person_name` + `company_name`
   - Download template if needed
3. Preview your data
4. Click **"Start Enrichment"**
5. Watch progress bar! 📊

---

### Feature 3: Quick Single Lookup

**Use case**: Look up one person fast

1. Go to **"Enrich Profiles"** tab
2. Scroll to **"Quick Single Lookup"**
3. Enter LinkedIn URL or email
4. Click **"Get Details"**
5. Review their info
6. Click **"Add to Notion"** if you want to save

---

## 💡 Pro Tips

### Get Better Results
- **Be specific** in AI targeting descriptions
- Use fewer contacts per company (3-5) for better quality
- Let the rate limiting work (prevents API errors)

### CSV Formatting
- **Always use headers** in CSVs
- **LinkedIn URLs**: Full profile URLs work best
- **Companies**: Just company names (no "Inc.", "LLC", etc.)

### Notion Setup
- Create a **dedicated database** for CRM contacts
- Use **properties** for all fields (email, phone, title, etc.)
- **Share the database** with your Notion integration

### Cost Management
- **OpenAI**: ~$0.0001 per contact (super cheap)
- **Apollo**: Respect rate limits to avoid extra charges
- **Notion**: Free tier is fine

---

## 🐛 Troubleshooting

### "Missing API keys"
**Fix**: Add keys in Settings → Secrets (see Step 3 above)

### "Not found in Apollo"
**Reasons**:
- Person doesn't exist in Apollo database
- LinkedIn URL is incorrect
- Email address is wrong
**Fix**: Try different search method (name + company)

### "Already exists in Notion"
**Reason**: Contact is already in your database
**Fix**: This is intentional! App prevents duplicates

### "Rate limit error"
**Reason**: Apollo API limit hit (5 requests/second)
**Fix**: App has built-in delays. If still happens, increase delay in Settings

### "App is slow on first load"
**Reason**: Free Streamlit Cloud apps sleep after 7 days
**Fix**: First request wakes it up (~30 sec). Then it's fast!

---

## 📊 Understanding Results

### Success Metrics

After running AI targeting, you'll see:
- **Companies processed**: How many companies searched
- **Total found**: How many people found
- **Added to Notion**: How many new contacts added
- **Already existed**: How many duplicates skipped

### Export Data

- Click **"Download Results CSV"** to export
- Contains all found contacts with details
- Use for backup or additional processing

---

## 🔒 Security Notes

### Your API Keys

- **Never share** your API keys
- **Don't commit** them to GitHub
- **Each user** should have their own keys
- **Rotate regularly** (every 3-6 months)

### Data Privacy

- All data stays in **your Notion** workspace
- AI only sees: names, titles, companies (no emails/phones)
- Apollo data is enrichment only
- Nothing stored in app (stateless)

---

## 💰 Costs Summary

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| Apollo.io | $49-79 | Required (per user) |
| OpenAI | ~$0.50-2 | Very cheap for AI targeting |
| Notion | Free | Basic plan works |
| App hosting | Free | Streamlit Community Cloud |
| **Total** | **~$50-80/mo** | Mainly Apollo subscription |

---

## 📞 Need Help?

### Common Questions

**Q: Can multiple people use this?**
A: Yes! Each person needs their own API keys (especially Apollo).

**Q: How many contacts can I enrich?**
A: Depends on your Apollo plan. Typically 500-1000/month.

**Q: Will this spam people?**
A: No! This just enriches data. YOU decide if/when to reach out.

**Q: Can I customize Notion fields?**
A: Yes! The app uses your existing Notion database structure.

**Q: Is my data safe?**
A: Yes! Everything goes to YOUR Notion. Nothing stored elsewhere.

---

## ✅ Quick Checklist

Before using:

- [ ] Got Apollo API key
- [ ] Got Notion integration token
- [ ] Got Notion database ID
- [ ] Got OpenAI API key
- [ ] Shared Notion database with integration
- [ ] Added all keys to app secrets
- [ ] Tested with 1-2 contacts first
- [ ] App working correctly
- [ ] Contacts appearing in Notion

---

## 🚀 You're Ready!

**Start with something small**:
1. Try AI targeting with **1 company** and **3 people**
2. Check results in Notion
3. Once comfortable, scale up!

**Remember**:
- Quality > Quantity (3 relevant people > 10 random ones)
- Check Notion after each run
- Adjust your AI descriptions based on results

---

## 🎯 Example Workflows

### Workflow 1: HLTH 2025 Conference Prep

```
1. CSV with 20 healthcare companies attending HLTH
2. AI targeting: "C-suite executives interested in digital health partnerships"
3. 5 people per company
4. Review results in Notion
5. Export CSV for email campaign
```

### Workflow 2: Investor Outreach

```
1. Single company lookup: "Sequoia Capital"
2. AI targeting: "Partners focused on healthcare investments"
3. 7 people (broader search)
4. Manual review in Notion
5. Personalized outreach
```

### Workflow 3: Bulk LinkedIn Enrichment

```
1. Export LinkedIn connections to CSV
2. Upload to "Enrich Profiles"
3. Auto-enrich with Apollo data
4. Results in Notion with company details
5. Segment by industry/title
```

---

**Happy CRM'ing!** 🎉

Need help? Ask the person who shared this with you!

---

*Last updated: October 15, 2025*
*For: HLTH 2025 CRM v1.0*
