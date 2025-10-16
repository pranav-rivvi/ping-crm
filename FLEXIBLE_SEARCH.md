# Flexible Contact Enrichment System

## Overview

The system now supports **intelligent priority-based search** with three different unique/composite keys:

1. **LinkedIn URL** (unique key - highest priority)
2. **Email** (unique key - second priority)
3. **Name + Company** (composite key - third priority)

## How It Works

### Priority-Based Search

For each row in your CSV, the system tries these methods **in order** until it finds a match:

```
1. LinkedIn URL → if exists → search Apollo by LinkedIn
   ↓ (if not found or not provided)
2. Email → if exists → search Apollo by email
   ↓ (if not found or not provided)
3. Name + Company → if both exist → search Apollo by name at company
   ↓ (if still not found)
4. Mark as FAILED
```

### CSV Format

**Flexible columns** - include any combination:

| Column | Required? | Priority | Example |
|--------|-----------|----------|---------|
| `linkedin_url` | Optional | 1st | `https://linkedin.com/in/username` |
| `email` | Optional | 2nd | `karen@cvshealth.com` |
| `person_name` | Optional* | 3rd | `Karen Lynch` |
| `company_name` | Optional* | 3rd | `CVS Health` |

*Note: `person_name` and `company_name` must be provided **together** to work as a composite key.

## CSV Examples

### Example 1: Mixed Data
```csv
linkedin_url,email,person_name,company_name
https://linkedin.com/in/user1,,,
,karen@cvs.com,,
,,Gail Boudreaux,Elevance Health
https://linkedin.com/in/user2,bruce@humana.com,Bruce Broussard,Humana
```

**What happens:**
- Row 1: Searches by LinkedIn only
- Row 2: Searches by email only
- Row 3: Searches by name + company only
- Row 4: Tries LinkedIn first, falls back to email if needed, then name+company

### Example 2: LinkedIn Only
```csv
linkedin_url
https://linkedin.com/in/timcook
https://linkedin.com/in/satya-nadella
https://linkedin.com/in/sundar-pichai
```

### Example 3: Emails Only
```csv
email
tim@apple.com
satya@microsoft.com
sundar@google.com
```

### Example 4: Names Only
```csv
person_name,company_name
Karen Lynch,CVS Health
Bruce Broussard,Humana
Gail Boudreaux,Elevance Health
```

### Example 5: All Fields (Safest)
```csv
linkedin_url,email,person_name,company_name
https://linkedin.com/in/karenlynch,karen@cvshealth.com,Karen Lynch,CVS Health
,bruce@humana.com,Bruce Broussard,Humana
,,Gail Boudreaux,Elevance Health
```

## Result Messages

The system tells you **which method succeeded**:

- ✅ `Added via LinkedIn` - Found using LinkedIn URL
- ✅ `Updated via Email` - Found using email address
- ✅ `Created via Name+Company` - Found using name + company search
- ⏭️ `Already exists (found via LinkedIn)` - Skipped duplicate
- ❌ `Not found in Apollo (tried: Email)` - Couldn't find contact

## Benefits

1. **Maximum flexibility** - Use whatever data you have
2. **Fallback logic** - If one method fails, tries the next
3. **LinkedIn prioritized** - Most accurate search method
4. **Data completeness** - Multiple ways to find the same person
5. **Transparent results** - Know exactly how each contact was found

## Recommendations

### Best Practices

1. **Provide multiple identifiers when possible**
   - LinkedIn + Email + Name is safest
   - System will use the most reliable method available

2. **LinkedIn URLs are most reliable**
   - Direct match in Apollo
   - Highest success rate
   - Recommended for VIP contacts

3. **Email is second-best**
   - Good for professionals with public emails
   - Works well for verified business emails

4. **Name + Company as fallback**
   - Use when LinkedIn/email not available
   - Less precise (common names may mismatch)
   - Better with full names and exact company names

### When to Use Each Method

**Use LinkedIn URL when:**
- You have the person's LinkedIn profile
- VIP contacts (CEOs, executives)
- You need 100% accuracy

**Use Email when:**
- You have verified business email
- Person is active professionally
- LinkedIn profile is private/unavailable

**Use Name + Company when:**
- Only basic info available
- Bulk research from public lists
- Conference attendee lists without emails

## Technical Details

### Search Priority Logic

```python
def enrich_contact_flexible(row, apollo, notion):
    # 1. Try LinkedIn
    if linkedin_url exists and valid:
        person_data = apollo.search_by_linkedin_url(linkedin_url)

    # 2. Try Email (if LinkedIn failed or missing)
    if not person_data and email exists and valid:
        person_data = apollo.search_by_email(email)

    # 3. Try Name + Company (if both failed or missing)
    if not person_data and person_name and company_name:
        person_data = apollo.search_person_by_name(person_name, company_name)

    # 4. Failed
    if not person_data:
        return FAILED
```

### Validation

**Row-level validation:**
- At least ONE of these must be present per row:
  - Valid LinkedIn URL (contains 'linkedin.com')
  - Valid email (contains '@')
  - Both person_name AND company_name

**CSV-level validation:**
- At least ONE of these column combinations must exist:
  - `linkedin_url` column
  - `email` column
  - Both `person_name` AND `company_name` columns

## UI Features

### CSV Upload Tab

1. **Auto-detection** - System detects available search methods
2. **Priority display** - Shows which methods will be tried
3. **Live feedback** - See which method succeeded for each contact
4. **Smart fallback** - Automatically tries next method if one fails

### Status Messages

During processing, you'll see:
```
Processing 1/10: https://linkedin.com/in/user
✅ Success: Karen Lynch added via LinkedIn

Processing 2/10: karen@cvs.com
✅ Success: Karen Lynch updated via Email

Processing 3/10: Gail Boudreaux
✅ Success: Gail Boudreaux created via Name+Company
```

## Templates

Download from the UI sidebar:

1. **📋 Full Template** - All columns with examples
2. **📄 Simple Template** - Just name + company (traditional)

## FAQ

**Q: Can I mix different search types in one CSV?**
A: Yes! Each row is evaluated independently.

**Q: What if I provide all three (LinkedIn + Email + Name)?**
A: System uses LinkedIn first (highest priority), others as backup.

**Q: What if LinkedIn fails but email works?**
A: System automatically tries email next, then name+company.

**Q: Do I need all columns in my CSV?**
A: No! Include only the columns you have data for. System adapts.

**Q: What's the most reliable method?**
A: LinkedIn URL > Email > Name+Company (in that order)

**Q: Can I upload just emails or just LinkedIn URLs?**
A: Absolutely! Single-column CSVs work perfectly.

## Migration from Old Format

### Old Format (Required both columns)
```csv
person_name,company_name
Karen Lynch,CVS Health
```

### New Format (Same file still works!)
```csv
person_name,company_name
Karen Lynch,CVS Health
```

**Your existing CSVs are fully compatible!**

The new system is **backward compatible** - old name+company CSVs work exactly as before, but now you can also add LinkedIn/email columns for better accuracy.

## Summary

The flexible search system gives you:
- ✅ Multiple ways to find contacts
- ✅ Automatic fallback logic
- ✅ Clear result messages
- ✅ Backward compatibility
- ✅ Maximum success rate

**Use whatever data you have - the system figures out the rest!**
