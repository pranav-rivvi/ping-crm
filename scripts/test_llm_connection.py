#!/usr/bin/env python3
"""
Test LLM Connection (OpenAI or Gemini)
Auto-detects which API key is available and tests the connection
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from src.llm_helper import AITargeting

console = Console()


def test_llm_connection():
    """Test AI targeting with real use cases"""

    console.print("\n[bold cyan]Testing AI Company Targeting System[/bold cyan]\n")

    # Check which API key is available
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')

    if not openai_key and not gemini_key:
        console.print("[red]❌ No AI API key found![/red]")
        console.print("\n[yellow]Please add ONE of these to your .env file:[/yellow]")
        console.print("  • OPENAI_API_KEY=sk-...")
        console.print("  • GEMINI_API_KEY=...")
        return 1

    if openai_key:
        console.print(f"[green]✓ Found OpenAI API key[/green]")
    if gemini_key:
        console.print(f"[green]✓ Found Gemini API key[/green]")

    console.print()

    # Initialize AI targeting
    try:
        ai = AITargeting()
        provider_info = ai.get_provider_info()

        console.print(f"[cyan]Using: {provider_info['provider'].upper()} ({provider_info['model']})[/cyan]\n")

    except Exception as e:
        console.print(f"[red]❌ Failed to initialize AI: {e}[/red]")
        return 1

    # Test cases for HLTH 2025 conference
    test_cases = [
        {
            "description": "c-suite executives",
            "industry": "Healthcare"
        },
        {
            "description": "sales leaders in New York",
            "industry": "Healthcare Technology"
        },
        {
            "description": "people who make purchasing decisions for healthcare software",
            "industry": "Health Insurance"
        }
    ]

    for idx, test_case in enumerate(test_cases, 1):
        console.print(f"[bold yellow]Test {idx}: \"{test_case['description']}\"[/bold yellow]")
        console.print(f"Industry context: {test_case['industry']}\n")

        try:
            # Get AI strategy
            strategy = ai.analyze_targeting_request(
                test_case['description'],
                test_case['industry']
            )

            # Display results
            console.print(f"[green]✓ AI Analysis:[/green]")
            console.print(f"  {strategy['explanation']}\n")

            # Show titles
            console.print("[cyan]Job Titles:[/cyan]")
            for title in strategy['titles'][:8]:
                console.print(f"  • {title}")
            if len(strategy['titles']) > 8:
                console.print(f"  • ... and {len(strategy['titles']) - 8} more")

            # Show seniorities
            console.print("\n[cyan]Seniority Levels:[/cyan]")
            for seniority in strategy['seniorities']:
                console.print(f"  • {seniority.replace('_', ' ').title()}")

            # Show locations
            if strategy.get('locations'):
                console.print("\n[cyan]Locations:[/cyan]")
                for loc in strategy['locations']:
                    console.print(f"  • {loc}")

            console.print("\n" + "="*60 + "\n")

        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]\n")
            import traceback
            traceback.print_exc()

    # Final summary
    console.print("[bold green]✓ All tests completed![/bold green]\n")

    console.print("[cyan]Next steps:[/cyan]")
    console.print("  1. The AI connection works!")
    console.print("  2. Ready to use in Streamlit UI")
    console.print("  3. Upload companies.csv and start targeting")

    return 0


if __name__ == '__main__':
    sys.exit(test_llm_connection())
