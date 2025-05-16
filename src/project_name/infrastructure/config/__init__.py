# src/project_name/infrastructure/config/__init__.py
"""Configuration infrastructure package."""

from project_name.infrastructure.config.settings import APISettings, settings

__all__ = ["settings", "APISettings"]
