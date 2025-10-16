"""
HLTH 2025 CRM - Source Package
Core enrichment and sync functionality
"""

from .apollo_client import ApolloClient
from .notion_sync import NotionClient
from .processors import TierAssigner, PriorityScorer

__all__ = [
    'ApolloClient',
    'NotionClient',
    'TierAssigner',
    'PriorityScorer'
]

__version__ = '1.0.0'
