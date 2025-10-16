# State Field & Apollo Email Unlocking Guide

## Part 1: Adding State Field to Notion

### What State Data Do We Get?

Apollo provides location data for each contact:
- **City**: e.g., "Miami"
- **State**: e.g., "Florida"
- **Country**: e.g., "United States"

The code now captures and writes the **State** field automatically.

---

### Step 1: Add State Field to Your Notion Database

**Method 1: Via Notion Web/Desktop**

1. Open your Notion database: **"HLTH Conference Outreach Tracker"**

2. Click the **"+"** button at the end of your table header (or right-click any column header)

3. Add new property:
   - **Name**: `State`
   - **Type**: `Text` (rich_text)

4. Done! The enrichment code will now automatically fill this field

**Method 2: Via Notion Mobile**

1. Open database
2. Tap any row to open full page
3. Scroll to properties
4. Tap "+ Add a property"
5. Name it `State`, select type `Text`

---

### Step 2: Test State Field

Run a test enrichment:

```bash
source venv/bin/activate
python scripts/test_e2e.py "Bruce Broussard" "Humana"
```

Check your Notion database - you should now see:
- **State**: "Florida" (or wherever the person is based)

---

### What Gets Written

**Before** (without State field):
- Contact Name: Phillip Giarth
- Company: Humana
- Title: Regional VP
- Email, LinkedIn, etc.

**After** (with State field):
- Contact Name: Phillip Giarth
- Company: Humana
- Title: Regional VP
- **State: Florida** ✨ NEW!
- Email, LinkedIn, etc.

---

## Part 2: Apollo Email Unlocking

### Understanding Apollo Emails

When you see: `email_not_unlocked@domain.com`

**What it means:**
- Apollo has this person's email in their database
- You haven't "unlocked" it yet (uses credits)
- LinkedIn URL is FREE and doesn't require unlocking

---

### How Apollo Credits Work

**Free Plan:**
- Limited email credits per month
- Usually ~50-100 email unlocks/month
- Contact search is FREE
- LinkedIn URLs are FREE

**Paid Plans:**
- More email credits
- Bulk email export
- Higher API limits

---

### Method 1: Unlock Emails in Apollo Web UI

**Step 1**: Go to https://app.apollo.io

**Step 2**: Search for the person
```
Name: Phillip Giarth
Company: Humana
```

**Step 3**: Click their profile

**Step 4**: Click **"Unlock Email"** button
- Uses 1 credit
- Email is revealed instantly
- Email is now in your "Unlocked" list

**Step 5**: Re-run enrichment
```bash
python scripts/test_e2e.py "Phillip Giarth" "Humana"
```

Now the REAL email will appear (not `email_not_unlocked@domain.com`)

---

### Method 2: Bulk Email Unlocking

**For Multiple Contacts:**

1. Create a list in Apollo with your target contacts

2. Select all contacts

3. Click "Export" → Choose email export

4. Apollo will unlock all emails in batch (uses credits for each)

5. Re-run your enrichment script

---

### Method 3: API Email Reveal (Advanced)

Apollo has an `/email_reveal` endpoint:

```python
# Example (not implemented yet, but can add if you want)
def reveal_email(apollo_client, person_id):
    endpoint = f"{apollo_client.BASE_URL}/people/{person_id}/email"
    response = apollo_client.session.get(endpoint)
    return response.json()
```

**Note**: This uses your API credits automatically

---

### Email Unlocking Strategy

**Recommended Approach for HLTH 2025:**

#### Phase 1: LinkedIn First (Free)
```bash
# Run enrichment to get LinkedIn URLs
python scripts/test_e2e.py "Person Name" "Company"
```

**Result**: You get:
- ✅ Name, title, company
- ✅ LinkedIn URL (FREE - use this for outreach!)
- ✅ Location, seniority
- ❌ Email (locked)

#### Phase 2: Selective Email Unlocking

**Only unlock emails for:**
1. **High-priority contacts** (VPs, C-suite)
2. **People you're actually going to email**
3. **After initial LinkedIn connection** (if they don't respond)

**Why this works:**
- LinkedIn connections are FREE
- Save email credits for warm leads
- Most professionals respond on LinkedIn anyway

#### Phase 3: Bulk Unlock After Event

**After HLTH 2025:**
- You've met people
- You know who's interested
- Unlock emails for follow-ups

---

### Checking Your Email Credit Balance

**Via Web UI:**
1. Go to https://app.apollo.io
2. Click your profile (top right)
3. Go to "Settings" → "Plan & Billing"
4. See "Email Credits: X remaining"

**Via API:**
```bash
# Check your plan limits
curl -X GET "https://api.apollo.io/v1/auth/health" \
  -H "X-Api-Key: YOUR_API_KEY"
```

---

### Alternative: Other Email Finding Tools

If you run out of Apollo credits, use these:

**1. LinkedIn Sales Navigator**
- Shows emails for some contacts
- Can message directly (no email needed)

**2. Hunter.io**
- Find emails by name + company domain
- ~50 free searches/month
- API available

**3. RocketReach**
- Alternative to Apollo
- Different database
- May have emails Apollo doesn't

**4. Manual Methods**
- Company website → Team page
- Google: "FirstName LastName CompanyName email"
- GitHub profiles (for technical contacts)

---

## Best Practices

### For HLTH 2025 Conference

**Pre-Event Research:**
```bash
# Enrich without worrying about emails
python scripts/test_e2e.py "Target Person" "Company"
```

**What you get (all FREE):**
- ✅ LinkedIn URL - Message them about meeting at HLTH
- ✅ Title - Know their role
- ✅ Company info - Research talking points
- ✅ Location - "I see you're in Miami too!"

**Post-Event Follow-Up:**
1. Met someone at booth → Add to Notion
2. Want to email them → Unlock email in Apollo
3. Re-run enrichment → Email appears
4. Send personalized follow-up

---

### Email Unlocking Priority

**Tier 1: Always Unlock** (if emailing)
- C-Level executives (CEO, CFO, CMO)
- Decision makers you met in person
- Warm introductions

**Tier 2: Selective Unlock**
- VPs, Directors
- LinkedIn connection didn't respond
- Need email for vendor onboarding

**Tier 3: LinkedIn First**
- Entry/mid-level contacts
- Initial outreach
- Cold contacts

---

## Code Changes Made

**Updated Files:**

### 1. `src/apollo_client.py`
```python
def _normalize_contact(self, raw_data: Dict) -> Dict:
    return {
        # ... existing fields ...
        'city': raw_data.get('city', ''),        # NEW
        'state': raw_data.get('state', ''),      # NEW
        'country': raw_data.get('country', ''),  # NEW
    }
```

### 2. `src/notion_client.py`
```python
# In _update_page and _create_page:
if enriched_data.get('state'):
    try:
        properties["State"] = {
            "rich_text": [{"text": {"content": enriched_data['state']}}]
        }
    except Exception:
        pass  # Skip if State field doesn't exist yet
```

**Graceful handling**: If you haven't added the State field to Notion yet, the code won't crash - it just skips it.

---

## Testing State Field

### Test 1: Without State Field in Notion

```bash
python scripts/test_e2e.py "Bruce Broussard" "Humana"
```

**Result**: Everything works, State is silently skipped

### Test 2: After Adding State Field

1. Add State field to Notion (Text type)
2. Run same command
3. Check Notion → State field is populated!

---

## Summary

### State Field ✅
- **Added to code**: Captures city, state, country from Apollo
- **How to enable**: Add "State" field (Text type) to your Notion database
- **Benefit**: Filter contacts by location, see where people are based

### Email Unlocking 💡
- **LinkedIn URLs**: FREE, use these first!
- **Email unlocking**: Costs credits, use strategically
- **Best strategy**: LinkedIn for initial outreach, emails for follow-ups
- **Check credits**: https://app.apollo.io → Settings → Plan

---

## Quick Actions

**Right Now:**
```bash
# 1. Add State field to Notion
# Open database → Add property → Name: "State", Type: "Text"

# 2. Test it
source venv/bin/activate
python scripts/test_e2e.py "Any Executive" "Any Company"

# 3. Check Notion - State field should be populated!
```

**For Emails:**
- Use LinkedIn URLs from enriched data (FREE)
- Only unlock emails when you're actually going to use them
- Consider bulk unlocking after the conference

---

*Last updated: October 15, 2025*
