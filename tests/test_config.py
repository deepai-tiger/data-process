"""Configuration loading, CLI overrides and page-range parsing."""

from __future__ import annotations

import pytest

from kdp.config import DEFAULT_CONFIG_PATH, Config, load_config, parse_page_spec


def test_the_shipped_default_config_is_valid():
    config = load_config(DEFAULT_CONFIG_PATH)
    assert config.pdf.mode == "page_images"
    assert config.ocr.languages == ["kor", "eng"]


def test_load_config_returns_a_validated_model():
    assert isinstance(load_config(), Config)


def test_a_missing_explicit_config_file_is_an_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.yaml")


def test_a_custom_file_overrides_only_what_it_names(tmp_path):
    path = tmp_path / "mine.yaml"
    path.write_text("pdf:\n  dpi: 400\n", encoding="utf-8")
    config = load_config(path)
    assert config.pdf.dpi == 400
    assert config.pdf.mode == "page_images"  # untouched default


def test_dotted_overrides_are_expanded_into_the_tree():
    config = load_config(overrides={"pdf.dpi": 300, "chunk.max_tokens": 1024})
    assert config.pdf.dpi == 300
    assert config.chunk.max_tokens == 1024


def test_none_overrides_are_ignored_so_unset_cli_flags_do_nothing():
    config = load_config(overrides={"pdf.dpi": None})
    assert config.pdf.dpi == load_config().pdf.dpi


def test_overrides_are_merged_rather_than_replacing_a_section(tmp_path):
    path = tmp_path / "mine.yaml"
    path.write_text("pdf:\n  dpi: 400\n  do_tables: false\n", encoding="utf-8")
    config = load_config(path, overrides={"pdf.dpi": 150})
    assert config.pdf.dpi == 150
    assert config.pdf.do_tables is False


def test_an_unknown_enum_value_is_rejected():
    with pytest.raises(ValueError):
        load_config(overrides={"pdf.formula_engine": "magic"})


def test_output_paths_derive_from_out_dir():
    paths = load_config(overrides={"paths.out_dir": "/tmp/kdp"}).paths
    assert str(paths.docjson_dir) == "/tmp/kdp/interim/docjson"
    assert str(paths.dataset_dir) == "/tmp/kdp/dataset"
    assert str(paths.report_dir) == "/tmp/kdp/reports"


def test_config_dumps_to_json_safe_types():
    dumped = load_config().dump()
    assert isinstance(dumped["paths"]["raw_dir"], str)


@pytest.mark.parametrize(
    "spec,expected",
    [
        ("", [1, 2, 3, 4, 5]),
        ("2", [2]),
        ("1-3", [1, 2, 3]),
        ("1-3,5", [1, 2, 3, 5]),
        ("5,1-2", [1, 2, 5]),
        ("3-", [3, 4, 5]),
        ("-2", [1, 2]),
        ("1-99", [1, 2, 3, 4, 5]),
        ("2,2,2", [2]),
        ("0-2", [1, 2]),
    ],
)
def test_page_specs_are_parsed_and_clamped(spec, expected):
    assert parse_page_spec(spec, 5) == expected


def test_a_page_spec_beyond_the_document_yields_nothing():
    assert parse_page_spec("10-20", 5) == []
