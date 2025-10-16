"""
Smart LLM Helper - Auto-detects OpenAI or Gemini from .env
Uses whichever API key is available
"""

import os
import json
from typing import Dict, Optional


class SmartLLM:
    """Auto-detect and use OpenAI or Gemini based on available API key"""

    def __init__(self, openai_key: Optional[str] = None, gemini_key: Optional[str] = None):
        """
        Initialize with API keys (auto-detects from env if not provided)

        Args:
            openai_key: OpenAI API key (optional, checks env)
            gemini_key: Gemini API key (optional, checks env)
        """
        self.openai_key = openai_key or os.getenv('OPENAI_API_KEY')
        self.gemini_key = gemini_key or os.getenv('GEMINI_API_KEY')

        # Determine which provider to use
        if self.openai_key:
            self.provider = 'openai'
            self._init_openai()
        elif self.gemini_key:
            self.provider = 'gemini'
            self._init_gemini()
        else:
            raise ValueError("No AI API key found. Please set OPENAI_API_KEY or GEMINI_API_KEY in .env")

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_key)
            self.model = "gpt-4o-mini"  # Cheapest, fastest OpenAI model
            print(f"✓ Using OpenAI ({self.model})")
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

    def _init_gemini(self):
        """Initialize Gemini client"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            self.client = genai.GenerativeModel('gemini-1.5-flash')  # Fast, cheap Gemini model
            self.model = "gemini-1.5-flash"
            print(f"✓ Using Gemini ({self.model})")
        except ImportError:
            raise ImportError("Gemini package not installed. Run: pip install google-generativeai")

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate text using whichever LLM is available

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)

        Returns:
            Generated text
        """
        if self.provider == 'openai':
            return self._generate_openai(prompt, system_prompt)
        else:
            return self._generate_gemini(prompt, system_prompt)

    def _generate_openai(self, prompt: str, system_prompt: str = None) -> str:
        """Generate with OpenAI"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )

        return response.choices[0].message.content

    def _generate_gemini(self, prompt: str, system_prompt: str = None) -> str:
        """Generate with Gemini"""
        # Combine system prompt with user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = self.client.generate_content(
            full_prompt,
            generation_config={
                'temperature': 0.3,
                'max_output_tokens': 800,
            }
        )

        return response.text


class AITargeting:
    """AI-powered targeting strategy generator"""

    def __init__(self):
        """Initialize with auto-detected LLM"""
        self.llm = SmartLLM()

    def analyze_targeting_request(
        self,
        user_description: str,
        company_industry: str = None
    ) -> Dict:
        """
        Convert natural language to Apollo search parameters

        Args:
            user_description: "people who buy enterprise software"
            company_industry: "Healthcare" (optional)

        Returns:
            {
                "titles": ["CTO", "VP IT", ...],
                "seniorities": ["c_suite", "vp"],
                "locations": ["New York"] or None,
                "explanation": "..."
            }
        """

        system_prompt = """You are a B2B sales targeting expert. Your job is to convert natural language descriptions into specific job titles and search parameters.

ALWAYS return ONLY valid JSON. No other text."""

        user_prompt = f"""
Convert this targeting request into specific search parameters.

USER REQUEST: "{user_description}"
COMPANY INDUSTRY: {company_industry or "Not specified"}

Generate:
1. 10-15 specific job titles that match this request
2. Appropriate seniority levels
3. Location requirements (if mentioned)
4. Brief explanation

Return ONLY valid JSON in this EXACT format:
{{
  "titles": ["exact", "job", "titles"],
  "seniorities": ["c_suite", "vp", "director"],
  "locations": ["City/State"] or null,
  "explanation": "Brief explanation"
}}

SENIORITY OPTIONS (use only these):
- "c_suite" (CEO, CTO, CFO, CMO, etc.)
- "vp" (Vice Presidents, SVP)
- "director" (Directors)
- "manager" (Managers)
- "senior" (Senior ICs)

EXAMPLES:

Input: "c-suite executives"
Output:
{{
  "titles": ["CEO", "Chief Executive Officer", "COO", "Chief Operating Officer", "CFO", "Chief Financial Officer", "CTO", "Chief Technology Officer", "CMO", "Chief Marketing Officer", "President"],
  "seniorities": ["c_suite"],
  "locations": null,
  "explanation": "Targeting top-level C-suite executives across all functions"
}}

Input: "sales leaders in New York"
Output:
{{
  "titles": ["VP Sales", "Vice President of Sales", "SVP Sales", "Director of Sales", "Head of Sales", "Chief Revenue Officer"],
  "seniorities": ["c_suite", "vp", "director"],
  "locations": ["New York"],
  "explanation": "Targeting senior sales leadership in New York"
}}

Input: "people who make software purchasing decisions"
Output:
{{
  "titles": ["CTO", "Chief Technology Officer", "VP Technology", "VP IT", "CIO", "Chief Information Officer", "VP Engineering", "Director IT"],
  "seniorities": ["c_suite", "vp", "director"],
  "locations": null,
  "explanation": "Targeting technology decision-makers who control IT/software budgets"
}}

Now convert this request:
"""

        # Generate response
        response_text = self.llm.generate(user_prompt, system_prompt)

        # Clean up response (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        # Parse JSON
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as e:
            # Fallback: extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError(f"Failed to parse AI response as JSON: {response_text[:200]}")

        # Validate required fields
        if 'titles' not in result or 'seniorities' not in result:
            raise ValueError("AI response missing required fields (titles, seniorities)")

        # Ensure locations is null instead of empty list
        if result.get('locations') == []:
            result['locations'] = None

        return result

    def get_provider_info(self) -> Dict:
        """Get information about current LLM provider"""
        return {
            'provider': self.llm.provider,
            'model': self.llm.model
        }
