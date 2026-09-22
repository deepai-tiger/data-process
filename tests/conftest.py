"""Shared fixtures.

Every test here runs offline: no model weights, no tesseract, no LibreOffice.
"""

from __future__ import annotations

import pytest

from kdp.config import Config


@pytest.fixture
def config() -> Config:
    """Library defaults, independent of configs/default.yaml."""
    return Config()
