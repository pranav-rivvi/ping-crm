# HLTH 2025 CRM - Web UI Guide
**Enhanced Streamlit Interface with AI Company Targeting**

---

## Quick Start

### Launch the Web App

```bash
cd /Users/pranavarora99/Desktop/HLTH2025_CRM
source venv/bin/activate
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## Features Overview

### 🎯 Tab 4: AI-Powered Company Targeting (Enhanced!)

This is your new, enhanced AI targeting interface with:

#### **1️⃣ Upload Companies**
- Upload a simple CSV with just one column: `company_name`
- Example:
  ```csv
  company_name
  CVS Health
  Humana
  UnitedHealth Group
  ```

#### **2️⃣ Describe Who You Want to Reach**
- **User-Configurable Search**: Type your targeting goal in natural language
- AI automatically figures out:
  - Relevant job titles
  - Seniority levels
  - Location filters (if mentioned)

**Example Inputs**:
```
✅ "C-suite executives for partnership discussions at HLTH 2025"
✅ "Sales and marketing leaders in the Northeast region"
✅ "Technology decision-makers who buy enterprise software"
✅ "Operations managers who handle supply chain"
✅ "Clinical leaders focused on patient outcomes"
```

#### **3️⃣ How Many People Per Company? (NEW!)**
- **Always-Visible Slider**: No hidden menus!
- Range: 1-7 people per company (max 7 for quality)
- Default: 5 people
- **Real-time metrics**: Shows total expected contacts
  - Example: 10 companies × 5 people = ~50 contacts

#### **4️⃣ Ready to Go?**
- **🔍 Preview AI Strategy** (NEW!)
  - See exactly what AI will search for
  - Shows: Job titles, seniority levels, locations
  - Review before executing

- **🚀 Find People & Add to Notion**
  - Executes the search
  - Adds contacts directly to Notion
  - Real-time progress tracking

---

## Enhanced UX Features

### 1. **Preview Before Execute**
- Click "Preview AI Strategy" to see what AI plans to do
- Review the job titles AI generated
- Check seniority filters
- Verify location targeting
- Make sure it aligns with your goal
- Then click "Find People" when ready

### 2. **Prominent Slider Control**
- No more hidden "Advanced Options"!
- Slider is always visible
- Limited to 7 for quality (no more 20-person dumps)
- Shows total expected results in real-time

### 3. **User-Configurable Search**
- Be as specific or general as you want
- Mention locations: "in New York" or "Northeast region"
- Specify functions: "sales leaders" or "technology decision-makers"
- Describe purpose: "for partnership discussions" or "to pitch our platform"

### 4. **Smart Metrics**
```
┌─────────────────────────────────────┐
│ Total Contacts: ~50                 │
│                                     │
│ 📊 Expected results:                │
│ ~50 contacts (10 companies × 5)    │
└─────────────────────────────────────┘
```

---

## Complete Workflow Example

### Scenario: Finding C-Suite at Healthcare Payers

**Step 1**: Create `payers.csv`
```csv
company_name
Humana
UnitedHealth Group
CVS Health
Cigna
Elevance Health
```

**Step 2**: Launch app
```bash
streamlit run app.py
```

**Step 3**: Navigate to Tab 4 "🎯 AI Company Targeting"

**Step 4**: Upload `payers.csv`
- ✅ Loaded 5 companies

**Step 5**: Enter your goal
```
C-suite executives and VPs for partnership discussions about value-based care solutions
```

**Step 6**: Adjust slider
- Set to **7** people per company
- See metric: "Total Contacts: ~35"

**Step 7**: Click "🔍 Preview AI Strategy"
- Review AI-generated titles:
  - CEO, Chief Executive Officer
  - CFO, Chief Financial Officer
  - COO, Chief Operating Officer
  - CMO, Chief Marketing Officer
  - CTO, Chief Technology Officer
  - President
  - VP Strategy
  - VP Innovation
  - VP Business Development
  - ...and more

- Review seniority levels:
  - C-Suite
  - VP

**Step 8**: Click "🚀 Find People & Add to Notion"
- Watch real-time progress
- See live stats:
  - Companies: 5
  - Found: 35
  - Added: 35
  - Skipped: 0

**Step 9**: Results!
- 35 C-suite executives added to Notion
- Complete profiles with:
  - Name, Title, Company
  - Email, Phone, LinkedIn
  - City, State, Country
  - Enrichment notes

---

## Other Tabs

### 📤 Tab 1: Bulk Upload
- Upload CSV with contacts (name, email, LinkedIn)
- Flexible search priority: LinkedIn → Email → Name+Company
- Batch enrichment with progress bars

### 🔗 Tab 2: LinkedIn/Email Lookup
- Single-contact quick lookup
- Paste LinkedIn URL or email
- Instant enrichment and Notion add
- Preview before adding

### 📊 Tab 3: Results
- View all enrichment results
- Filter by status (Success, Failed, Skipped)
- Download results as CSV
- Reset and start new batch

---

## Tips & Best Practices

### 1. **Be Specific in Your Goal**
❌ Bad: "executives"
✅ Good: "C-suite executives for partnership discussions at HLTH 2025"

❌ Bad: "tech people"
✅ Good: "Technology decision-makers who evaluate and purchase enterprise software"

### 2. **Use the Preview Feature**
- Always preview before executing on large batches
- Verify AI understood your intent
- Check if titles match your expectations
- Adjust your description if needed

### 3. **Start Small**
- Test with 2-3 companies first
- Verify quality in Notion
- Then scale to full list

### 4. **Optimize People Count**
- **1-3 people**: Only top executives
- **5 people**: Balanced (recommended)
- **7 people**: Maximum coverage

### 5. **Monitor Credits**
- Each person search uses ~1 Apollo credit
- 5 people × 10 companies = ~50 credits
- Plan accordingly for large batches

---

## Keyboard Shortcuts (Streamlit)

- **Ctrl/Cmd + K**: Command palette
- **R**: Refresh app
- **C**: Clear cache

---

## Troubleshooting

### Issue: "AI Company Targeting requires an AI API key"
**Solution**: Add to `.env`:
```bash
OPENAI_API_KEY=sk-proj-...
```
Then restart: `streamlit run app.py`

### Issue: Slider not appearing
**Solution**: Refresh the page (press R)

### Issue: Preview button not working
**Solution**: Make sure you've:
1. Uploaded companies CSV
2. Entered a description
3. Waited for CSV to load

### Issue: No results found
**Solution**:
- Try broader search terms
- Check if companies exist in Apollo database
- Verify company names are exact (e.g., "CVS Health" not "CVS")

---

## What's New in This Version

### ✨ Major Enhancements

1. **Slider Always Visible**
   - No more hidden "Advanced Options"
   - Prominent placement in main flow
   - Limited to 7 for quality

2. **Preview AI Strategy Button**
   - NEW button to preview before execution
   - See exact titles AI will search
   - Verify seniority and location filters
   - Make informed decisions

3. **Better Metrics**
   - Real-time total contacts calculation
   - Shows: companies × people = total
   - Helps plan API credit usage

4. **Improved UX Flow**
   - Clear step-by-step numbering (1️⃣ 2️⃣ 3️⃣ 4️⃣)
   - Better descriptions and help text
   - More example inputs
   - User-friendly language

5. **Enhanced Customization**
   - More control over search parameters
   - Better natural language understanding
   - Clearer feedback on what AI is doing

---

## API Credit Usage

### Per Company (with 5 people)
```
Company search:  1 credit
5 people search: 5 credits
Total:           6 credits
```

### Example Batches
```
10 companies × 5 people = ~60 credits
20 companies × 5 people = ~120 credits
50 companies × 5 people = ~300 credits
```

### Apollo.io Free Tier
- 50 credits/month
- Can enrich ~8 companies
- Consider paid plan for larger batches

---

## Next Steps

### After Your First Successful Run

1. **Check Notion Database**
   - Verify all contacts added
   - Review enrichment notes
   - Check data quality

2. **Download Results CSV**
   - Tab 3: Download button
   - Backup of all enrichment data
   - Import into other tools if needed

3. **Scale Up**
   - Start with 10 companies
   - Test quality
   - Then process full list

4. **Refine Targeting**
   - Try different descriptions
   - Test various slider values
   - Find optimal balance

---

## Support

### Documentation
- Main README: `/README.md`
- Quickstart: `/docs/setup/QUICKSTART.md`
- Architecture: `/COMPREHENSIVE_SYSTEM_ANALYSIS.md`

### Test Scripts
- AI Targeting Test: `python scripts/test_e2e_ai_targeting.py`
- Validation: `python scripts/validate_setup.py`

### Need Help?
1. Check this guide first
2. Review COMPREHENSIVE_SYSTEM_ANALYSIS.md
3. Run validation script
4. Check .env file for API keys

---

**Ready to find the perfect contacts for HLTH 2025!** 🚀

---

*Last Updated: October 15, 2025*
*App Version: 1.0 with Enhanced AI Targeting*
