"""Shared fixtures.

Every test here runs offline: no model weights, no tesseract, no LibreOffice.
"""

from __future__ import annotations

import pytest

from kdp.config import Config


@pytest.fixture
def config(tmp_path) -> Config:
    """Library defaults, independent of configs/default.yaml.

    Output goes to a temporary directory: the default ``out/`` is relative to
    the working directory, so a test that builds a dataset would otherwise
    overwrite the one the pipeline just produced in the repository.
    """
    return Config.model_validate({"paths": {"out_dir": str(tmp_path / "out")}})
