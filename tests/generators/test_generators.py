"""Smoke tests for the extracted generator modules."""
import json
import os

import pytest

from connector_generator.src.api_generator import (
    _json_to_idl_fields,
    _json_value_to_idl_type,
    _singularize,
    _is_date_string,
    _write_connectors_xml,
    _write_types_idl,
    json_to_idl_fields,
)
from connector_generator.src.config_generator import (
    _write_osgi_xml,
)
from connector_generator.src.impl_generator import (
    _json_to_pojo_fields,
    _json_to_conversion_logic,
    _write_java_stub,
)
from connector_generator.src.definition_loader import load_definition


# ─────────────────────────────────────────────
# api_generator helpers
# ─────────────────────────────────────────────

class TestJsonToIdlFields:
    def test_flat_string_fields(self):
        data = {"name": "Alice", "city": "Vancouver"}
        result = _json_to_idl_fields(data, indent=1)
        assert "\tstring name" in result
        assert "\tstring city" in result

    def test_int_becomes_long(self):
        result = _json_to_idl_fields({"count": 42}, indent=1)
        assert "\tlong count" in result

    def test_bool_field(self):
        result = _json_to_idl_fields({"active": True}, indent=1)
        assert "\tbool active" in result

    def test_float_field(self):
        result = _json_to_idl_fields({"price": 1.5}, indent=1)
        assert "\tdouble price" in result

    def test_date_string(self):
        result = _json_to_idl_fields({"created": "2024-01-15"}, indent=1)
        assert "\tdate created" in result

    def test_null_field_has_todo(self):
        result = _json_to_idl_fields({"val": None}, indent=1)
        assert "string val" in result
        assert "TODO" in result

    def test_empty_array_has_todo(self):
        result = _json_to_idl_fields({"items": []}, indent=1)
        assert "TODO" in result

    def test_nested_object_emits_struct(self):
        structs = []
        result = _json_to_idl_fields({"addr": {"street": "Main"}}, indent=1, top_level_structs=structs)
        assert "Addr addr" in result
        assert len(structs) == 1
        assert "struct Addr" in structs[0]

    def test_list_of_objects_emits_struct(self):
        structs = []
        data = {"items": [{"id": 1, "name": "x"}]}
        result = _json_to_idl_fields(data, indent=1, top_level_structs=structs)
        assert "[]" in result
        assert len(structs) == 1

    def test_list_input_unwraps_first_element(self):
        result = _json_to_idl_fields([{"x": "y"}], indent=1)
        assert "string x" in result

    def test_exported_alias_is_same_function(self):
        assert json_to_idl_fields is _json_to_idl_fields


class TestJsonValueToIdlType:
    def test_bool(self):      assert _json_value_to_idl_type(True) == ("bool", "")
    def test_int(self):       assert _json_value_to_idl_type(42) == ("long", "")
    def test_float(self):     assert _json_value_to_idl_type(3.14) == ("double", "")
    def test_string(self):    assert _json_value_to_idl_type("hello") == ("string", "")
    def test_date_str(self):  assert _json_value_to_idl_type("2024-01-01") == ("date", "")
    def test_none(self):      assert _json_value_to_idl_type(None)[0] == "string"
    def test_empty_list(self):
        idl_type, comment = _json_value_to_idl_type([])
        assert "TODO" in comment
    def test_int_list(self):  assert _json_value_to_idl_type([1, 2]) == ("long[]", "")


class TestSingularize:
    def test_regular_s(self):     assert _singularize("items") == "item"
    def test_ies_suffix(self):    assert _singularize("categories") == "category"
    def test_no_change(self):     assert _singularize("data") == "data"
    def test_ss_unchanged(self):  assert _singularize("address") == "address"


class TestIsDateString:
    def test_iso_date(self):      assert _is_date_string("2024-01-15")
    def test_iso_datetime(self):  assert _is_date_string("2024-01-15T10:30:00")
    def test_slash_date(self):    assert _is_date_string("01/15/2024")
    def test_plain_string(self):  assert not _is_date_string("hello")
    def test_partial(self):       assert not _is_date_string("2024-01")


class TestWriteConnectorsXml:
    def test_generates_valid_xml(self, tmp_path):
        connectors = [
            {
                "connectorid": "GetOrder",
                "inputClass": "GetOrderRequest",
                "dataRecordClass": "GetOrderDataRecord",
            }
        ]
        out = str(tmp_path / "connectors.xml")
        _write_connectors_xml(out, "order.tmf", connectors)
        assert os.path.exists(out)
        content = open(out).read()
        assert "GetOrder" in content
        assert "GetOrderRequest" in content
        assert 'version="1.0.0"' in content


class TestWriteTypesIdl:
    def test_generates_idl_file(self, tmp_path):
        out = str(tmp_path / "GetOrderTypes.model")
        _write_types_idl(out, "order.tmf", "GetOrder", "\tstring id", "\tstring status")
        content = open(out).read()
        assert "struct GetOrderRequest" in content
        assert "struct GetOrderEntity" in content
        assert "struct GetOrderDataRecord" in content
        assert "string id" in content


# ─────────────────────────────────────────────
# config_generator helpers
# ─────────────────────────────────────────────

class TestWriteOsgiXml:
    def test_generates_xml(self, tmp_path):
        out = str(tmp_path / "component.xml")
        _write_osgi_xml(out, "order.tmf", "GetOrder")
        content = open(out).read()
        assert "GetOrder" in content
        assert "scr:component" in content
        assert "com.telus.connector.order.tmf.GetOrder" in content


# ─────────────────────────────────────────────
# impl_generator helpers
# ─────────────────────────────────────────────

class TestJsonToPojoFields:
    def test_string_field(self, tmp_path):
        result = _json_to_pojo_fields({"name": "Alice"}, "order.tmf", str(tmp_path), [])
        assert "private String name;" in result
        assert "getName()" in result
        assert "setName(" in result

    def test_int_field(self, tmp_path):
        result = _json_to_pojo_fields({"count": 5}, "order.tmf", str(tmp_path), [])
        assert "private long count;" in result

    def test_bool_field(self, tmp_path):
        result = _json_to_pojo_fields({"active": True}, "order.tmf", str(tmp_path), [])
        assert "private boolean active;" in result

    def test_null_field_has_todo(self, tmp_path):
        result = _json_to_pojo_fields({"val": None}, "order.tmf", str(tmp_path), [])
        assert "TODO" in result


class TestJsonToConversionLogic:
    def test_returns_empty_for_missing_file(self):
        body, helpers, types = _json_to_conversion_logic("/nonexistent/file.json")
        assert body == ""
        assert helpers == ""
        assert types == []

    def test_flat_json(self, tmp_path):
        path = str(tmp_path / "resp.json")
        with open(path, "w") as f:
            json.dump({"orderId": "123", "status": "active"}, f)
        body, helpers, types = _json_to_conversion_logic(path)
        assert "setOrderId" in body
        assert "setStatus" in body

    def test_nested_object_emits_helper(self, tmp_path):
        path = str(tmp_path / "resp.json")
        with open(path, "w") as f:
            json.dump({"address": {"street": "Main St"}}, f)
        body, helpers, types = _json_to_conversion_logic(path)
        assert "convertToAddress" in body
        assert "Address" in types


class TestWriteJavaStub:
    def test_connector_stub(self, tmp_path):
        out = str(tmp_path / "FooConnector.java")
        _write_java_stub(out, "order.tmf", "Foo", "call")
        content = open(out).read()
        assert "class FooConnector" in content
        assert "package com.telus.connector.order.tmf.call" in content

    def test_converter_stub(self, tmp_path):
        out = str(tmp_path / "FooConverter.java")
        _write_java_stub(out, "order.tmf", "Foo", "converter")
        content = open(out).read()
        assert "class FooConverter" in content

