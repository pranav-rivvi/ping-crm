# Project Structure

## Overview

Clean, professional folder organization following Python best practices for MVP development and future scalability.

---

## Directory Layout

```
HLTH2025_CRM/
│
├── src/                          # Source Code (Core Modules)
│   ├── __init__.py              # Package initialization & exports
│   ├── apollo_client.py         # Apollo.io API integration
│   ├── notion_sync.py           # Notion database sync
│   └── processors.py            # Business logic (tier, priority)
│
├── scripts/                      # Entry Points & Utilities
│   ├── enrich.py               # Main enrichment workflow
│   └── validate_setup.py       # Pre-flight system check
│
├── docs/                         # Documentation
│   ├── setup/                   # Setup & Configuration Guides
│   │   ├── QUICKSTART.md       # 5-minute getting started
│   │   ├── NOTION_SETUP.md     # Notion database setup
│   │   └── WHAT_YOU_NEED.md    # API keys & requirements
│   │
│   └── architecture/            # Technical Documentation
│       ├── BREAKDOWN.md        # MVP vs Full architecture
│       ├── VALIDATION_REPORT.md # Code validation audit
│       └── FULL_ARCHITECTURE.txt # Complete system spec
│
├── config/                       # Configuration Files
│   └── .env.example            # Environment variable template
│
├── examples/                     # Example & Template Files
│   └── companies.csv.example   # Sample CSV format
│
├── venv/                         # Python Virtual Environment
│   └── ...                      # (Git ignored)
│
├── .env                         # Your API Keys (Create this!)
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
└── PROJECT_STRUCTURE.md         # This file
```

---

## Design Principles

### 1. Separation of Concerns

**src/** - Business logic only
- No CLI code
- No file I/O
- Pure functions
- Easy to test
- Reusable modules

**scripts/** - Entry points & orchestration
- CLI interfaces
- File operations
- Workflow coordination
- Error handling
- User interaction

### 2. Maintainability

**Organized docs/** - Easy to navigate
- Setup guides separated from architecture
- Progressive disclosure (QUICKSTART → detailed guides)
- Technical specs separated from user docs

**config/** - Centralized configuration
- Template files
- Settings management
- Easy to find and modify

**examples/** - Sample files
- CSV templates
- Configuration examples
- Test data

### 3. Scalability

**Modular src/** structure
- Easy to add new modules
- Clear import paths
- Package initialization
- Version management

**Flexible scripts/**
- Add new entry points without touching core
- Utility scripts separate from main workflow
- Easy to create new tools

---

## Module Descriptions

### src/apollo_client.py
**Purpose**: Apollo.io API integration

**Responsibilities**:
- Company search
- Contact search
- Email enrichment
- Data normalization
- Rate limiting
- Retry logic

**Exports**:
- `ApolloClient` class

### src/notion_sync.py
**Purpose**: Notion database synchronization

**Responsibilities**:
- Page creation
- Property building
- Duplicate detection
- Industry/size mapping
- URL validation

**Exports**:
- `NotionClient` class

### src/processors.py
**Purpose**: Business logic & rules

**Responsibilities**:
- Tier assignment (1-4)
- Priority scoring (1-10)
- Industry categorization
- Scoring algorithms

**Exports**:
- `TierAssigner` class
- `PriorityScorer` class

### scripts/enrich.py
**Purpose**: Main enrichment workflow

**Responsibilities**:
- CSV parsing
- Progress tracking
- Error reporting
- Results summary
- Rate limiting
- CLI interface

**Usage**:
```bash
python scripts/enrich.py companies.csv
```

### scripts/validate_setup.py
**Purpose**: Pre-flight validation

**Responsibilities**:
- Python version check
- Dependency verification
- Environment validation
- File structure check
- Import testing

**Usage**:
```bash
python scripts/validate_setup.py
```

---

## Import Patterns

### From scripts/ to src/
```python
# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from src
from src.apollo_client import ApolloClient
from src.notion_sync import NotionClient
from src.processors import TierAssigner, PriorityScorer
```

### Within src/ (future)
```python
# Relative imports within package
from .apollo_client import ApolloClient
from .processors import TierAssigner
```

### Package exports (src/__init__.py)
```python
# Clean public API
from .apollo_client import ApolloClient
from .notion_sync import NotionClient
from .processors import TierAssigner, PriorityScorer

__all__ = [
    'ApolloClient',
    'NotionClient',
    'TierAssigner',
    'PriorityScorer'
]
```

---

## File Naming Conventions

### Python Files
- **snake_case**: `apollo_client.py`, `notion_sync.py`
- **Descriptive**: Clear what the module does
- **No abbreviations**: Full words preferred

### Documentation
- **UPPERCASE.md**: Top-level docs (README, QUICKSTART)
- **PascalCase.md**: Technical docs
- **Descriptive**: Clear topic indication

### Configuration
- **.env.example**: Template (committed)
- **.env**: Actual keys (git ignored)
- **Dot files**: Hidden system files

---

## Adding New Features

### 1. New Data Source
```
src/
└── new_source_client.py    # Add new client module

scripts/
└── enrich.py              # Import and use in workflow
```

### 2. New Script
```
scripts/
└── new_utility.py         # Add new entry point
                          # Imports from src/
```

### 3. New Documentation
```
docs/
├── setup/                 # If setup-related
│   └── NEW_GUIDE.md
└── architecture/          # If technical
    └── NEW_SPEC.md
```

---

## Testing Structure (Future)

```
tests/
├── __init__.py
├── test_apollo_client.py
├── test_notion_sync.py
├── test_processors.py
└── test_integration.py
```

---

## Benefits of This Structure

### For Development
1. **Clear separation**: Logic vs orchestration
2. **Easy testing**: Import modules directly
3. **Reusable code**: src/ can be packaged
4. **Clean imports**: Explicit paths

### For Maintenance
1. **Easy navigation**: Logical grouping
2. **Clear dependencies**: src/ has no circular deps
3. **Modular updates**: Change one module at a time
4. **Documentation organized**: Easy to find guides

### For Scaling
1. **Add features**: New modules in src/
2. **Add tools**: New scripts without touching core
3. **Add docs**: Organized folders
4. **Package ready**: src/ can become pip installable

---

## Migration Notes

### What Changed
- Source files moved to `src/`
- Scripts moved to `scripts/`
- Docs organized into `docs/setup/` and `docs/architecture/`
- Config files in `config/`
- Examples in `examples/`

### Import Updates
- Scripts now use `from src.module import Class`
- `sys.path` manipulation in scripts
- Package initialization in `src/__init__.py`

### Path Updates
- `.env.example` → `config/.env.example`
- `companies.csv.example` → `examples/companies.csv.example`
- All documentation paths updated in scripts

---

## Future Enhancements

### tests/ Directory
```
tests/
├── unit/          # Unit tests for each module
├── integration/   # Integration tests
└── fixtures/      # Test data
```

### cli/ Directory (if needed)
```
cli/
├── __init__.py
└── commands/     # Command modules for complex CLI
```

### data/ Directory (if needed)
```
data/
├── cache/        # Local cache files
├── exports/      # Export outputs
└── temp/         # Temporary files
```

---

## Best Practices

1. **Keep src/ pure**: No I/O, no CLI
2. **Scripts orchestrate**: Handle I/O and user interaction
3. **Document as you go**: Update docs/ with changes
4. **Config centralized**: Use config/ for settings
5. **Examples updated**: Keep examples/ current

---

**This structure supports**:
- ✅ Clean MVP development
- ✅ Easy incremental updates
- ✅ Professional organization
- ✅ Future scalability
- ✅ Team collaboration
- ✅ Package distribution

---

*Last updated: October 15, 2025*
