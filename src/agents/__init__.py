"""
BantuMarket Agents Module
Contains all agent implementations
"""

from .ingestion_scout import IngestionScoutAgent
from .compliance_officer import ComplianceOfficerAgent
from .risk_sentinel import RiskSentinelAgent

__all__ = [
    "IngestionScoutAgent",
    "ComplianceOfficerAgent",
    "RiskSentinelAgent"
]

# Made with Bob
