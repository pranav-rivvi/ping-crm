#!/usr/bin/env python3
"""
Setup Validation Script
Validates that all dependencies and configurations are correct
"""

import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

console = Console()


def check_python_version():
    """Check Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)"


def check_dependencies():
    """Check all required packages are installed"""
    required_packages = {
        'requests': 'requests',
        'pandas': 'pandas',
        'notion_client': 'notion_client',
        'python-dotenv': 'dotenv',
        'rich': 'rich',
        'tenacity': 'tenacity',
        'click': 'click'
    }

    results = {}
    for display_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            results[display_name] = (True, "✓ Installed")
        except ImportError:
            results[display_name] = (False, "✗ Missing")

    return results


def check_env_file():
    """Check if .env file exists and has required keys"""
    # Check in project root
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'

    if not env_path.exists():
        return False, "✗ .env file not found in project root"

    # Load and check keys
    from dotenv import load_dotenv
    load_dotenv(env_path)

    required_keys = ['APOLLO_API_KEY', 'NOTION_TOKEN', 'NOTION_DB_ID']
    missing_keys = []

    for key in required_keys:
        value = os.getenv(key)
        if not value or value == f'your_{key.lower()}_here' or 'your_' in value:
            missing_keys.append(key)

    if missing_keys:
        return False, f"✗ Missing/invalid: {', '.join(missing_keys)}"

    return True, "✓ All keys configured"


def check_project_files():
    """Check all required project files exist"""
    project_root = Path(__file__).parent.parent

    required_files = {
        'src/apollo_client.py': project_root / 'src' / 'apollo_client.py',
        'src/notion_sync.py': project_root / 'src' / 'notion_sync.py',
        'src/processors.py': project_root / 'src' / 'processors.py',
        'scripts/enrich.py': project_root / 'scripts' / 'enrich.py',
        'requirements.txt': project_root / 'requirements.txt',
        'config/.env.example': project_root / 'config' / '.env.example'
    }

    results = {}
    for display_name, file_path in required_files.items():
        exists = file_path.exists()
        results[display_name] = (exists, "✓ Found" if exists else "✗ Missing")

    return results


def test_imports():
    """Test that all custom modules can be imported"""
    results = {}

    try:
        from src.apollo_client import ApolloClient
        results['src.apollo_client'] = (True, "✓ OK")
    except Exception as e:
        results['src.apollo_client'] = (False, f"✗ Error: {str(e)[:40]}")

    try:
        from src.notion_sync import NotionClient
        results['src.notion_sync'] = (True, "✓ OK")
    except Exception as e:
        results['src.notion_sync'] = (False, f"✗ Error: {str(e)[:40]}")

    try:
        from src.processors import TierAssigner, PriorityScorer
        results['src.processors'] = (True, "✓ OK")
    except Exception as e:
        results['src.processors'] = (False, f"✗ Error: {str(e)[:40]}")

    return results


def main():
    """Run all validation checks"""
    console.print(Panel.fit(
        "[bold blue]HLTH 2025 CRM - Setup Validation[/bold blue]\n"
        "Checking system requirements and configuration",
        border_style="blue"
    ))

    all_passed = True

    # Python version check
    console.print("\n[bold]1. Python Version[/bold]")
    py_ok, py_msg = check_python_version()
    if py_ok:
        console.print(f"   [green]{py_msg}[/green]")
    else:
        console.print(f"   [red]{py_msg}[/red]")
        all_passed = False

    # Dependencies check
    console.print("\n[bold]2. Python Dependencies[/bold]")
    deps = check_dependencies()
    dep_table = Table(show_header=False, box=None, padding=(0, 2))
    dep_table.add_column("Package", style="cyan")
    dep_table.add_column("Status")

    for pkg, (ok, msg) in deps.items():
        color = "green" if ok else "red"
        dep_table.add_row(pkg, f"[{color}]{msg}[/{color}]")
        if not ok:
            all_passed = False

    console.print(dep_table)

    if not all(ok for ok, _ in deps.values()):
        console.print("\n   [yellow]Install missing dependencies: pip install -r requirements.txt[/yellow]")

    # Environment file check
    console.print("\n[bold]3. Environment Configuration[/bold]")
    env_ok, env_msg = check_env_file()
    if env_ok:
        console.print(f"   [green]{env_msg}[/green]")
    else:
        console.print(f"   [red]{env_msg}[/red]")
        console.print("   [yellow]Copy config/.env.example to .env and fill in your API keys[/yellow]")
        all_passed = False

    # Project files check
    console.print("\n[bold]4. Project Files[/bold]")
    files = check_project_files()
    file_table = Table(show_header=False, box=None, padding=(0, 2))
    file_table.add_column("File", style="cyan")
    file_table.add_column("Status")

    for file, (ok, msg) in files.items():
        color = "green" if ok else "red"
        file_table.add_row(file, f"[{color}]{msg}[/{color}]")
        if not ok:
            all_passed = False

    console.print(file_table)

    # Module imports check
    console.print("\n[bold]5. Module Imports[/bold]")
    imports = test_imports()
    import_table = Table(show_header=False, box=None, padding=(0, 2))
    import_table.add_column("Module", style="cyan")
    import_table.add_column("Status")

    for module, (ok, msg) in imports.items():
        color = "green" if ok else "red"
        import_table.add_row(module, f"[{color}]{msg}[/{color}]")
        if not ok:
            all_passed = False

    console.print(import_table)

    # Final status
    console.print("\n" + "="*60)
    if all_passed:
        console.print(Panel.fit(
            "[bold green]✓ All checks passed![/bold green]\n"
            "You're ready to run: python scripts/enrich.py companies.csv",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]✗ Some checks failed[/bold red]\n"
            "Please fix the issues above before running the enrichment",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == '__main__':
    main()
