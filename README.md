# HLTH 2025 CRM - Company Enrichment Tool

Fast, organized MVP for enriching company data and syncing to Notion for HLTH Vegas 2025 conference outreach.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Features

- **Apollo.io Integration**: Automated company and contact enrichment
- **Notion Sync**: Seamless database synchronization
- **Auto Tier Assignment**: Industry-based tier classification
- **Priority Scoring**: Smart 1-10 scoring algorithm
- **Duplicate Detection**: Automatic skip of existing companies
- **Progress Tracking**: Real-time enrichment status
- **Error Handling**: Robust retry logic and error management

---

## Project Structure

```
HLTH2025_CRM/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── apollo_client.py         # Apollo.io API client
│   ├── notion_sync.py           # Notion database sync
│   └── processors.py            # Tier & priority logic
│
├── scripts/                      # Executable scripts
│   ├── enrich.py               # Main enrichment script
│   └── validate_setup.py       # Setup validation
│
├── docs/                         # Documentation
│   ├── setup/
│   │   ├── QUICKSTART.md       # 5-minute setup guide
│   │   ├── NOTION_SETUP.md     # Notion database setup
│   │   └── WHAT_YOU_NEED.md    # Required API keys
│   └── architecture/
│       ├── BREAKDOWN.md        # Architecture options
│       ├── VALIDATION_REPORT.md # Technical audit
│       └── FULL_ARCHITECTURE.txt # Complete architecture spec
│
├── config/                       # Configuration
│   └── .env.example            # Environment template
│
├── examples/                     # Example files
│   └── companies.csv.example   # Sample CSV format
│
├── venv/                         # Virtual environment
├── .env                         # Your API keys (create this)
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Apollo.io API key
- Notion account

### Installation

```bash
# Navigate to project
cd HLTH2025_CRM

# Activate virtual environment
source venv/bin/activate

# Verify setup
python scripts/validate_setup.py
```

### Configuration

```bash
# 1. Copy environment template
cp config/.env.example .env

# 2. Edit with your API keys
nano .env  # Add your keys

# 3. Setup Notion database (see docs/setup/NOTION_SETUP.md)
```

### Usage

```bash
# Create your companies list
# Format: CSV with 'company_name' column

# Run enrichment
python scripts/enrich.py companies.csv
```

---

## API Keys Required

### 1. Apollo.io API Key
Get from: https://app.apollo.io/#/settings/integrations/api

**Free tier**: 50 credits/month (~8-10 companies)

### 2. Notion Integration Token
Get from: https://www.notion.so/my-integrations

**Free**: Unlimited

### 3. Notion Database ID
Extract from your database URL after setup

---

## Documentation

### Setup Guides
- **[QUICKSTART.md](docs/setup/QUICKSTART.md)** - Start here! 5-minute setup
- **[WHAT_YOU_NEED.md](docs/setup/WHAT_YOU_NEED.md)** - Detailed API key instructions
- **[NOTION_SETUP.md](docs/setup/NOTION_SETUP.md)** - Notion database configuration

### Architecture
- **[BREAKDOWN.md](docs/architecture/BREAKDOWN.md)** - MVP vs Full system options
- **[VALIDATION_REPORT.md](docs/architecture/VALIDATION_REPORT.md)** - Technical audit report
- **[FULL_ARCHITECTURE.txt](docs/architecture/FULL_ARCHITECTURE.txt)** - Complete specifications

---

## Features Detail

### Data Enrichment
- Company information (industry, size, revenue, location)
- Decision-maker contacts (3-10 per company)
- Email addresses (verified when available)
- LinkedIn profiles
- Technology stack
- Funding stage

### Auto Tier Assignment
- **Tier 1 - AEP Urgent**: IMOs, agents, brokers
- **Tier 2 - Strategic**: Health plans, payers
- **Tier 3 - Proven Vertical**: Providers, health systems
- **Tier 4 - Exploratory**: Pharma, biotech

### Priority Scoring (1-10)
Factors:
- Company size
- Revenue range
- Contact quality (verified emails)
- Recent activity
- Tier classification

---

## Development

### Project Organization

**src/** - Clean, importable Python modules
- Separation of concerns
- Easy testing
- Reusable components

**scripts/** - Executable entry points
- Main enrichment script
- Validation tools
- Utilities

**docs/** - Organized documentation
- Setup guides
- Architecture specs
- API documentation

**config/** - Configuration management
- Environment templates
- Settings files

---

## Future Enhancements

### Phase 2 (Optional)
- Web scraping for company descriptions
- News scraping for recent mentions
- LinkedIn profile finder (SerpAPI)
- SQLite caching layer

### Phase 3 (Scale-up)
- Batch processing with resume
- Data quality dashboard
- Export to multiple formats
- Advanced analytics

See [docs/architecture/FULL_ARCHITECTURE.txt](docs/architecture/FULL_ARCHITECTURE.txt) for complete roadmap.

---

## Troubleshooting

### Validation Failed
```bash
python scripts/validate_setup.py
```
Follow the error messages to fix issues.

### Import Errors
Make sure you're in the project root and virtual environment is activated:
```bash
cd /Users/pranavarora99/Desktop/HLTH2025_CRM
source venv/bin/activate
```

### Company Not Found
Try using the full legal name. Check Apollo.io directly to verify company listing.

### Notion Sync Errors
- Verify integration is connected to database
- Check database ID is correct (32 characters)
- Ensure all required properties exist

---

## Performance

- **Enrichment speed**: ~3-5 seconds per company
- **Rate limiting**: 1.5 second delay between companies
- **API usage**: ~6 credits per company (Apollo.io)
- **Batch size**: Unlimited (respects rate limits)

---

## Security

- Environment variables for all secrets
- .env excluded from git
- No credentials in code
- HTTPS for all API calls

---

## Contributing

This is a personal MVP project. For enhancements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## Support

**Documentation**: Check `docs/` folder for detailed guides

**Validation**: Run `python scripts/validate_setup.py`

**Issues**: Review error messages and docs/setup/ guides

---

## License

MIT License - See LICENSE file for details

---

## Credits

**Tech Stack**:
- Python 3.13+
- Apollo.io API (company data)
- Notion API (database sync)
- Rich (terminal UI)
- Pandas (data processing)

**Built for**: HLTH Vegas 2025 Conference

---

**Ready to enrich!** 🚀

Start with [docs/setup/QUICKSTART.md](docs/setup/QUICKSTART.md) to get running in 5 minutes.
