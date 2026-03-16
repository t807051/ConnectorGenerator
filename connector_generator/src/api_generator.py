import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

try:
    from .settings import CONNECTORDIR
    from .file_ops import projectname_to_path
except ImportError:
    from settings import CONNECTORDIR
    from file_ops import projectname_to_path


def generate_api_per_connector(projectname: str, connectors: list, definition_file: str):
    """Generate connectors.xml and <connectorid>Types.model IDL for each connector."""
    api_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.api")
    osgi_inf_dir = os.path.join(api_dir, "OSGI-INF", "solvatio")
    connectors_xml = os.path.join(osgi_inf_dir, "connectors.xml")

    os.makedirs(osgi_inf_dir, exist_ok=True)
    _write_connectors_xml(connectors_xml, projectname, connectors)

    datatypes_dir = os.path.join(
        api_dir,
        "src",
        "com",
        "telus",
        "connector",
        projectname_to_path(projectname),
        "api",
        "datatypes",
    )
    os.makedirs(datatypes_dir, exist_ok=True)

    definition_dir = os.path.dirname(os.path.abspath(definition_file))

    for connector in connectors:
        cid = connector["connectorid"]
        request_example_fname = connector.get("requestExample")
        response_example_fname = connector.get("responseExample")

        request_fields = ""
        request_structs = []
        if request_example_fname:
            req_path = os.path.join(definition_dir, request_example_fname)
            if os.path.exists(req_path) and os.path.getsize(req_path) > 0:
                try:
                    with open(req_path, "r", encoding="utf-8-sig") as f:
                        req_data = json.load(f)
                    request_fields = _json_to_idl_fields(
                        req_data, indent=1, top_level_structs=request_structs
                    )
                    print(
                        f"  [Types] Converted requestExample '{request_example_fname}' -> IDL fields"
                    )
                except (json.JSONDecodeError, OSError) as e:
                    print(
                        f"  [WARN] Could not read/parse requestExample '{request_example_fname}': {e}"
                    )
            else:
                print(f"  [WARN] requestExample file not found or empty: {req_path}")

        entity_fields = ""
        entity_structs = []
        if response_example_fname:
            resp_path = os.path.join(definition_dir, response_example_fname)
            if os.path.exists(resp_path) and os.path.getsize(resp_path) > 0:
                try:
                    with open(resp_path, "r", encoding="utf-8-sig") as f:
                        resp_data = json.load(f)
                    entity_fields = _json_to_idl_fields(
                        resp_data, indent=1, top_level_structs=entity_structs
                    )
                    print(
                        f"  [Types] Converted responseExample '{response_example_fname}' -> IDL fields"
                    )
                except (json.JSONDecodeError, OSError) as e:
                    print(
                        f"  [WARN] Could not read/parse responseExample '{response_example_fname}': {e}"
                    )
            else:
                print(f"  [WARN] responseExample file not found or empty: {resp_path}")

        types_path = os.path.join(datatypes_dir, f"{cid}Types.model")
        _write_types_idl(
            types_path,
            projectname,
            cid,
            request_fields,
            entity_fields,
            request_structs,
            entity_structs,
        )


def _write_connectors_xml(connectors_xml: str, projectname: str, connectors: list):
    """Build OSGI-INF/solvatio/connectors.xml programmatically."""
    root = ET.Element("connectors")
    for connector in connectors:
        cid = connector["connectorid"]
        input_class = connector["inputClass"]
        data_rec_class = connector["dataRecordClass"]

        conn_el = ET.SubElement(root, "connector")
        conn_el.set("version", "1.0.0")
        conn_el.set("name", cid)
        conn_el.set("description", "")
        conn_el.set("id", f"com.telus.connector.{projectname}.{cid}")

        input_el = ET.SubElement(conn_el, "input")
        input_el.set("name", "parameters")
        input_el.set("class", f"com.telus.connector.{projectname}.api.datatypes.{input_class}")

        output_el = ET.SubElement(conn_el, "output")
        output_el.set("class", f"com.telus.connector.{projectname}.api.datatypes.{data_rec_class}")

    raw_xml = ET.tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="\t")
    lines = [line for line in pretty_xml.splitlines() if line.strip()]
    lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    final_xml = "\n".join(lines)

    with open(connectors_xml, "w", encoding="utf-8") as f:
        f.write(final_xml)
    print(f"Generated: {connectors_xml}")
    for connector in connectors:
        print(f"  + connector: {connector['connectorid']}")


def _write_types_idl(
    path: str,
    projectname: str,
    connectorid: str,
    request_fields: str,
    entity_fields: str,
    request_structs: list = None,
    entity_structs: list = None,
):
    """Generate the <connectorid>Types.model IDL file."""
    req_body = f"\n{request_fields}\n" if request_fields else ""
    entity_body = f"\n{entity_fields}\n" if entity_fields else ""

    extra_structs = []
    for s in request_structs or []:
        if s not in extra_structs:
            extra_structs.append(s)
    for s in entity_structs or []:
        if s not in extra_structs:
            extra_structs.append(s)

    extra_block = ("\n\n" + "\n\n".join(extra_structs)) if extra_structs else ""

    content = (
        f"package com.telus.connector.{projectname}.api.datatypes\n"
        f"\n"
        f"import com.telus.common.api.datatypes.AbstractDataRecord\n"
        f"\n"
        f"struct {connectorid}Request {{{req_body}}}\n"
        f"\n"
        f"struct {connectorid}Entity {{{entity_body}}}"
        f"{extra_block}\n"
        f"\n"
        f"struct {connectorid}DataRecord : AbstractDataRecord {{\n"
        f"\t{connectorid}Entity entityy\n"
        f"}}\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Types IDL: {path}")


def _json_to_idl_fields(data, indent: int = 1, top_level_structs: list = None) -> str:
    """Recursively convert a parsed JSON object into IDL field declarations."""
    if top_level_structs is None:
        top_level_structs = []
    tab = "\t" * indent
    lines = []

    if isinstance(data, list):
        if not data:
            return ""
        data = data[0] if isinstance(data[0], dict) else {}
    if not isinstance(data, dict):
        return ""

    for key, value in data.items():
        if isinstance(value, dict):
            struct_name = key.capitalize()
            nested_fields = _json_to_idl_fields(value, 1, top_level_structs)
            struct_block = f"struct {struct_name} {{\n{nested_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{struct_name} {key}")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            singular_name = _singularize(key).capitalize()
            elem_fields = _infer_fields_from_list(value, 1, top_level_structs)
            struct_block = f"struct {singular_name} {{\n{elem_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{singular_name}[] {key}")
        else:
            idl_type, comment = _json_value_to_idl_type(value)
            field_line = f"{tab}{idl_type} {key}"
            if comment:
                field_line = f"{field_line}  {comment}"
            lines.append(field_line)

    return "\n".join(lines)


def _json_value_to_idl_type(value) -> tuple:
    """Map a single JSON value to (idl_type, comment)."""
    if isinstance(value, bool):
        return ("bool", "")
    if isinstance(value, int):
        return ("long", "")
    if isinstance(value, float):
        return ("double", "")
    if isinstance(value, str):
        return ("date", "") if _is_date_string(value) else ("string", "")
    if value is None:
        return ("string", "// TODO: verify data type - null in sample")
    if isinstance(value, list):
        if not value:
            return ("string[]", "// TODO: verify data type - empty array in sample")
        first = value[0]
        if isinstance(first, bool):
            return ("bool[]", "")
        if isinstance(first, int):
            return ("long[]", "")
        if isinstance(first, float):
            return ("double[]", "")
        if isinstance(first, str):
            return ("date[]", "") if _is_date_string(first) else ("string[]", "")
        return ("string[]", "// TODO: verify data type - empty array in sample")
    return ("string", "")


def _infer_fields_from_list(items: list, indent: int, top_level_structs: list) -> str:
    """Infer IDL fields from a list of JSON objects by scanning all elements."""
    tab = "\t" * indent
    lines = []
    if not items or not isinstance(items[0], dict):
        return ""
    keys = list(items[0].keys())
    for key in keys:
        best_value = _first_non_null_value(items, key)
        if best_value is None:
            lines.append(
                f"{tab}string {key}  // TODO: verify data type - all values null in sample"
            )
        elif isinstance(best_value, dict):
            struct_name = key.capitalize()
            nested_fields = _json_to_idl_fields(best_value, 1, top_level_structs)
            struct_block = f"struct {struct_name} {{\n{nested_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{struct_name} {key}")
        elif isinstance(best_value, list) and best_value and isinstance(best_value[0], dict):
            singular_name = _singularize(key).capitalize()
            elem_fields = _infer_fields_from_list(best_value, 1, top_level_structs)
            struct_block = f"struct {singular_name} {{\n{elem_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{singular_name}[] {key}")
        else:
            idl_type, comment = _json_value_to_idl_type(best_value)
            field_line = f"{tab}{idl_type} {key}"
            if comment:
                field_line = f"{field_line}  {comment}"
            lines.append(field_line)
    return "\n".join(lines)


def _first_non_null_value(items: list, key: str):
    """Return the first non-null value for key across a list of dicts."""
    for item in items:
        if isinstance(item, dict):
            val = item.get(key)
            if val is not None:
                return val
    return None


def _singularize(name: str) -> str:
    """Simple singularization for IDL/POJO struct naming."""
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith(("sses", "xes", "ches", "shes")):
        return name[:-2]
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _is_date_string(value: str) -> bool:
    """Return True if the string looks like a date or datetime."""
    patterns = [
        r"^\d{4}-\d{2}-\d{2}$",
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}",
        r"^\d{2}/\d{2}/\d{4}$",
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}",
    ]
    for pattern in patterns:
        if re.match(pattern, value, re.IGNORECASE):
            return True
    return False


# Exported for spec_generator wiring in main.py.
json_to_idl_fields = _json_to_idl_fields

