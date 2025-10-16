#!/usr/bin/env python3
"""
HLTH 2025 CRM - Bulk Enrichment UI
Streamlit app for mass contact enrichment
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment
load_dotenv()

from src.apollo_client import ApolloClient
from src.notion_client import NotionClient
from src.llm_helper import AITargeting

# Page config
st.set_page_config(
    page_title="HLTH 2025 CRM - Bulk Enrichment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional UX Design with Dark Mode Support
st.markdown("""
<style>
    /* ============================================
       LIGHT MODE (DEFAULT)
       ============================================ */

    /* Main Layout */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }

    /* Sidebar Styling - Modern & Clean */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2c3e50;
        font-weight: 600;
    }

    /* Sidebar Sections */
    .sidebar-section {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }

    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }

    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }

    /* Stat boxes */
    .stat-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }

    /* Template download section */
    .template-section {
        background: #fff3cd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }

    /* Divider */
    .divider {
        border-top: 1px solid #e9ecef;
        margin: 1.5rem 0;
    }

    /* Help text */
    .help-text {
        color: #6c757d;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }

    /* ============================================
       DARK MODE
       ============================================ */

    @media (prefers-color-scheme: dark) {
        /* Main Layout - Dark Mode */
        .main-header {
            color: #4da6ff;
        }

        .sub-header {
            color: #b0b0b0;
        }

        /* Sidebar - Dark Mode */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%) !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #e0e0e0 !important;
        }

        /* Sidebar Sections - Dark Mode */
        .sidebar-section {
            background: #1e1e1e;
            box-shadow: 0 2px 4px rgba(0,0,0,0.4);
        }

        /* Status indicators - Dark Mode */
        .status-success {
            background: #1e4620;
            color: #7dff7d;
            border-left: 4px solid #4caf50;
        }

        .status-error {
            background: #4a1a1f;
            color: #ff7d7d;
            border-left: 4px solid #f44336;
        }

        /* Info boxes - Dark Mode */
        .info-box {
            background: #1a2a3a;
            border-left: 4px solid #42a5f5;
            color: #b3d9ff;
        }

        /* Stat boxes - Dark Mode */
        .stat-box {
            background: #1e1e1e;
            border: 1px solid #333;
            color: #e0e0e0;
        }

        /* Template download section - Dark Mode */
        .template-section {
            background: #3a3318;
            border-left: 4px solid #ffb300;
            color: #ffe066;
        }

        /* Divider - Dark Mode */
        .divider {
            border-top: 1px solid #333;
        }

        /* Help text - Dark Mode */
        .help-text {
            color: #999;
        }

        /* Streamlit elements - Dark Mode overrides */
        [data-testid="stMarkdownContainer"] {
            color: #e0e0e0;
        }

        /* Make text inputs readable in dark mode */
        [data-baseweb="input"] {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
        }

        [data-baseweb="textarea"] {
            background-color: #2a2a2a !important;
            color: #e0e0e0 !important;
        }

        /* Buttons in dark mode */
        [data-testid="stButton"] button {
            color: #e0e0e0;
        }

        /* Metrics in dark mode */
        [data-testid="stMetricValue"] {
            color: #4da6ff;
        }

        /* DataFrames in dark mode */
        [data-testid="stDataFrame"] {
            background-color: #1e1e1e;
        }

        /* Expander in dark mode */
        [data-testid="stExpander"] {
            background-color: #1e1e1e;
            border: 1px solid #333;
        }

        /* File uploader in dark mode */
        [data-testid="stFileUploader"] {
            background-color: #1e1e1e;
        }

        /* Progress bar in dark mode */
        [data-testid="stProgress"] > div > div {
            background-color: #4da6ff;
        }

        /* Radio buttons in dark mode */
        [data-testid="stRadio"] label {
            color: #e0e0e0;
        }

        /* Checkboxes in dark mode */
        [data-testid="stCheckbox"] label {
            color: #e0e0e0;
        }

        /* Slider in dark mode */
        [data-testid="stSlider"] {
            color: #e0e0e0;
        }
    }
</style>
""", unsafe_allow_html=True)


def validate_env():
    """Check if environment variables are set"""
    required = ['APOLLO_API_KEY', 'NOTION_TOKEN', 'NOTION_DB_ID']
    missing = [key for key in required if not os.getenv(key)]
    return len(missing) == 0, missing


def enrich_contact_flexible(row, apollo, notion):
    """
    Enrich contact with flexible search priority:
    1. LinkedIn URL (unique key)
    2. Email (unique key)
    3. Name + Company (composite key)
    """
    try:
        # Extract available fields
        linkedin_url = row.get('linkedin_url', '').strip() if 'linkedin_url' in row else ''
        email = row.get('email', '').strip() if 'email' in row else ''
        person_name = row.get('person_name', '').strip() if 'person_name' in row else ''
        company_name = row.get('company_name', '').strip() if 'company_name' in row else ''

        person_data = None
        company_data = None
        search_method = ''

        # Priority 1: LinkedIn URL (highest priority)
        if linkedin_url and 'linkedin.com' in linkedin_url.lower():
            search_method = 'LinkedIn'
            person_data, company_data = apollo.search_by_linkedin_url(linkedin_url)

        # Priority 2: Email
        if not person_data and email and '@' in email:
            search_method = 'Email'
            person_data, company_data = apollo.search_by_email(email)

        # Priority 3: Name + Company
        if not person_data and person_name and company_name:
            search_method = 'Name+Company'
            company_data = apollo.search_company(company_name)
            if company_data:
                person_data = apollo.search_person_by_name(person_name, company_name)

        # If still no data found
        if not person_data:
            identifier = linkedin_url or email or person_name or 'Unknown'
            return {
                'status': 'failed',
                'person': identifier,
                'company': company_name or 'Unknown',
                'message': f'Not found in Apollo (tried: {search_method or "none"})',
                'data': {}
            }

        # Extract final names
        final_person_name = person_data.get('name', person_name or email or linkedin_url)
        final_company_name = company_data.get('name', company_name) if company_data else company_name

        # Check if exists in Notion
        existing = notion.find_contact(final_person_name, final_company_name)
        if existing:
            return {
                'status': 'skipped',
                'person': final_person_name,
                'company': final_company_name,
                'message': f'Already exists (found via {search_method})',
                'data': person_data
            }

        # Upsert to Notion
        success, action = notion.upsert_contact(
            contact_name=final_person_name,
            company_name=final_company_name,
            enriched_data=person_data,
            company_data=company_data
        )

        if success:
            return {
                'status': 'success',
                'person': final_person_name,
                'company': final_company_name,
                'message': f'{action.capitalize()}d via {search_method}',
                'data': person_data
            }
        else:
            return {
                'status': 'failed',
                'person': final_person_name,
                'company': final_company_name,
                'message': 'Failed to write to Notion',
                'data': {}
            }

    except Exception as e:
        identifier = row.get('person_name') or row.get('email') or row.get('linkedin_url') or 'Unknown'
        return {
            'status': 'failed',
            'person': str(identifier),
            'company': row.get('company_name', 'Unknown'),
            'message': str(e),
            'data': {}
        }


def validate_user_keys(apollo_key, notion_token, notion_db_id, ai_key=None):
    """Validate user's API keys by testing connections"""
    try:
        # Test Apollo
        apollo = ApolloClient(apollo_key)
        # Simple test - search for a common company
        test_company = apollo.search_company("Google")
        if not test_company:
            return False, "Apollo API key invalid - couldn't connect to Apollo.io"

        # Test Notion
        notion = NotionClient(notion_token, notion_db_id)
        # Try to query the database
        from notion_client import Client
        client = Client(auth=notion_token)
        try:
            client.databases.query(database_id=notion_db_id, page_size=1)
        except Exception as e:
            return False, f"Notion credentials invalid - {str(e)}"

        # Test AI (optional)
        if ai_key:
            if ai_key.startswith('sk-'):
                # OpenAI key
                import openai
                openai.api_key = ai_key
                try:
                    openai.models.list()
                except Exception as e:
                    return False, f"OpenAI API key invalid - {str(e)}"
            else:
                # Gemini key
                import google.generativeai as genai
                try:
                    genai.configure(api_key=ai_key)
                    genai.list_models()
                except Exception as e:
                    return False, f"Gemini API key invalid - {str(e)}"

        return True, "All API keys validated successfully!"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def show_setup_screen():
    """Show login and API key setup screen"""
    st.markdown('<p class="main-header">🏥 Ping CRM - Setup</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Enter your email and API keys to get started</p>', unsafe_allow_html=True)

    st.markdown("---")

    with st.form("setup_form"):
        st.markdown("### 👤 Your Information")

        user_email = st.text_input(
            "Email Address",
            placeholder="your.email@company.com",
            help="Your email for identification"
        )

        st.markdown("### 🔑 API Keys")
        st.caption("All keys are stored only in your session and never saved permanently")

        apollo_key = st.text_input(
            "Apollo.io API Key",
            type="password",
            placeholder="Enter your Apollo API key",
            help="Get from: https://app.apollo.io/#/settings/integrations/api"
        )

        notion_token = st.text_input(
            "Notion Integration Token",
            type="password",
            placeholder="secret_...",
            help="Get from: https://www.notion.so/my-integrations"
        )

        notion_db_id = st.text_input(
            "Notion Database ID",
            type="password",
            placeholder="32-character database ID",
            help="Copy from your Notion database URL"
        )

        st.markdown("### 🤖 AI API Key (Choose one)")

        ai_provider = st.radio(
            "AI Provider",
            ["OpenAI (Recommended)", "Google Gemini"],
            horizontal=True
        )

        ai_key = st.text_input(
            f"{ai_provider.split()[0]} API Key",
            type="password",
            placeholder="sk-... (OpenAI) or your Gemini key",
            help="For AI-powered company targeting"
        )

        st.markdown("---")

        col1, col2 = st.columns([1, 1])

        with col1:
            validate_button = st.form_submit_button(
                "🔍 Validate & Continue",
                type="primary",
                use_container_width=True
            )

        with col2:
            if st.form_submit_button("📖 Need Help?", use_container_width=True):
                st.info("Check QUICKSTART_FOR_FRIEND.md for detailed setup instructions")

        if validate_button:
            if not user_email or '@' not in user_email:
                st.error("❌ Please enter a valid email address")
                return False

            if not all([apollo_key, notion_token, notion_db_id, ai_key]):
                st.error("❌ Please fill in all API keys")
                return False

            # Validate keys
            with st.spinner("🔍 Validating your API keys..."):
                success, message = validate_user_keys(apollo_key, notion_token, notion_db_id, ai_key)

            if success:
                st.success(f"✅ {message}")
                st.balloons()

                # Store in session state
                st.session_state.user_email = user_email
                st.session_state.user_setup_complete = True
                st.session_state.apollo_key = apollo_key
                st.session_state.notion_token = notion_token
                st.session_state.notion_db_id = notion_db_id
                st.session_state.ai_key = ai_key
                st.session_state.ai_provider = "openai" if ai_provider.startswith("OpenAI") else "gemini"

                # Set environment variables for this session
                os.environ['APOLLO_API_KEY'] = apollo_key
                os.environ['NOTION_TOKEN'] = notion_token
                os.environ['NOTION_DB_ID'] = notion_db_id

                if st.session_state.ai_provider == "openai":
                    os.environ['OPENAI_API_KEY'] = ai_key
                else:
                    os.environ['GEMINI_API_KEY'] = ai_key

                st.rerun()
            else:
                st.error(f"❌ {message}")
                st.info("💡 Double-check your API keys and try again")
                return False

    return False


def main():
    """Main app"""

    # Check if user has completed setup
    if 'user_setup_complete' not in st.session_state:
        show_setup_screen()
        return

    # Show user info in sidebar
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as:")
        st.caption(st.session_state.user_email)

        if st.button("🚪 Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Header
    st.markdown('<p class="main-header">🏥 Ping CRM - Contact Enrichment</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered contact enrichment with Apollo.io and Notion</p>', unsafe_allow_html=True)

    # Sidebar - Professional UX Design
    with st.sidebar:
        # Logo/Brand Section
        st.markdown("### 🏥 Ping CRM")
        st.caption("Intelligent Contact Enrichment Platform")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # System Status
        st.markdown("#### System Status")
        st.markdown('<div class="status-success">✅ All Systems Ready</div>', unsafe_allow_html=True)
        st.caption(f"Using {st.session_state.ai_provider.upper()} for AI targeting")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Quick Guide Section
        with st.expander("📖 Quick Guide", expanded=False):
            st.markdown("""
            **CSV Format Requirements:**

            Include at least ONE identifier:
            - `linkedin_url` (highest priority)
            - `email` (second priority)
            - `person_name` + `company_name` (third)

            **Search Priority:**
            LinkedIn → Email → Name+Company

            System tries in order until match found.
            """)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Settings Section
        with st.expander("⚙️ Settings", expanded=False):
            st.markdown("**Rate Limiting**")
            st.caption("Prevents API rate limiting errors")

            delay = st.slider(
                "Delay between requests",
                min_value=0.5,
                max_value=5.0,
                value=1.5,
                step=0.5,
                format="%.1f sec",
                label_visibility="collapsed"
            )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Templates Section
        st.markdown("#### 📥 Download Templates")

        st.caption("Start with a template to ensure correct formatting")

        template_full = "linkedin_url,email,person_name,company_name\nhttps://linkedin.com/in/user1,karen@cvs.com,Karen Lynch,CVS Health\n,bruce@humana.com,Bruce Broussard,Humana\n,,Gail Boudreaux,Elevance Health"
        st.download_button(
            label="📋 Full Template (All Fields)",
            data=template_full,
            file_name="contacts_template_full.csv",
            mime="text/csv",
            use_container_width=True
        )

        template_simple = "person_name,company_name\nKaren Lynch,CVS Health\nBruce Broussard,Humana\nGail Boudreaux,Elevance Health"
        st.download_button(
            label="📄 Simple Template (Name + Company)",
            data=template_simple,
            file_name="contacts_template_simple.csv",
            mime="text/csv",
            use_container_width=True
        )

        template_companies = "company_name\nCVS Health\nHumana\nUnitedHealth Group\nCigna\nElevance Health"
        st.download_button(
            label="🏢 Companies Template (AI Targeting)",
            data=template_companies,
            file_name="companies_template.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Help Section
        st.markdown("#### ℹ️ Need Help?")
        st.caption("Refer to documentation or run validation script")

        if st.button("🔍 Validate Setup", use_container_width=True):
            st.info("Run: `python scripts/validate_setup.py`")

        # Footer
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.caption("Built for HLTH Vegas 2025")
        st.caption("Version 1.0 with AI Targeting")

    # Main content - AI Company Targeting is now the primary feature
    tab1, tab2 = st.tabs(["🎯 AI Company Targeting", "👥 Enrich Profiles"])

    with tab1:
        # AI Company Targeting Tab (Primary Feature)
        # Initialize clients
        if 'apollo' not in st.session_state:
            with st.spinner("Initializing API clients..."):
                st.session_state.apollo = ApolloClient(os.getenv('APOLLO_API_KEY'))
                st.session_state.notion = NotionClient(
                    os.getenv('NOTION_TOKEN'),
                    os.getenv('NOTION_DB_ID')
                )

        # Streamlined header
        st.markdown("### 🎯 AI-Powered Company Targeting")
        st.markdown("---")

        # Step 1: Define your search FIRST
        st.markdown("#### 1️⃣ What Are You Looking For?")

        user_description = st.text_area(
            "Describe who you want to find",
            placeholder="Examples:\n• C-suite executives for partnership discussions at HLTH 2025\n• Sales and marketing leaders in California\n• Technology decision-makers who buy enterprise software\n• Operations managers handling supply chain",
            height=80,
            key="target_description",
            help="Use natural language! AI translates your description into job titles, seniority levels, and location filters."
        )

        st.markdown("")  # Spacing

        # Number of people - More prominent
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            num_people = st.slider(
                "👥 Contacts per company",
                min_value=1,
                max_value=7,
                value=5,
                key="num_people_slider",
                help="1-3 = Senior executives only | 4-5 = Balanced coverage | 6-7 = Broad team"
            )

        with col2:
            st.metric("Per Company", num_people)

        with col3:
            # Will update after upload
            if 'companies_count' in st.session_state:
                st.metric("Total Expected", f"~{st.session_state.companies_count * num_people}")
            else:
                st.metric("Total Expected", "—")

        st.markdown("")  # Spacing

        # Field selection
        with st.expander("⚙️ Select Fields to Populate", expanded=False):
            st.caption("Choose which Apollo data fields to add to your Notion tracker")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Contact Info**")
                include_email = st.checkbox("Email", value=True, key="field_email")
                include_phone = st.checkbox("Phone", value=True, key="field_phone")
                include_linkedin = st.checkbox("LinkedIn URL", value=True, key="field_linkedin")
                include_title = st.checkbox("Job Title", value=True, key="field_title")

            with col2:
                st.markdown("**Location**")
                include_city = st.checkbox("City", value=True, key="field_city")
                include_state = st.checkbox("State", value=True, key="field_state")
                include_country = st.checkbox("Country", value=True, key="field_country")

            with col3:
                st.markdown("**Other**")
                include_seniority = st.checkbox("Seniority Level", value=True, key="field_seniority")
                include_company_info = st.checkbox("Company Details", value=True, key="field_company")

            # Store selections in session state
            st.session_state.field_selections = {
                'email': include_email,
                'phone': include_phone,
                'linkedin_url': include_linkedin,
                'title': include_title,
                'city': include_city,
                'state': include_state,
                'country': include_country,
                'seniority': include_seniority,
                'company_info': include_company_info
            }

        st.markdown("---")

        # Step 2: Add companies
        st.markdown("#### 2️⃣ Add Target Companies")
        st.caption("Choose how you want to add companies")

        input_method = st.radio(
            "Input method",
            ["Single Company", "Upload CSV"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if input_method == "Single Company":
            # Single company input
            company_input = st.text_input(
                "Company name or website URL",
                placeholder="e.g., CVS Health  OR  www.cvshealth.com",
                help="Enter a company name (e.g., 'CVS Health') or website URL (e.g., 'cvshealth.com')"
            )

            if company_input:
                # Parse input - could be name or URL
                if 'http' in company_input or 'www.' in company_input or '.com' in company_input:
                    # It's a URL - extract domain
                    domain = company_input.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
                    st.info(f"🔍 Will search for company with domain: **{domain}**")
                    # Store as single-item dataframe
                    st.session_state.df_companies = pd.DataFrame({'company_name': [domain]})
                    st.session_state.companies_count = 1
                    st.session_state.input_is_domain = True
                else:
                    # It's a company name
                    st.success(f"✅ Ready to search: **{company_input}**")
                    st.session_state.df_companies = pd.DataFrame({'company_name': [company_input]})
                    st.session_state.companies_count = 1
                    st.session_state.input_is_domain = False

        else:
            # CSV upload
            uploaded_companies = st.file_uploader(
                "CSV file with company names",
                type=['csv'],
                key="companies_csv",
                help="CSV with one column: 'company_name'. Example: CVS Health, Humana, Cigna"
            )

            # Template download right under uploader
            st.caption("📥 Don't have a CSV? Download a template:")
            template_companies = "company_name\nCVS Health\nHumana\nUnitedHealth Group\nCigna\nElevance Health"
            st.download_button(
                label="📄 Download Companies Template",
                data=template_companies,
                file_name="companies_template.csv",
                mime="text/csv",
                use_container_width=False
            )

            if uploaded_companies:
                df_companies = pd.read_csv(uploaded_companies)

                if 'company_name' not in df_companies.columns:
                    st.error("❌ CSV must have 'company_name' column")
                    st.stop()

                st.success(f"✅ Loaded **{len(df_companies)} companies**")
                st.session_state.df_companies = df_companies
                st.session_state.companies_count = len(df_companies)
                st.session_state.input_is_domain = False

                with st.expander("📋 Preview companies", expanded=False):
                    st.dataframe(df_companies, use_container_width=True)

        st.markdown("---")

        # Step 3: Execute (only show if we have companies and description)
        if 'df_companies' in st.session_state and user_description:
            st.markdown("#### 3️⃣ Execute Your Search")

            col1, col2 = st.columns([1, 1])

            with col1:
                preview_button = st.button(
                    "🔍 Preview AI Strategy",
                    type="secondary",
                    use_container_width=True,
                    key="preview_ai_strategy",
                    help="See exactly what AI will search for before running"
                )

            with col2:
                start_button = st.button(
                    "🚀 Find & Add to Notion",
                    type="primary",
                    use_container_width=True,
                    key="start_ai_targeting",
                    help="Start the search and automatically add all contacts to Notion"
                )

            # Preview AI strategy
            if preview_button and user_description:
                with st.spinner("🤖 AI is analyzing your request..."):
                    ai = AITargeting()

                    # Get industry context from first company
                    first_company = st.session_state.df_companies.iloc[0]['company_name']
                    company_data = st.session_state.apollo.search_company(first_company)
                    industry = company_data.get('industry', '') if company_data else ''

                    strategy = ai.analyze_targeting_request(user_description, industry)

                    # Store in session
                    st.session_state.ai_strategy = strategy

                # Display strategy preview
                st.markdown("### 🤖 AI Search Strategy Preview")

                st.success(f"✅ **{strategy['explanation']}**")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**🎯 Job Titles to Search:**")
                    for idx, title in enumerate(strategy['titles'][:10], 1):
                        st.markdown(f"{idx}. {title}")
                    if len(strategy['titles']) > 10:
                        st.markdown(f"  _...and {len(strategy['titles']) - 10} more titles_")

                with col2:
                    st.markdown("**📊 Seniority Levels:**")
                    for seniority in strategy['seniorities']:
                        st.markdown(f"• {seniority.replace('_', ' ').title()}")

                    if strategy.get('locations'):
                        st.markdown("\n**📍 Locations:**")
                        for loc in strategy['locations']:
                            st.markdown(f"• {loc}")
                    else:
                        st.markdown("\n**📍 Locations:** All (no filter)")

                st.info("👆 Looks good? Click **'Find & Add to Notion'** to start!")

            # Start search
            if start_button and user_description:
                # Get or generate AI strategy
                if 'ai_strategy' not in st.session_state:
                    with st.spinner("🤖 AI is analyzing your goal..."):
                        ai = AITargeting()

                        # Get industry context from first company
                        first_company = st.session_state.df_companies.iloc[0]['company_name']
                        company_data = st.session_state.apollo.search_company(first_company)
                        industry = company_data.get('industry', '') if company_data else ''

                        strategy = ai.analyze_targeting_request(user_description, industry)
                        st.session_state.ai_strategy = strategy
                else:
                    strategy = st.session_state.ai_strategy

                # Show AI strategy being used
                st.markdown("### 🤖 Using AI Strategy")
                st.success(f"**{strategy['explanation']}**")

                with st.expander("📋 Search details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Searching for these titles:**")
                        for title in strategy['titles'][:8]:
                            st.markdown(f"• {title}")
                        if len(strategy['titles']) > 8:
                            st.markdown(f"  _...and {len(strategy['titles']) - 8} more_")

                    with col2:
                        st.markdown("**Seniority levels:**")
                        for seniority in strategy['seniorities']:
                            st.markdown(f"• {seniority.replace('_', ' ').title()}")

                st.divider()

                # Initialize tracking
                if 'company_results' not in st.session_state:
                    st.session_state.company_results = []
                    st.session_state.company_stats = {
                        'companies_processed': 0,
                        'total_found': 0,
                        'total_added': 0,
                        'total_skipped': 0
                    }

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Stats display
                col1, col2, col3, col4 = st.columns(4)
                stat_companies = col1.empty()
                stat_found = col2.empty()
                stat_added = col3.empty()
                stat_skipped = col4.empty()

                # Results display
                results_container = st.empty()

                # Process each company
                df_companies = st.session_state.df_companies
                total_companies = len(df_companies)

                for idx, row in df_companies.iterrows():
                    company_name = row['company_name']

                    status_text.info(f"Processing {idx + 1}/{total_companies}: {company_name}")

                    try:
                        # Search company
                        company_data = st.session_state.apollo.search_company(company_name)

                        if not company_data:
                            st.session_state.company_results.append({
                                'company': company_name,
                                'status': 'not_found',
                                'found': 0,
                                'added': 0,
                                'people': []
                            })
                            continue

                        # Search people with AI strategy
                        people = st.session_state.apollo.search_people_by_company(
                            company_id=company_data['apollo_id'],
                            titles=strategy['titles'],
                            seniorities=strategy['seniorities'],
                            locations=strategy.get('locations'),
                            max_results=num_people
                        )

                        # Add to Notion
                        added_count = 0
                        skipped_count = 0

                        for person in people:
                            # Check if exists
                            existing = st.session_state.notion.find_contact(
                                person['name'],
                                company_data['name']
                            )

                            if existing:
                                skipped_count += 1
                                continue

                            # Filter person data based on user's field selections
                            field_selections = st.session_state.get('field_selections', {})
                            filtered_person = {'name': person['name']}  # Name is always included

                            if field_selections.get('email', True):
                                filtered_person['email'] = person.get('email')
                            if field_selections.get('phone', True):
                                filtered_person['phone'] = person.get('phone')
                            if field_selections.get('linkedin_url', True):
                                filtered_person['linkedin_url'] = person.get('linkedin_url')
                            if field_selections.get('title', True):
                                filtered_person['title'] = person.get('title')
                            if field_selections.get('city', True):
                                filtered_person['city'] = person.get('city')
                            if field_selections.get('state', True):
                                filtered_person['state'] = person.get('state')
                            if field_selections.get('country', True):
                                filtered_person['country'] = person.get('country')
                            if field_selections.get('seniority', True):
                                filtered_person['seniority'] = person.get('seniority')

                            # Filter company data if not selected
                            filtered_company = company_data if field_selections.get('company_info', True) else None

                            # Add to Notion with personalized outreach context and filtered data
                            success, action = st.session_state.notion.upsert_contact(
                                contact_name=person['name'],
                                company_name=company_data['name'],
                                enriched_data=filtered_person,
                                company_data=filtered_company,
                                outreach_context=user_description  # Pass user's goal as context
                            )

                            if success:
                                added_count += 1

                        # Store results
                        st.session_state.company_results.append({
                            'company': company_name,
                            'status': 'success',
                            'found': len(people),
                            'added': added_count,
                            'skipped': skipped_count,
                            'people': people
                        })

                        # Update stats
                        st.session_state.company_stats['companies_processed'] += 1
                        st.session_state.company_stats['total_found'] += len(people)
                        st.session_state.company_stats['total_added'] += added_count
                        st.session_state.company_stats['total_skipped'] += skipped_count

                    except Exception as e:
                        st.session_state.company_results.append({
                            'company': company_name,
                            'status': 'error',
                            'found': 0,
                            'added': 0,
                            'error': str(e),
                            'people': []
                        })

                    # Update progress
                    progress = (idx + 1) / total_companies
                    progress_bar.progress(progress)

                    # Update stats
                    stat_companies.metric("Companies", st.session_state.company_stats['companies_processed'])
                    stat_found.metric("Found", st.session_state.company_stats['total_found'])
                    stat_added.metric("Added", st.session_state.company_stats['total_added'])
                    stat_skipped.metric("Skipped", st.session_state.company_stats['total_skipped'])

                    # Show recent results
                    with results_container.container():
                        st.markdown("### Recent Results")
                        for result in st.session_state.company_results[-3:]:
                            if result['status'] == 'success':
                                st.success(f"✅ **{result['company']}**: Found {result['found']}, Added {result['added']}, Skipped {result['skipped']}")
                                for person in result['people'][:2]:
                                    st.markdown(f"  • {person['name']} - {person.get('title', 'N/A')}")
                            elif result['status'] == 'not_found':
                                st.warning(f"⚠️ **{result['company']}**: Not found in Apollo")
                            else:
                                st.error(f"❌ **{result['company']}**: {result.get('error', 'Error')}")

                    # Rate limiting
                    if idx < total_companies - 1:
                        time.sleep(1.5)

                # Completion
                status_text.success("✅ All companies processed!")
                st.balloons()

                # Final summary
                st.markdown("### 🎉 Targeting Complete!")
                st.markdown(f"""
                - **Companies processed:** {st.session_state.company_stats['companies_processed']}
                - **Total people found:** {st.session_state.company_stats['total_found']}
                - **Added to Notion:** {st.session_state.company_stats['total_added']}
                - **Already existed:** {st.session_state.company_stats['total_skipped']}
                """)

                # Export option
                if st.session_state.company_results:
                    # Create export DataFrame
                    export_data = []
                    for result in st.session_state.company_results:
                        for person in result.get('people', []):
                            export_data.append({
                                'Company': result['company'],
                                'Name': person['name'],
                                'Title': person.get('title', 'N/A'),
                                'Email': person.get('email', 'N/A'),
                                'LinkedIn': person.get('linkedin_url', 'N/A'),
                                'Location': f"{person.get('city', '')}, {person.get('state', '')}".strip(', ')
                            })

                    if export_data:
                        export_df = pd.DataFrame(export_data)

                        csv = export_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results CSV",
                            data=csv,
                            file_name=f"ai_targeting_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )

                # Reset button
                if st.button("🔄 Start New Search", key="reset_ai_search"):
                    for key in ['company_results', 'company_stats', 'ai_strategy']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()

    with tab2:
        # Enrich Profiles tab
        st.subheader("1️⃣ Upload Your CSV")
        st.caption("📄 Include at least ONE identifier per contact: LinkedIn URL, Email, or Name + Company")

        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="Flexible format: linkedin_url, email, person_name, company_name (at least one required)"
        )

        # Template downloads right under uploader
        st.caption("📥 Don't have a CSV? Download a template:")
        col1, col2 = st.columns(2)

        with col1:
            template_full = "linkedin_url,email,person_name,company_name\nhttps://linkedin.com/in/user1,karen@cvs.com,Karen Lynch,CVS Health\n,bruce@humana.com,Bruce Broussard,Humana\n,,Gail Boudreaux,Elevance Health"
            st.download_button(
                label="📋 Full Template (All Fields)",
                data=template_full,
                file_name="contacts_template_full.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            template_simple = "person_name,company_name\nKaren Lynch,CVS Health\nBruce Broussard,Humana\nGail Boudreaux,Elevance Health"
            st.download_button(
                label="📄 Simple Template (Name + Company)",
                data=template_simple,
                file_name="contacts_template_simple.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Divider
        st.markdown("---")

        # Single LinkedIn/Email Lookup Section
        st.subheader("💼 Quick Single Lookup")
        st.caption("🔍 Look up a single contact by LinkedIn URL or Email address")

        # Initialize clients if not already
        if 'apollo' not in st.session_state:
            with st.spinner("Initializing API clients..."):
                st.session_state.apollo = ApolloClient(os.getenv('APOLLO_API_KEY'))
                st.session_state.notion = NotionClient(
                    os.getenv('NOTION_TOKEN'),
                    os.getenv('NOTION_DB_ID')
                )

        # Input for LinkedIn or Email
        single_input = st.text_input(
            "LinkedIn URL or Email",
            placeholder="e.g., https://linkedin.com/in/username  OR  email@company.com",
            key="single_lookup_input",
            help="Enter a LinkedIn profile URL or email address to look up contact details"
        )

        # Get Details button
        col1, col2 = st.columns([1, 3])
        with col1:
            get_details_button = st.button(
                "🔍 Get Details",
                type="primary",
                use_container_width=True,
                key="get_details_button",
                disabled=not single_input
            )

        # Process single lookup
        if get_details_button and single_input:
            with st.spinner("🔍 Searching Apollo..."):
                person_data = None
                company_data = None
                search_method = ''

                # Determine if it's LinkedIn or Email
                if 'linkedin.com' in single_input.lower():
                    search_method = 'LinkedIn'
                    person_data, company_data = st.session_state.apollo.search_by_linkedin_url(single_input)
                elif '@' in single_input:
                    search_method = 'Email'
                    person_data, company_data = st.session_state.apollo.search_by_email(single_input)
                else:
                    st.error("❌ Please enter a valid LinkedIn URL or Email address")

                # Store in session state for "Add to Notion" button
                if person_data:
                    st.session_state.single_lookup_person = person_data
                    st.session_state.single_lookup_company = company_data
                    st.session_state.single_lookup_method = search_method

                    # Display results
                    st.success(f"✅ Found via {search_method}!")

                    # Display person details
                    st.markdown("#### 👤 Contact Details")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Personal Info:**")
                        st.markdown(f"• **Name:** {person_data.get('name', 'N/A')}")
                        st.markdown(f"• **Title:** {person_data.get('title', 'N/A')}")
                        st.markdown(f"• **Seniority:** {person_data.get('seniority', 'N/A').replace('_', ' ').title()}")
                        st.markdown(f"• **Email:** {person_data.get('email', 'N/A')}")
                        st.markdown(f"• **Phone:** {person_data.get('phone', 'N/A')}")

                    with col2:
                        st.markdown("**Location & Links:**")
                        st.markdown(f"• **City:** {person_data.get('city', 'N/A')}")
                        st.markdown(f"• **State:** {person_data.get('state', 'N/A')}")
                        st.markdown(f"• **Country:** {person_data.get('country', 'N/A')}")
                        linkedin_url = person_data.get('linkedin_url', 'N/A')
                        if linkedin_url != 'N/A':
                            st.markdown(f"• **LinkedIn:** [{linkedin_url}]({linkedin_url})")
                        else:
                            st.markdown(f"• **LinkedIn:** N/A")

                    # Display company details if available
                    if company_data:
                        st.markdown("#### 🏢 Company Details")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Company Info:**")
                            st.markdown(f"• **Name:** {company_data.get('name', 'N/A')}")
                            st.markdown(f"• **Industry:** {company_data.get('industry', 'N/A')}")
                            st.markdown(f"• **Size:** {company_data.get('estimated_num_employees', 'N/A')} employees")
                            website = company_data.get('website_url', 'N/A')
                            if website != 'N/A':
                                st.markdown(f"• **Website:** [{website}]({website})")
                            else:
                                st.markdown(f"• **Website:** N/A")

                        with col2:
                            st.markdown("**Additional Info:**")
                            st.markdown(f"• **Location:** {company_data.get('city', 'N/A')}, {company_data.get('state', 'N/A')}")
                            st.markdown(f"• **Revenue:** {company_data.get('estimated_annual_revenue', 'N/A')}")
                            linkedin_url = company_data.get('linkedin_url', 'N/A')
                            if linkedin_url != 'N/A':
                                st.markdown(f"• **LinkedIn:** [{linkedin_url}]({linkedin_url})")
                            else:
                                st.markdown(f"• **LinkedIn:** N/A")

                    # Add to Notion button
                    st.markdown("")  # Spacing
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        add_to_notion_button = st.button(
                            "➕ Add to Notion",
                            type="primary",
                            use_container_width=True,
                            key="add_single_to_notion"
                        )

                    if add_to_notion_button:
                        # Check if already exists
                        existing = st.session_state.notion.find_contact(
                            person_data['name'],
                            company_data.get('name', '') if company_data else ''
                        )

                        if existing:
                            st.warning(f"⚠️ Contact already exists in Notion: {person_data['name']}")
                        else:
                            # Add to Notion
                            success, action = st.session_state.notion.upsert_contact(
                                contact_name=person_data['name'],
                                company_name=company_data.get('name', '') if company_data else '',
                                enriched_data=person_data,
                                company_data=company_data
                            )

                            if success:
                                st.success(f"✅ Successfully {action}d **{person_data['name']}** to Notion!")
                            else:
                                st.error("❌ Failed to add contact to Notion")

                else:
                    st.error(f"❌ No contact found via {search_method}")
                    st.info("💡 Try a different LinkedIn URL or email address")

        # Divider before CSV section
        st.markdown("---")

        if uploaded_file is not None:
            try:
                # Read CSV
                df = pd.read_csv(uploaded_file)

                # Check for at least one valid search key per row
                has_linkedin = 'linkedin_url' in df.columns
                has_email = 'email' in df.columns
                has_name_company = 'person_name' in df.columns and 'company_name' in df.columns

                # Validate that at least ONE search method exists
                if not (has_linkedin or has_email or has_name_company):
                    st.error("❌ CSV must contain at least ONE of:")
                    st.error("   1. **linkedin_url** column (highest priority)")
                    st.error("   2. **email** column (second priority)")
                    st.error("   3. **person_name** + **company_name** columns (third priority)")
                    st.stop()

                # Analyze available columns
                available_methods = []
                if has_linkedin:
                    available_methods.append("LinkedIn")
                if has_email:
                    available_methods.append("Email")
                if has_name_company:
                    available_methods.append("Name+Company")

                st.success(f"✅ Detected search methods: **{', '.join(available_methods)}**")
                st.info("💡 System will try in priority order: LinkedIn → Email → Name+Company")

                # Show preview
                st.subheader("2️⃣ Preview Data")
                st.dataframe(df, use_container_width=True)

                st.success(f"✅ Loaded {len(df)} contacts")

                # Initialize clients
                if 'apollo' not in st.session_state:
                    with st.spinner("Initializing API clients..."):
                        st.session_state.apollo = ApolloClient(os.getenv('APOLLO_API_KEY'))
                        st.session_state.notion = NotionClient(
                            os.getenv('NOTION_TOKEN'),
                            os.getenv('NOTION_DB_ID')
                        )

                # Start enrichment
                st.subheader("3️⃣ Start Enrichment")

                col1, col2 = st.columns([1, 3])

                with col1:
                    start_button = st.button(
                        "🚀 Start Enrichment",
                        type="primary",
                        use_container_width=True
                    )

                if start_button or st.session_state.get('enrichment_running', False):
                    st.session_state.enrichment_running = True

                    # Results tracking
                    if 'results' not in st.session_state:
                        st.session_state.results = []
                        st.session_state.stats = {'success': 0, 'failed': 0, 'skipped': 0}
                        st.session_state.current_index = 0

                    # Progress containers
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # Stats display
                    col1, col2, col3, col4 = st.columns(4)
                    stat_success = col1.empty()
                    stat_failed = col2.empty()
                    stat_skipped = col3.empty()
                    stat_total = col4.empty()

                    # Live results
                    results_placeholder = st.empty()

                    # Process contacts
                    total = len(df)

                    for idx in range(st.session_state.current_index, total):
                        row = df.iloc[idx]

                        # Create identifier for status display
                        identifier = (
                            row.get('linkedin_url', '') or
                            row.get('email', '') or
                            row.get('person_name', 'Contact')
                        )

                        # Update status
                        status_text.info(f"Processing {idx + 1}/{total}: {identifier}")

                        # Enrich using flexible priority search
                        result = enrich_contact_flexible(
                            row,
                            st.session_state.apollo,
                            st.session_state.notion
                        )

                        # Store result
                        st.session_state.results.append(result)
                        st.session_state.stats[result['status']] += 1
                        st.session_state.current_index = idx + 1

                        # Update progress
                        progress = (idx + 1) / total
                        progress_bar.progress(progress)

                        # Update stats
                        stat_success.metric("✅ Success", st.session_state.stats['success'])
                        stat_failed.metric("❌ Failed", st.session_state.stats['failed'])
                        stat_skipped.metric("⏭️ Skipped", st.session_state.stats['skipped'])
                        stat_total.metric("📊 Total", idx + 1)

                        # Show recent results
                        recent_results = st.session_state.results[-5:]
                        results_df = pd.DataFrame([{
                            'Person': r['person'],
                            'Company': r['company'],
                            'Status': r['status'].upper(),
                            'Message': r['message']
                        } for r in recent_results])

                        results_placeholder.dataframe(
                            results_df,
                            use_container_width=True,
                            hide_index=True
                        )

                        # Rate limiting
                        if idx < total - 1:
                            time.sleep(delay)

                    # Completion
                    st.session_state.enrichment_running = False
                    status_text.success(f"✅ Enrichment complete! Processed {total} contacts")

                    # Final summary
                    st.balloons()

                    st.markdown("### 🎉 Enrichment Complete!")
                    st.markdown(f"""
                    - **Success**: {st.session_state.stats['success']} contacts added/updated
                    - **Skipped**: {st.session_state.stats['skipped']} already existed
                    - **Failed**: {st.session_state.stats['failed']} couldn't be enriched
                    """)

            except Exception as e:
                st.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
