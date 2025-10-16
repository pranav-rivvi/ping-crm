# Notion Database Setup Guide

## Step 1: Create a Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Name it: "HLTH 2025 CRM"
4. Select your workspace
5. Click "Submit"
6. Copy the "Internal Integration Token" (starts with `secret_`)
7. Save this as `NOTION_TOKEN` in your `.env` file

---

## Step 2: Create Notion Database

1. Open Notion
2. Create a new page called "HLTH 2025 Outreach"
3. Add a database (type `/database` and select "Table - Inline")
4. Name the database "Companies"

---

## Step 3: Add Database Properties

Add the following properties to your database (click "+" in the top right of the table):

### Required Properties

| Property Name | Type | Options (for select/multi-select) |
|--------------|------|----------------------------------|
| Company Name | Title | (default) |
| Status | Select | Not Contacted, Email Sent, Opened, Replied, Meeting Booked, Meeting Done, Pilot Discussion, Pilot Signed, Closed-Lost, Nurture |
| Industry | Select | Insurance / Payer, Healthcare Provider / Health System, Pharmacy / PBM, Pharma / Biotech, Other |
| Tier | Select | Tier 1 - AEP Urgent, Tier 2 - Strategic, Tier 3 - Proven Vertical, Tier 4 - Exploratory |
| Priority Score | Number | (leave default) |
| Company Website | URL | - |
| Company LinkedIn | URL | - |
| Company Size | Select | 1-50, 51-200, 201-1000, 1000-5000, 5000+, Unknown |
| Location | Text | - |
| Revenue Range | Select | <$1M, $1-10M, $10-50M, $50-200M, $200M+, Unknown |
| Funding Stage | Select | Seed, Series A, Series B, Series C+, Public, Private, Unknown |
| Primary Contact Name | Text | - |
| Primary Contact Title | Text | - |
| Primary Contact Email | Email | - |
| Primary Contact LinkedIn | URL | - |
| Secondary Contact Name | Text | - |
| Secondary Contact Title | Text | - |
| Secondary Contact Email | Email | - |
| Tertiary Contact Name | Text | - |
| Tertiary Contact Title | Text | - |
| Tertiary Contact Email | Email | - |
| Enrichment Date | Date | - |
| Apollo ID | Text | - |

---

## Step 4: Connect Integration to Database

1. Click the "..." (three dots) in the top right of your database
2. Scroll down to "Connections"
3. Click "Connect to" and select "HLTH 2025 CRM" (your integration)
4. Confirm the connection

---

## Step 5: Get Database ID

1. Open your database as a full page (click "Open as page" icon)
2. Look at the URL in your browser. It will look like:
   ```
   https://www.notion.so/workspace/DATABASE_ID?v=VIEW_ID
   ```
3. Copy the `DATABASE_ID` (32-character string between the last `/` and the `?`)
4. Save this as `NOTION_DB_ID` in your `.env` file

**Example**:
```
URL: https://www.notion.so/myworkspace/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6?v=...
DATABASE_ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## Step 6: Verify Setup

Your `.env` file should now have:

```bash
APOLLO_API_KEY=your_apollo_key_here
NOTION_TOKEN=secret_your_notion_token_here
NOTION_DB_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## Optional: Customize Your Database

You can add views to your database:

1. **Tier View**: Group by "Tier" to see priorities
2. **Status Board**: Create a board view grouped by "Status"
3. **High Priority**: Filter where "Priority Score" > 7

---

You're all set! Return to the main README to run the enrichment script.
