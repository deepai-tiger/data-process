"""Logging setup: our own output survives, third-party noise does not."""

from __future__ import annotations

import logging

import pytest

from kdp.logging_utils import ThirdPartyRootNoiseFilter, setup_logging

PIX2TEX_CLI = "/venv/lib/python3.12/site-packages/pix2tex/cli.py"


def make_record(pathname: str, args: tuple = ()) -> logging.LogRecord:
    return logging.LogRecord("root", logging.INFO, pathname, 1, "0.666", args, None)


@pytest.fixture
def pristine_root():
    """Hand the root logger back untouched; setup_logging replaces handlers."""
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    yield root
    root.handlers[:] = handlers
    root.setLevel(level)


def test_a_record_from_pix2tex_is_dropped():
    record = make_record(PIX2TEX_CLI, ((64, 32), (64, 21)))
    assert not ThirdPartyRootNoiseFilter().filter(record)


def test_our_own_records_are_kept():
    assert ThirdPartyRootNoiseFilter().filter(make_record("/workspace/src/kdp/pipeline.py"))


def test_pix2tex_chatter_does_not_reach_the_console(pristine_root, capsys):
    setup_logging("INFO")
    # args that are not format arguments: formatting this record raises, and
    # the handler would print the traceback in its place
    pristine_root.handle(make_record(PIX2TEX_CLI, ((64, 32), (64, 21))))
    assert capsys.readouterr().err == ""


def test_pipeline_progress_still_reaches_the_console(pristine_root, capsys):
    setup_logging("INFO")
    logging.getLogger("kdp.pipeline").info("extracted %d pages", 7)
    assert "extracted 7 pages" in capsys.readouterr().err
