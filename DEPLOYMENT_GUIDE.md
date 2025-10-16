# 🚀 Deployment Guide - Streamlit Community Cloud
**Deploy your HLTH 2025 CRM in 5 minutes for FREE**

---

## Why Streamlit Cloud?

✅ **100% FREE** - No credit card needed
✅ **Zero infrastructure** - No Docker, no servers
✅ **Built-in secrets** - Secure API key management
✅ **Auto-updates** - Push to GitHub = instant update
✅ **Simple sharing** - Share with anyone via link
✅ **HTTPS** - Secure by default

---

## 📋 Prerequisites

You need:
1. GitHub account (free)
2. Streamlit Cloud account (free - sign up with GitHub)
3. Your API keys ready:
   - Apollo.io API key
   - Notion API token
   - Notion Database ID
   - OpenAI API key (or Gemini API key)

---

## 🎯 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
# Navigate to your project
cd /Users/pranavarora99/Desktop/HLTH2025_CRM

# Initialize git (if not already done)
git init

# Create .gitignore
echo ".env
venv/
__pycache__/
*.pyc
.DS_Store
*.db" > .gitignore

# Add all files
git add .

# Commit
git commit -m "Initial commit - HLTH 2025 CRM"

# Create a new repository on GitHub (via web browser)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/hlth-2025-crm.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/

2. **Click "New app"**

3. **Fill in**:
   - Repository: `YOUR_USERNAME/hlth-2025-crm`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: `your-crm-app` (or any name you want)

4. **Click "Advanced settings"** → **Add secrets**

---

### Step 3: Add API Keys as Secrets

In the secrets section, paste this format:

```toml
# API Keys
APOLLO_API_KEY = "your_apollo_api_key_here"
NOTION_TOKEN = "your_notion_token_here"
NOTION_DB_ID = "your_notion_database_id_here"

# AI Keys (add ONE of these)
OPENAI_API_KEY = "sk-your_openai_key_here"
# OR
GEMINI_API_KEY = "your_gemini_key_here"
```

**IMPORTANT**: Replace the values with your actual API keys!

5. **Click "Deploy!"**

---

### Step 4: Wait for Deployment

- First deployment takes 2-3 minutes
- Watch the build logs (they'll show if something goes wrong)
- Once done, you'll see: ✅ **App is live!**

---

## 🔐 Sharing with Your Friend

### Option 1: Public App (Anyone with link can access)
- Just share the URL: `https://your-crm-app.streamlit.app`
- Anyone with the link can use it
- **Their own API keys**: Each user adds their keys in Streamlit settings

### Option 2: Private App (Email-based access)
1. Go to app settings → **Sharing**
2. Toggle "This app is private"
3. Add your friend's email
4. They'll get an invite email
5. They log in with GitHub/Google/Email

---

## 👥 Multi-User Setup

### Each User Needs Their Own Keys

**User Setup Instructions** (send this to your friend):

1. **Access the app** (via link or invite)

2. **Go to Settings** → **Manage app** → **Secrets**
   (Only visible if you give them edit access)

3. **Add their API keys**:
   ```toml
   APOLLO_API_KEY = "their_apollo_key"
   NOTION_TOKEN = "their_notion_token"
   NOTION_DB_ID = "their_notion_db_id"
   OPENAI_API_KEY = "their_openai_key"
   ```

4. **That's it!** App works with their data

---

## 🔄 How to Update the App

Any time you make changes:

```bash
# Make your changes to code
# Then:
git add .
git commit -m "Description of changes"
git push

# App auto-updates in ~1 minute! 🚀
```

---

## 🛠️ Alternative: Run Locally for Testing

Before deploying, test locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your keys
cp .env.example .env
# (Edit .env with your API keys)

# 3. Run app
streamlit run app.py
```

Open http://localhost:8501 in browser

---

## 💰 Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| **Streamlit Cloud** | FREE | Unlimited public apps, 1 private app |
| **GitHub** | FREE | Public repos |
| **Apollo.io** | $49-79/mo | Per user (they need their own) |
| **Notion** | FREE | Basic plan works |
| **OpenAI** | ~$0.50-$2/mo | GPT-4o-mini is very cheap |

**Total for deployment**: **$0** 🎉
**Total for usage**: Apollo subscription only

---

## 🔥 Quick Start (For Your Friend)

Send them this:

### "Hey! Here's how to use the CRM:"

1. **Get API keys**:
   - Apollo.io: https://app.apollo.io/#/settings/integrations/api
   - Notion: https://www.notion.so/my-integrations
   - OpenAI: https://platform.openai.com/api-keys

2. **Access the app**: [YOUR_APP_URL]

3. **Add your keys**: Settings → Secrets (paste your API keys)

4. **Start using it!** 🎯

---

## 🐛 Troubleshooting

### "App won't start"
- Check build logs for errors
- Verify requirements.txt has all dependencies
- Ensure app.py is in root directory

### "Missing API keys"
- Add secrets in Streamlit Cloud settings
- Use exact format (TOML syntax)
- No quotes around secret names

### "Rate limit errors"
- Apollo API has rate limits (5 requests/second)
- App has built-in delays (1.5s between companies)
- Adjust in Settings → Rate Limiting

### "App is slow"
- Free tier sleeps after 7 days of inactivity
- First request wakes it up (~30 seconds)
- Then it's fast!

---

## 🎨 Custom Domain (Optional)

Want `crm.yourcompany.com` instead of `your-app.streamlit.app`?

1. **Upgrade to Streamlit Cloud Pro** ($20/mo per workspace)
2. Add custom domain in settings
3. Update DNS records
4. Done!

---

## 📊 Usage Monitoring

Streamlit Cloud dashboard shows:
- ✅ App uptime
- 👥 Number of viewers
- 📈 Resource usage
- 🔄 Deployment history

---

## 🔒 Security Best Practices

### DO:
- ✅ Use Streamlit secrets for API keys (never commit .env)
- ✅ Set app to private if handling sensitive data
- ✅ Give each user their own Apollo API key
- ✅ Regularly rotate API keys

### DON'T:
- ❌ Commit API keys to GitHub
- ❌ Share API keys between users
- ❌ Use personal Notion tokens for team workspaces
- ❌ Make app public with shared credentials

---

## 🚀 Advanced: Docker Deployment (Optional)

If you prefer Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Deploy to:
- **Google Cloud Run** (pay per use, ~$5/mo)
- **Railway.app** (free tier available)
- **Fly.io** (free tier available)
- **Heroku** ($7/mo)

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Code pushed to GitHub
- [ ] `.gitignore` includes `.env`
- [ ] `requirements.txt` is up to date
- [ ] API keys ready
- [ ] Tested locally with `streamlit run app.py`
- [ ] App settings configured
- [ ] Secrets added to Streamlit Cloud
- [ ] App deployed successfully
- [ ] Shared with friend (if private)
- [ ] Friend can access and add their keys

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Streamlit Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: Create issue in your repo

---

## 🎯 Summary

**Simplest deployment**:
1. Push to GitHub (5 min)
2. Deploy on Streamlit Cloud (2 min)
3. Add API keys as secrets (1 min)
4. Share with friend (30 sec)

**Total time**: ~10 minutes
**Total cost**: $0
**Total complexity**: Minimal 🎉

---

**Your app is now live and production-ready!** 🚀

Each user can connect their own API keys, and everything just works!

---

*Created: October 15, 2025*
*For: HLTH 2025 CRM*
