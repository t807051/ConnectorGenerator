"""Tests for the connector_generator.main public surface."""
import json
import os

import pytest

from connector_generator.main import (
    main,
    generate_config_per_connector,
    generate_api_per_connector,
    generate_impl_per_connector,
)
from connector_generator.src.definition_loader import load_definition


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _write_definition(tmp_path, data: dict) -> str:
    path = os.path.join(str(tmp_path), "definition.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return path


MINIMAL_DEFINITION = {
    "projectname": "inventory.tmf",
    "connectors": [
        {
            "connectorid": "GetInventory",
            "inputClass": "GetInventoryRequest",
            "entityClass": "GetInventoryEntity",
            "dataRecordClass": "GetInventoryDataRecord",
            "apiPath": "/inventory/v1/items",
            "httpMethod": "GET",
        }
    ],
}


# ─────────────────────────────────────────────
# load_definition
# ─────────────────────────────────────────────

def test_load_definition_valid(tmp_path):
    path = _write_definition(tmp_path, MINIMAL_DEFINITION)
    data = load_definition(path)
    assert data["projectname"] == "inventory.tmf"
    assert len(data["connectors"]) == 1
    assert data["connectors"][0]["connectorid"] == "GetInventory"


def test_load_definition_missing_file():
    with pytest.raises(FileNotFoundError):
        load_definition("/nonexistent/path/definition.json")


def test_load_definition_empty_file(tmp_path):
    empty = str(tmp_path / "empty.json")
    open(empty, "w").close()
    with pytest.raises(ValueError, match="empty"):
        load_definition(empty)


def test_load_definition_invalid_json(tmp_path):
    bad = str(tmp_path / "bad.json")
    with open(bad, "w") as f:
        f.write("{ not valid json }")
    with pytest.raises(ValueError, match="invalid"):
        load_definition(bad)


def test_load_definition_missing_projectname(tmp_path):
    data = {k: v for k, v in MINIMAL_DEFINITION.items() if k != "projectname"}
    path = _write_definition(tmp_path, data)
    with pytest.raises(ValueError, match="projectname"):
        load_definition(path)


def test_load_definition_missing_connectors(tmp_path):
    path = _write_definition(tmp_path, {"projectname": "foo"})
    with pytest.raises(ValueError, match="connectors"):
        load_definition(path)


def test_load_definition_connector_missing_required_field(tmp_path):
    data = {
        "projectname": "foo",
        "connectors": [{"connectorid": "Bar"}],
    }
    path = _write_definition(tmp_path, data)
    with pytest.raises(ValueError):
        load_definition(path)


# ─────────────────────────────────────────────
# Public wrappers importable from connector_generator.main
# ─────────────────────────────────────────────

def test_public_wrappers_are_callable():
    assert callable(main)
    assert callable(generate_config_per_connector)
    assert callable(generate_api_per_connector)
    assert callable(generate_impl_per_connector)


# ─────────────────────────────────────────────
# main() CLI – exits with code 1 on bad input
# ─────────────────────────────────────────────

def test_main_no_args_exits(monkeypatch):
    import sys
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_main_bad_file_exits(monkeypatch, tmp_path):
    import sys
    monkeypatch.setattr(sys, "argv", ["main.py", str(tmp_path / "nope.json")])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
