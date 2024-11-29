"""
ems_audit/settings.py

This module is used to write settings contents related to payroll app
"""

from ems.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "ems_audit.context_processors.history_form",
)
