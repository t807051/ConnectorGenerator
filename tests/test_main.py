"""Tests for the main module."""
import pytest

from connector_generator.main import generate_connector


def test_generate_connector_returns_dict():
    result = generate_connector("my-connector", "http")
    assert isinstance(result, dict)


def test_generate_connector_fields():
    result = generate_connector("my-connector", "http")
    assert result["name"] == "my-connector"
    assert result["type"] == "http"
    assert result["version"] == "1.0"


def test_generate_connector_empty_name_raises():
    with pytest.raises(ValueError, match="name"):
        generate_connector("", "http")


def test_generate_connector_empty_type_raises():
    with pytest.raises(ValueError, match="type"):
        generate_connector("my-connector", "")
