"""Smoke tests for the extracted generator modules."""
import json
import os

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
from connector_generator.src import kb_generator


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


class TestKbSfcxGeneration:
    def test_generates_one_sfcx_per_connector(self, tmp_path, monkeypatch):
        call_root = tmp_path / "call"
        template_root = tmp_path / "template_call"
        projectname = "hat"
        project_call_dir = call_root / projectname
        project_call_dir.mkdir(parents=True)
        (template_root / "svcqualification").mkdir(parents=True)

        template_content = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<process:ProcessDefinition name="GetSvcQualification">\n'
            '  <elements xsi:type="process:ConnectorTask" name="SyncCustomerTVSubscriptionsList"/>\n'
            '  <connector connectorId="com.telus.connector.svcqualification.GetSvcQualification"/>\n'
            '  <parameterType signature="Lcom.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;"/>\n'
            '  <resultType signature="Lcom.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;"/>\n'
            '  <type signature="Lcom.telus.connector.svcqualification.api.datatypes.GetSvcQualificationDataRecord;"/>\n'
            '  <source>return GetSvcQualificationDataRecord.create()</source>\n'
            '  <notation:Diagram name="SyncCustomerTvSubscriptionsList"/>\n'
            '</process:ProcessDefinition>\n'
        )

        legacy_path = project_call_dir / "GetSvcQualification.sfcx"
        legacy_path.write_text(template_content, encoding="utf-8")

        monkeypatch.setattr(kb_generator, "CALLDIR", str(call_root))
        monkeypatch.setattr(kb_generator, "TEMPLATEKBCALLDIR", str(template_root))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        connectors = [
            {
                "connectorid": "GetSiteOutages",
                "inputClass": "GetSiteOutagesRequest",
                "dataRecordClass": "GetSiteOutagesDataRecord",
            },
            {
                "connectorid": "GetSmartphoneData",
                "inputClass": "GetSmartphoneDataRequest",
                "dataRecordClass": "GetSmartphoneDataDataRecord",
            },
        ]

        kb_generator.generate_kb_call_sfcx_per_connector(projectname, connectors)

        first = project_call_dir / "GetSiteOutages.sfcx"
        second = project_call_dir / "GetSmartphoneData.sfcx"
        assert first.exists()
        assert second.exists()
        assert not legacy_path.exists()

        first_content = first.read_text(encoding="utf-8")
        assert "connectorId=\"com.telus.connector.hat.GetSiteOutages\"" in first_content
        assert "GetSiteOutagesRequest" in first_content
        assert "GetSiteOutagesDataRecord" in first_content
        assert "svcqualification" not in first_content
        # Issues 1 & 2: stale display names must be replaced
        assert "SyncCustomerTVSubscriptionsList" not in first_content
        assert "SyncCustomerTvSubscriptionsList" not in first_content
        assert first_content.count('name="GetSiteOutages"') >= 2  # ProcessDefinition + ConnectorTask + Diagram


class TestKbQaGeneration:
    """Tests for generate_kb_qa_per_connector."""

    # ── shared fixtures ────────────────────────────────────────────────────

    @staticmethod
    def _make_env(tmp_path, projectname="inventory.tmf"):
        """
        Build a fake QADIR/projectname tree with legacy template copies,
        mimicking what copy_templates() leaves behind.
        """
        qa_root      = tmp_path / "qa"
        template_root = tmp_path / "template_qa"
        projectdir   = qa_root / projectname
        legacy_sub   = projectdir / "getsvcqualification"
        legacy_sub.mkdir(parents=True)
        (template_root / "svcqualification" / "getsvcqualification").mkdir(parents=True)

        sfcx_content = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<process:ProcessDefinition name="QAIssueGetSvcQualification" processType="ISSUE">\n'
            '  <elements xsi:type="process:ConnectorTask" name="StbDiagnosticsQuery"/>\n'
            '  <connector connectorId="com.telus.connector.svcqualification.GetSvcQualification"/>\n'
            '  <parameterType signature="Lcom.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;"/>\n'
            '  <resultType signature="Lcom.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;"/>\n'
            '  <type signature="Lqa.da.svcqualification.QAIssueGetSvcQualification;"/>\n'
            '  <form formId="qa.da.svcqualification.getsvcqualification.QAIssueGetSvcQualification"/>\n'
            '  <source>import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest\n'
            'return GetSvcQualificationRequest.create</source>\n'
            '  <notation:Diagram name="QAIssueSTBDiagnosticQuery"/>\n'
            '</process:ProcessDefinition>\n'
        )
        sfrm2_content = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<model:Form>\n'
            '  <parameters name="lpdsId"/>\n'
            '  <variants formId="qa.da.svcqualification.getsvcqualification.QAIssueGetSvcQualification"/>\n'
            '  <title value="Get Servcice Qualification"/>\n'
            '</model:Form>\n'
        )

        (legacy_sub / "QAIssueGetSvcQualification.sfcx").write_text(sfcx_content, encoding="utf-8")
        (legacy_sub / "QAIssueGetSvcQualification.sfrm2").write_text(sfrm2_content, encoding="utf-8")
        (projectdir / "QAIssuesSvcQualification.model").write_text("", encoding="utf-8")
        (projectdir / "QAIssuesSvcQualification_en_CA.content").write_text("", encoding="utf-8")
        (projectdir / "QAIssuesSvcQualification_fr_CA.content").write_text("", encoding="utf-8")

        return qa_root, projectdir

    @staticmethod
    def _connectors():
        return [
            {
                "connectorid": "GetSiteOutages",
                "inputClass": "GetSiteOutagesRequest",
                "dataRecordClass": "GetSiteOutagesDataRecord",
                "connectordescription": "Retrieve site outages",
            },
            {
                "connectorid": "GetSmartphoneData",
                "inputClass": "GetSmartphoneDataRequest",
                "dataRecordClass": "GetSmartphoneDataDataRecord",
                "connectordescription": "",
            },
        ]

    # ── file count & naming ─────────────────────────────────────────────────

    def test_generates_one_subfolder_per_connector(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors())

        assert (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfcx").exists()
        assert (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfrm2").exists()
        assert (projectdir / "getsmartphonedata" / "QAIssueGetSmartphoneData.sfcx").exists()
        assert (projectdir / "getsmartphonedata" / "QAIssueGetSmartphoneData.sfrm2").exists()

    # ── sfcx substitutions ──────────────────────────────────────────────────

    def test_sfcx_connector_id_substituted(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfcx").read_text()
        assert "QAIssueGetSiteOutages" in content
        assert "com.telus.connector.inventory.tmf.GetSiteOutages" in content
        assert "GetSiteOutagesRequest" in content

    def test_sfcx_no_svcqualification_placeholder(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfcx").read_text()
        assert "svcqualification" not in content

    def test_sfcx_qa_package_substituted(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfcx").read_text()
        assert "qa.da.inventory.tmf" in content
        assert "qa.da.svcqualification" not in content

    # ── sfrm2 substitutions ─────────────────────────────────────────────────

    def test_sfrm2_connector_id_substituted(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfrm2").read_text()
        assert "QAIssueGetSiteOutages" in content
        assert "qa.da.inventory.tmf" in content
        assert "svcqualification" not in content

    def test_sfrm2_retains_stub_input_field(self, tmp_path, monkeypatch):
        """lpdsId stub is preserved — developer updates form fields manually."""
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfrm2").read_text()
        assert "lpdsId" in content

    # ── project-level model file ────────────────────────────────────────────

    def test_model_file_created_with_correct_name(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors())

        assert (projectdir / "QAIssuesInventory.tmf.model").exists()

    def test_model_file_contains_all_connectors(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors())

        content = (projectdir / "QAIssuesInventory.tmf.model").read_text()
        assert "package qa.da.inventory.tmf" in content
        assert "issue QAIssueGetSiteOutages" in content
        assert "issue QAIssueGetSmartphoneData" in content
        assert "getsiteoutages.QAIssueGetSiteOutages" in content
        assert "getsmartphonedata.QAIssueGetSmartphoneData" in content

    # ── localisation content files ──────────────────────────────────────────

    def test_en_content_file_created(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors())

        content = (projectdir / "QAIssuesInventory.tmf_en_CA.content").read_text()
        assert "qa.da.inventory.tmf.QAIssueGetSiteOutages" in content
        assert 'title = "Retrieve site outages"' in content
        assert "qa.da.inventory.tmf.QAIssueGetSmartphoneData" in content

    def test_fr_content_file_has_blank_titles(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors())

        content = (projectdir / "QAIssuesInventory.tmf_fr_CA.content").read_text()
        assert 'title = ""' in content

    # ── legacy cleanup ──────────────────────────────────────────────────────

    def test_legacy_templates_removed(self, tmp_path, monkeypatch):
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors())

        assert not (projectdir / "QAIssuesSvcQualification.model").exists()
        assert not (projectdir / "QAIssuesSvcQualification_en_CA.content").exists()
        assert not (projectdir / "QAIssuesSvcQualification_fr_CA.content").exists()
        assert not (projectdir / "getsvcqualification").exists()

    # ── stale display-name fixes (issues 3, 4, 5) ──────────────────────────

    def test_sfcx_connector_task_name_replaced(self, tmp_path, monkeypatch):
        """Issue 3: ConnectorTask name='StbDiagnosticsQuery' → connectorid."""
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfcx").read_text()
        assert "StbDiagnosticsQuery" not in content
        assert 'name="GetSiteOutages"' in content

    def test_sfcx_diagram_name_replaced(self, tmp_path, monkeypatch):
        """Issue 4: notation:Diagram name='QAIssueSTBDiagnosticQuery' → QAIssue<connectorid>."""
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfcx").read_text()
        assert "QAIssueSTBDiagnosticQuery" not in content
        assert 'name="QAIssueGetSiteOutages"' in content

    def test_sfrm2_title_replaced(self, tmp_path, monkeypatch):
        """Issue 5: stale/misspelled form title replaced with connectorid."""
        qa_root, projectdir = self._make_env(tmp_path)
        monkeypatch.setattr(kb_generator, "QADIR", str(qa_root))
        monkeypatch.setattr(kb_generator, "TEMPLDATEKBQADIR", str(tmp_path / "template_qa"))
        monkeypatch.setattr(kb_generator, "TEMPLATE_NAME", "svcqualification")

        kb_generator.generate_kb_qa_per_connector("inventory.tmf", self._connectors()[:1])

        content = (projectdir / "getsiteoutages" / "QAIssueGetSiteOutages.sfrm2").read_text()
        assert "Get Servcice Qualification" not in content
        assert "GetSiteOutages" in content

