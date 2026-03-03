import os
import json
import shutil

# ─────────────────────────────────────────────
# 1. CONSTANTS
# ─────────────────────────────────────────────

#BASEDIR             = r"C:\github\Insight10.8\Insight"
BASEDIR             = r"C:\TEMP"
CONNECTORDIR        = os.path.join(BASEDIR, "connectors")
BUILDDIR            = os.path.join(BASEDIR, "build")
KBDIR               = os.path.join(BASEDIR, r"knowledgebases\com.telus.falcon.knowledgebase")
MODELDIR            = os.path.join(KBDIR, "model")
CALLDIR             = os.path.join(MODELDIR, r"da\call")
QADIR               = os.path.join(MODELDIR, r"qa\da")

#TEMPLATEDIR             = r"C:\cb\Insight10.8\Template"
TEMPLATEDIR             = r"C:\github\t807051\ConnectorGenerator\Template"
TEMPLATECONNECTORDIR    = os.path.join(TEMPLATEDIR, "connectors")
TEMPLATEBUILDDIR        = os.path.join(TEMPLATEDIR, "build")
TEMPLATEKBCALLDIR       = os.path.join(TEMPLATEDIR, r"knowledgebases\com.telus.falcon.knowledgebase\models\da\call")
TEMPLDATEKBQADIR        = os.path.join(TEMPLATEDIR, r"knowledgebases\com.telus.falcon.knowledgebase\models\qa\da")

TEMPLATE_NAME = "svcqualification"   # Template placeholder name

TEMPLATE_CONNECTOR_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME,
    "src", "com", "telus", "connector", TEMPLATE_NAME, "call", "TemplateConnector.java.txt"
)
TEMPLATE_FACTORY_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME,
    "src", "com", "telus", "connector", TEMPLATE_NAME, "factories", "TemplateFactory.java.txt"
)
TEMPLATE_EXCEPTION_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME,
    "src", "com", "telus", "connector", TEMPLATE_NAME, "exception", "TemplateException.java.txt"
)
TEMPLATE_CONVERTER_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME,
    "src", "com", "telus", "connector", TEMPLATE_NAME, "converter", "TemplateConverter.java.txt"
)


# ─────────────────────────────────────────────
# 2. LOAD CONNECTOR DEFINITION
# ─────────────────────────────────────────────

def load_definition(json_file: str) -> dict:
    """Read and parse the connector definition JSON file."""

    if not os.path.exists(json_file):
        raise FileNotFoundError(f"JSON definition file not found: {json_file}")

    if os.path.getsize(json_file) == 0:
        raise ValueError(f"JSON definition file is empty: {json_file}")

    try:
        with open(json_file, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file '{json_file}': {e}")

    if "projectname" not in data:
        raise ValueError("Missing required field: 'projectname'")
    if "connectors" not in data or not isinstance(data["connectors"], list):
        raise ValueError("Missing or invalid field: 'connectors' (must be a list)")
    if len(data["connectors"]) == 0:
        raise ValueError("'connectors' list must contain at least one connector")

    required_connector_fields = ["connectorid", "inputClass", "entityClass",
                                 "dataRecordClass", "apiPath", "httpMethod"]
    for i, connector in enumerate(data["connectors"]):
        for field in required_connector_fields:
            if field not in connector:
                raise ValueError(f"Connector [{i}] is missing required field: '{field}'")

    print(f"Successfully loaded definition: {json_file}")
    print(f"  Project : {data['projectname']}")
    print(f"  Connectors ({len(data['connectors'])}):")
    for c in data["connectors"]:
        print(f"    - {c['connectorid']} [{c['httpMethod']}] {c['apiPath']}")

    return data


# ─────────────────────────────────────────────
# 3. COPY TEMPLATES
# ─────────────────────────────────────────────

def copy_templates(projectname: str):
    """Copy all template directories to their target locations."""
    copies = [
        # Connector dirs
        (f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}",
         f"{CONNECTORDIR}\\com.telus.connector.{projectname}"),
        (f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}.api",
         f"{CONNECTORDIR}\\com.telus.connector.{projectname}.api"),
        (f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}.config",
         f"{CONNECTORDIR}\\com.telus.connector.{projectname}.config"),
        # Build dirs
        (f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.api.esa",
         f"{BUILDDIR}\\com.telus.connector.{projectname}.api.esa"),
        (f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.build",
         f"{BUILDDIR}\\com.telus.connector.{projectname}.build"),
        (f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.config.esa",
         f"{BUILDDIR}\\com.telus.connector.{projectname}.config.esa"),
        (f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.esa",
         f"{BUILDDIR}\\com.telus.connector.{projectname}.esa"),
        (f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.feature",
         f"{BUILDDIR}\\com.telus.connector.{projectname}.feature"),
        (f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.p2",
         f"{BUILDDIR}\\com.telus.connector.{projectname}.p2"),
        # KB dirs
        (f"{TEMPLATEKBCALLDIR}\\{TEMPLATE_NAME}", f"{CALLDIR}\\{projectname}"),
        (f"{TEMPLDATEKBQADIR}\\{TEMPLATE_NAME}",  f"{QADIR}\\{projectname}"),
    ]
    for src, dst in copies:
        shutil.copytree(src, dst)
        print(f"Copied: {src} -> {dst}")


# ─────────────────────────────────────────────
# 4. EDIT CONFIG FILES
# ─────────────────────────────────────────────

def edit_config_files(projectname: str):
    """Edit .project and pom.xml in the config project directory."""
    config_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    _replace_in_file(os.path.join(config_dir, ".project"), "svcQualification", projectname)
    _replace_in_file(os.path.join(config_dir, "pom.xml"),  "svcQualification", projectname)


# ─────────────────────────────────────────────
# 5. EDIT API FILES
# ─────────────────────────────────────────────

def edit_api_files(projectname: str):
    """Edit .project, pom.xml, MANIFEST.MF and rename src package in the API project."""
    api_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.api")

    _replace_in_file(os.path.join(api_dir, ".project"),              "svcqualification", projectname)
    _replace_in_file(os.path.join(api_dir, "pom.xml"),               "svcqualification", projectname)
    _replace_in_file(os.path.join(api_dir, r"META-INF\MANIFEST.MF"), "svcqualification", projectname)

    old_pkg = os.path.join(api_dir, "src", "com", "telus", "connector", TEMPLATE_NAME, "api")
    new_pkg = os.path.join(api_dir, "src", "com", "telus", "connector",
                           _projectname_to_path(projectname), "api")

    if os.path.exists(old_pkg):
        os.makedirs(os.path.dirname(new_pkg), exist_ok=True)
        os.rename(old_pkg, new_pkg)
        print(f"Renamed package folder: {old_pkg} -> {new_pkg}")
    else:
        print(f"[WARN] Package folder not found, skipping rename: {old_pkg}")


# ─────────────────────────────────────────────
# 6. EDIT IMPLEMENTATION FILES
# ─────────────────────────────────────────────

def edit_impl_files(projectname: str):
    """Edit .project, pom.xml, and MANIFEST.MF in the implementation project."""
    impl_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}")

    _replace_in_file(os.path.join(impl_dir, ".project"),              "svcqualification", projectname)
    _replace_in_file(os.path.join(impl_dir, "pom.xml"),               "svcqualification", projectname)
    _replace_in_file(os.path.join(impl_dir, r"META-INF\MANIFEST.MF"), "svcqualification", projectname)

    old_pkg = os.path.join(impl_dir, "src", "com", "telus", "connector", TEMPLATE_NAME)
    new_pkg = os.path.join(impl_dir, "src", "com", "telus", "connector",
                           _projectname_to_path(projectname))

    if os.path.exists(old_pkg):
        os.makedirs(os.path.dirname(new_pkg), exist_ok=True)
        os.rename(old_pkg, new_pkg)
        print(f"Renamed package folder: {old_pkg} -> {new_pkg}")
    else:
        print(f"[WARN] Package folder not found, skipping rename: {old_pkg}")


# ─────────────────────────────────────────────
# 7. GENERATE CONFIG FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_config_per_connector(projectname: str, connectors: list):
    """Generate OSGI-INF xml, ConfigComponent java stubs, and update MANIFEST.MF."""
    config_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    osgi_dir   = os.path.join(config_dir, "OSGI-INF")
    src_dir    = os.path.join(config_dir, "src", "com", "telus", "connector",
                              _projectname_to_path(projectname))
    os.makedirs(osgi_dir, exist_ok=True)
    os.makedirs(src_dir,  exist_ok=True)

    osgi_files = []
    for connector in connectors:
        cid = connector["connectorid"]

        osgi_file = os.path.join(osgi_dir, f"com.telus.connector.{projectname}.{cid}.xml")
        _write_osgi_xml(osgi_file, projectname, cid)
        osgi_files.append(osgi_file)

        iface_file = os.path.join(src_dir, f"I{cid}ConfigurationComponent.java")
        _write_interface_config(iface_file, projectname, cid)

        impl_file = os.path.join(src_dir, f"{cid}ConfigurationComponent.java")
        _write_impl_config(impl_file, projectname, cid)

    manifest_path = os.path.join(config_dir, r"META-INF\MANIFEST.MF")
    _append_service_components(manifest_path, osgi_files)


# ─────────────────────────────────────────────
# 8. GENERATE API FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_api_per_connector(projectname: str, connectors: list, definition_file: str):
    """
    For each connector:
      1. Generates OSGI-INF/solvatio/connectors.xml in the API project.
      2. Generates the connectorid Types.model IDL file in the datatypes package.
    """
    api_dir        = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.api")
    osgi_inf_dir   = os.path.join(api_dir, "OSGI-INF", "solvatio")
    connectors_xml = os.path.join(osgi_inf_dir, "connectors.xml")

    os.makedirs(osgi_inf_dir, exist_ok=True)
    _write_connectors_xml(connectors_xml, projectname, connectors)

    # Flat folder name with dots retained, directly under src\
    datatypes_dir = os.path.join(
        api_dir, "src", "com", "telus", "connector",
        _projectname_to_path(projectname), "api", "datatypes"
    )
    os.makedirs(datatypes_dir, exist_ok=True)

    # Directory where the definition JSON lives — example files are co-located there
    definition_dir = os.path.dirname(os.path.abspath(definition_file))

    for connector in connectors:
        cid                    = connector["connectorid"]
        request_example_fname  = connector.get("requestExample")
        response_example_fname = connector.get("responseExample")

        # --- Read & convert requestExample -> IDL fields for <connectorid>Request ---
        request_fields = ""
        if request_example_fname:
            req_path = os.path.join(definition_dir, request_example_fname)
            if os.path.exists(req_path) and os.path.getsize(req_path) > 0:
                try:
                    with open(req_path, "r", encoding="utf-8-sig") as f:
                        req_data = json.load(f)
                    request_fields = _json_to_idl_fields(req_data, indent=1)
                    print(f"  [Types] Converted requestExample '{request_example_fname}' -> IDL fields")
                except (json.JSONDecodeError, OSError) as e:
                    print(f"  [WARN] Could not read/parse requestExample '{request_example_fname}': {e}")
            else:
                print(f"  [WARN] requestExample file not found or empty: {req_path}")

        # --- Read & convert responseExample -> IDL fields for <connectorid>Entity ---
        entity_fields = ""
        if response_example_fname:
            resp_path = os.path.join(definition_dir, response_example_fname)
            if os.path.exists(resp_path) and os.path.getsize(resp_path) > 0:
                try:
                    with open(resp_path, "r", encoding="utf-8-sig") as f:
                        resp_data = json.load(f)
                    entity_fields = _json_to_idl_fields(resp_data, indent=1)
                    print(f"  [Types] Converted responseExample '{response_example_fname}' -> IDL fields")
                except (json.JSONDecodeError, OSError) as e:
                    print(f"  [WARN] Could not read/parse responseExample '{response_example_fname}': {e}")
            else:
                print(f"  [WARN] responseExample file not found or empty: {resp_path}")

        # Write the Types IDL file
        types_path = os.path.join(datatypes_dir, f"{cid}Types.model")
        _write_types_idl(types_path, projectname, cid, request_fields, entity_fields)


# ─────────────────────────────────────────────
# 9. GENERATE IMPLEMENTATION FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_impl_per_connector(projectname: str, connectors: list, definition_file: str):
    """
    For each connector, create:
      - call/<connectorid>Connector.java          from TemplateConnector.java.txt
      - model/<requestStem>Pojo.java              if requestExample is provided
      - model/<responseStem>Pojo.java             if responseExample is provided
      - converter/<connectorid>Converter.java     from TemplateConverter.java.txt
                                                  if responseExample is provided,
                                                  otherwise a generic stub
      - factories/<connectorid>Factory.java       from TemplateFactory.java.txt
      - exception/<connectorid>ConversionException.java from TemplateException.java.txt
    """
    impl_dir       = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}")
    src_base       = os.path.join(impl_dir, "src", "com", "telus", "connector",
                                  _projectname_to_path(projectname))
    definition_dir = os.path.dirname(os.path.abspath(definition_file))

    for connector in connectors:
        cid                    = connector["connectorid"]
        http_method            = connector["httpMethod"]
        api_path               = connector["apiPath"]
        request_example_fname  = connector.get("requestExample")
        response_example_fname = connector.get("responseExample")

        # Derive stem names (filename without extension) for POJO class names
        # e.g. "myRequest.json" -> "myRequest"
        request_stem  = os.path.splitext(request_example_fname)[0]  if request_example_fname  else None
        response_stem = os.path.splitext(response_example_fname)[0] if response_example_fname else None

        # --- call: generated from TemplateConnector.java.txt ---
        call_dir = os.path.join(src_base, "call")
        os.makedirs(call_dir, exist_ok=True)
        _write_connector_java(
            path        = os.path.join(call_dir, f"{cid}Connector.java"),
            projectname = projectname,
            connectorid = cid,
            http_method = http_method
        )

        # --- model: generate POJO(s) from example JSON files ---
        model_dir = os.path.join(src_base, "model")
        os.makedirs(model_dir, exist_ok=True)

        if request_example_fname:
            req_path = os.path.join(definition_dir, request_example_fname)
            _write_pojo_java(
                path        = os.path.join(model_dir, f"{request_stem}Pojo.java"),
                projectname = projectname,
                class_name  = f"{request_stem}Pojo",
                json_path   = req_path,
                label       = "requestExample"
            )

        if response_example_fname:
            resp_path = os.path.join(definition_dir, response_example_fname)
            _write_pojo_java(
                path        = os.path.join(model_dir, f"{response_stem}Pojo.java"),
                projectname = projectname,
                class_name  = f"{response_stem}Pojo",
                json_path   = resp_path,
                label       = "responseExample"
            )

        # --- converter ---
        converter_dir = os.path.join(src_base, "converter")
        os.makedirs(converter_dir, exist_ok=True)

        if response_example_fname:
            resp_path         = os.path.join(definition_dir, response_example_fname)
            req_path_for_conv = (os.path.join(definition_dir, request_example_fname)
                                 if request_example_fname else None)
            _write_converter_java(
                path                  = os.path.join(converter_dir, f"{cid}Converter.java"),
                projectname           = projectname,
                connectorid           = cid,
                request_example_stem  = request_stem,
                response_example_stem = response_stem,
                resp_json_path        = resp_path,
                req_json_path         = req_path_for_conv
            )
        else:
            # Fall back to generic stub if no responseExample
            _write_java_stub(
                os.path.join(converter_dir, f"{cid}Converter.java"),
                projectname, cid, "converter"
            )

        # --- factories: generated from TemplateFactory.java.txt ---
        factories_dir = os.path.join(src_base, "factories")
        os.makedirs(factories_dir, exist_ok=True)
        _write_factory_java(
            path        = os.path.join(factories_dir, f"{cid}Factory.java"),
            projectname = projectname,
            connectorid = cid,
            api_path    = api_path
        )

        # --- exception: generated from TemplateException.java.txt ---
        exception_dir = os.path.join(src_base, "exception")
        os.makedirs(exception_dir, exist_ok=True)
        _write_exception_java(
            path        = os.path.join(exception_dir, f"{cid}ConversionException.java"),
            projectname = projectname,
            connectorid = cid
        )


# ─────────────────────────────────────────────
# 10. MAIN ORCHESTRATOR
# ─────────────────────────────────────────────

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <definition.json>")
        sys.exit(1)

    json_file = sys.argv[1]
    print(f"\nReading connector definition from: {json_file}")

    try:
        definition = load_definition(json_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n[ERROR] Failed to load definition: {e}")
        sys.exit(1)

    projectname = definition["projectname"]
    connectors  = definition["connectors"]

    print(f"\n=== Generating Connector Project: {projectname} ===\n")

    try:
        copy_templates(projectname)
        edit_config_files(projectname)
        edit_api_files(projectname)
        edit_impl_files(projectname)
        generate_config_per_connector(projectname, connectors)
        generate_api_per_connector(projectname, connectors, json_file)
        generate_impl_per_connector(projectname, connectors, json_file)
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}")
        sys.exit(1)

    print("\n=== Generation Complete ===")


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def _projectname_to_path(projectname: str) -> str:
    """Convert dots in projectname to OS path separators for src directory construction."""
    return projectname.replace(".", os.sep)


def _replace_in_file(filepath: str, old: str, new: str):
    """Replace all occurrences of old with new in a file."""
    with open(filepath, "r") as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Updated: {filepath}")


def _singularize(name: str) -> str:
    """
    Simple singularization for IDL struct naming from a plural JSON field name.
    Examples: outages -> outage, categories -> category, addresses -> address
    """
    if name.endswith("ies"):
        return name[:-3] + "y"
    elif (name.endswith("sses") or name.endswith("xes")
          or name.endswith("ches") or name.endswith("shes")):
        return name[:-2]
    elif name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _is_date_string(value: str) -> bool:
    """
    Return True if the string value looks like a date or datetime.
    Checked via regex patterns, case-insensitive.
    """
    import re
    patterns = [
        r'\d{4}-\d{2}-\d{2}',
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}',
        r'\w+ \d{2}, \d{4}, \d{1,2}:\d{2}:\d{2} [AP]M',
    ]
    for pattern in patterns:
        if re.match(pattern, value, re.IGNORECASE):
            return True
    return False


def _first_non_null_value(items: list, key: str):
    """
    Search all elements of a list-of-dicts for the first non-null value
    for the given key. Returns None if all values are null or key is absent.
    """
    for item in items:
        if isinstance(item, dict):
            val = item.get(key)
            if val is not None:
                return val
    return None


def _infer_fields_from_list(items: list, indent: int) -> str:
    """
    Infer IDL fields from a list of JSON objects by scanning ALL elements,
    not just the first. For each field key, the first non-null value across
    all elements is used to determine the IDL type.
    Fields that are null across all elements get a TODO comment.
    """
    tab   = "\t" * indent
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
            struct_name   = key.capitalize()
            nested_fields = _json_to_idl_fields(best_value, indent + 1)
            lines.append(f"{tab}struct {struct_name} {{")
            if nested_fields:
                lines.append(nested_fields)
            lines.append(f"{tab}}}")
            lines.append(f"{tab}{struct_name} {key}")
        elif isinstance(best_value, list) and best_value and isinstance(best_value[0], dict):
            singular_name = _singularize(key).capitalize()
            elem_fields   = _infer_fields_from_list(best_value, indent + 1)
            lines.append(f"{tab}struct {singular_name} {{")
            if elem_fields:
                lines.append(elem_fields)
            lines.append(f"{tab}}}")
            lines.append(f"{tab}list of {singular_name} {key}")
        else:
            idl_type, comment = _json_value_to_idl_type(key, best_value, indent)
            field_line = f"{tab}{idl_type} {key}"
            if comment:
                field_line = f"{field_line}  {comment}"
            lines.append(field_line)

    return "\n".join(lines)


def _json_to_idl_fields(data, indent: int = 1) -> str:
    """
    Recursively convert a parsed JSON object (dict or list) into IDL field declarations.
    JSON type mapping:
      str               -> string (or date if value matches a date pattern)
      int               -> long
      float             -> double
      bool              -> boolean
      None              -> string  + TODO comment
      list (empty)      -> list of string  + TODO comment
      list of primitives-> list of primitive IDL type
      list of objects   -> struct Singular defined first, then: list of Singular fieldname
      dict              -> struct FieldName defined first, then: FieldName fieldname
    """
    tab   = "\t" * indent
    lines = []

    if isinstance(data, list):
        if not data:
            return ""
        data = data[0] if isinstance(data[0], dict) else {}

    if not isinstance(data, dict):
        return ""

    for key, value in data.items():

        if isinstance(value, dict):
            struct_name   = key.capitalize()
            nested_fields = _json_to_idl_fields(value, indent + 1)
            lines.append(f"{tab}struct {struct_name} {{")
            if nested_fields:
                lines.append(nested_fields)
            lines.append(f"{tab}}}")
            lines.append(f"{tab}{struct_name} {key}")

        elif isinstance(value, list) and value and isinstance(value[0], dict):
            singular_name = _singularize(key).capitalize()
            elem_fields   = _infer_fields_from_list(value, indent + 1)
            lines.append(f"{tab}struct {singular_name} {{")
            if elem_fields:
                lines.append(elem_fields)
            lines.append(f"{tab}}}")
            lines.append(f"{tab}list of {singular_name} {key}")

        else:
            idl_type, comment = _json_value_to_idl_type(key, value, indent)
            field_line = f"{tab}{idl_type} {key}"
            if comment:
                field_line = f"{field_line}  {comment}"
            lines.append(field_line)

    return "\n".join(lines)


def _json_value_to_idl_type(key: str, value, indent: int) -> tuple:
    """
    Map a single JSON primitive or list-of-primitives value to a tuple of
    (idl_type_string, comment_string). comment_string is empty string when
    there is no comment. Dict and list-of-objects are handled directly in
    _json_to_idl_fields() and _infer_fields_from_list().
    """
    if isinstance(value, bool):
        return ("boolean", "")
    elif isinstance(value, int):
        return ("long", "")
    elif isinstance(value, float):
        return ("double", "")
    elif isinstance(value, str):
        if _is_date_string(value):
            return ("date", "")
        return ("string", "")
    elif value is None:
        return ("string", "// TODO: verify data type - null in sample")
    elif isinstance(value, list):
        if not value:
            return ("list of string", "// TODO: verify data type - empty array in sample")
        first = value[0]
        if isinstance(first, bool):
            return ("list of boolean", "")
        elif isinstance(first, int):
            return ("list of long", "")
        elif isinstance(first, float):
            return ("list of double", "")
        elif isinstance(first, str):
            if _is_date_string(first):
                return ("list of date", "")
            return ("list of string", "")
        else:
            return ("list of string", "// TODO: verify data type - empty array in sample")
    else:
        return ("string", "")


def _write_types_idl(path: str, projectname: str, connectorid: str,
                     request_fields: str, entity_fields: str):
    """Generate the connectorid Types.model IDL file in the API datatypes package."""
    req_body    = f"\n{request_fields}\n" if request_fields else ""
    entity_body = f"\n{entity_fields}\n" if entity_fields else ""

    content = (
        f"package com.telus.connector.{projectname}.api.datatypes\n"
        f"\n"
        f"import com.telus.common.api.datatypes.AbstractDataRecord\n"
        f"\n"
        f"struct {connectorid}Request {{{req_body}}}\n"
        f"\n"
        f"struct {connectorid}Entity {{{entity_body}}}\n"
        f"\n"
        f"struct {connectorid}DataRecord : AbstractDataRecord {{\n"
        f"\t{connectorid}Entity entity\n"
        f"}}\n"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Types IDL: {path}")


def _write_osgi_xml(path: str, projectname: str, connectorid: str):
    """Generate OSGI-INF xml for the given connector."""
    content = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<scr:component xmlns:scr="http://www.osgi.org/xmlns/scr/v1.2.0"\n'
        f'    activate="configure"\n'
        f'    configuration-pid="com.telus.connector.{projectname}.{connectorid}.rest"\n'
        f'    configuration-policy="require"\n'
        f'    immediate="true"\n'
        f'    name="com.telus.connector.{projectname}.{connectorid}">\n'
        f'  <property name="target" value="com.telus.connector.{projectname}.SvcQualification"/>\n'
        f'  <implementation class="com.telus.connector.{projectname}.{connectorid}ConfigurationComponent"/>\n'
        f'  <service>\n'
        f'    <provide interface="com.telus.connector.{projectname}.I{connectorid}ConfigurationComponent"/>\n'
        f'  </service>\n'
        f'</scr:component>\n'
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated OSGI XML: {path}")


def _write_interface_config(path: str, projectname: str, connectorid: str):
    """Write a stub Java interface for I<connectorid>ConfigurationComponent."""
    content = (
        f"package com.telus.connector.{projectname};\n"
        f"public interface I{connectorid}ConfigurationComponent {{\n"
        f"}}"
    )
    with open(path, "w") as f:
        f.write(content)


def _write_impl_config(path: str, projectname: str, connectorid: str):
    """Write a stub Java class for <connectorid>ConfigurationComponent."""
    content = (
        f"package com.telus.connector.{projectname};\n"
        f"public class {connectorid}ConfigurationComponent"
        f" implements I{connectorid}ConfigurationComponent {{\n"
        f"}}"
    )
    with open(path, "w") as f:
        f.write(content)


def _append_service_components(manifest_path, osgi_files):
    """Append OSGI-INF filenames to Service-Component in MANIFEST.MF."""
    entries = ",\n ".join([os.path.basename(f) for f in osgi_files])
    with open(manifest_path, "a") as f:
        f.write(f"\nService-Component: {entries}\n")


def _write_connectors_xml(connectors_xml: str, projectname: str, connectors: list):
    """Generate OSGI-INF/connectors.xml with one connector block per connector definition."""
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    root = ET.Element("connectors")

    for connector in connectors:
        cid            = connector["connectorid"]
        input_class    = connector["inputClass"]
        data_rec_class = connector["dataRecordClass"]

        conn_el = ET.SubElement(root, "connector")
        conn_el.set("version",     "1.0.0")
        conn_el.set("name",        cid)
        conn_el.set("description", "")
        conn_el.set("id",          f"com.telus.connector.{projectname}.{cid}")

        input_el = ET.SubElement(conn_el, "input")
        input_el.set("name",  "parameters")
        input_el.set("class", f"com.telus.connector.{projectname}.api.datatypes.{input_class}")

        output_el = ET.SubElement(conn_el, "output")
        output_el.set("class", f"com.telus.connector.{projectname}.api.datatypes.{data_rec_class}")

    raw_xml    = ET.tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="\t")

    lines = pretty_xml.splitlines()
    lines = [line for line in lines if line.strip()]
    lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    final_xml = "\n".join(lines)

    with open(connectors_xml, "w", encoding="utf-8") as f:
        f.write(final_xml)

    print(f"Generated: {connectors_xml}")
    for connector in connectors:
        print(f"  + connector: {connector['connectorid']}")


def _write_java_stub(path, projectname, connectorid, role):
    """Write a stub Java file for Connector/Converter/Factory/Exception."""
    class_name = {
        "call":      f"{connectorid}Connector",
        "converter": f"{connectorid}Converter",
        "factories": f"{connectorid}Factory",
        "exception": f"{connectorid}Exception",
    }[role]
    content = (
        f"package com.telus.connector.{projectname}.{role};\n"
        f"public class {class_name} {{\n"
        f"}}"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated stub: {path}")


def _write_connector_java(path: str, projectname: str, connectorid: str, http_method: str):
    """Generate Connector.java from TemplateConnector.java.txt."""
    import re

    if not os.path.exists(TEMPLATE_CONNECTOR_JAVA):
        raise FileNotFoundError(
            f"TemplateConnector.java.txt not found at: {TEMPLATE_CONNECTOR_JAVA}"
        )

    with open(TEMPLATE_CONNECTOR_JAVA, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    output_lines  = []
    in_block      = False
    block_matched = False

    re_if      = re.compile(r'//\s*ConnectorGenerator:\s*if\s+<httpMethod>\s*==\s*(\w+)')
    re_else_if = re.compile(r'//\s*ConnectorGenerator:\s*else if\s+<httpMethod>\s*==\s*(\w+)')
    re_end_if  = re.compile(r'//\s*ConnectorGenerator:\s*end if')

    for line in lines:
        stripped = line.strip()

        m_if = re_if.match(stripped)
        if m_if:
            in_block      = True
            block_matched = (m_if.group(1).upper() == http_method.upper())
            continue

        m_else_if = re_else_if.match(stripped)
        if m_else_if:
            if not block_matched:
                block_matched = (m_else_if.group(1).upper() == http_method.upper())
            else:
                block_matched = False
            continue

        if re_end_if.match(stripped):
            in_block      = False
            block_matched = False
            continue

        if in_block:
            if block_matched:
                output_lines.append(line)
        else:
            output_lines.append(line)

    content = "".join(output_lines)
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Connector java [{http_method}]: {path}")


def _write_factory_java(path: str, projectname: str, connectorid: str, api_path: str):
    """Generate Factory.java from TemplateFactory.java.txt."""
    if not os.path.exists(TEMPLATE_FACTORY_JAVA):
        raise FileNotFoundError(
            f"TemplateFactory.java.txt not found at: {TEMPLATE_FACTORY_JAVA}"
        )

    with open(TEMPLATE_FACTORY_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>",  connectorid)
    content = content.replace("<apiPath>",       api_path)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Factory java: {path}")


def _write_exception_java(path: str, projectname: str, connectorid: str):
    """Generate ConversionException.java from TemplateException.java.txt."""
    if not os.path.exists(TEMPLATE_EXCEPTION_JAVA):
        raise FileNotFoundError(
            f"TemplateException.java.txt not found at: {TEMPLATE_EXCEPTION_JAVA}"
        )

    with open(TEMPLATE_EXCEPTION_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>",  connectorid)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Exception java: {path}")


def _json_to_pojo_fields(data, projectname: str, model_dir: str,
                         nested_classes: list) -> str:
    """
    Convert a parsed JSON object into Java POJO field declarations, getters, and setters.
    Recursively generates separate POJO files for nested objects and lists of objects,
    writing them to model_dir. Discovered nested class names are appended to nested_classes
    so the caller can build the correct import statements.

    Type mapping:
      bool              -> boolean
      int               -> long
      float             -> double
      str (date)        -> Date
      str               -> String
      None              -> String  (with TODO comment)
      list of objects   -> List<SingularClassName>  (generates SingularClassNamePojo.java)
      list (other)      -> List<String>
      dict              -> ClassName  (generates ClassNamePojo.java)
    """
    if isinstance(data, list):
        data = data[0] if data and isinstance(data[0], dict) else {}
    if not isinstance(data, dict):
        return ""

    fields  = []
    methods = []

    for key, value in data.items():
        cap_key = key[0].upper() + key[1:] if key else key
        comment = ""

        if isinstance(value, bool):
            java_type = "boolean"

        elif isinstance(value, int):
            java_type = "long"

        elif isinstance(value, float):
            java_type = "double"

        elif isinstance(value, str):
            java_type = "Date" if _is_date_string(value) else "String"

        elif value is None:
            java_type = "String"
            comment   = " // TODO: verify data type - null in sample"

        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                # List of objects — singularize key for class name
                singular_name = _singularize(key).capitalize()
                class_name    = f"{singular_name}Pojo"
                java_type     = f"List<{singular_name}>"
                # Collect all keys across all elements (best non-null per key)
                merged = {}
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if k not in merged or merged[k] is None:
                                merged[k] = v
                # Recursively write the nested POJO file
                nested_path = os.path.join(model_dir, f"{class_name}.java")
                _write_pojo_java(
                    path        = nested_path,
                    projectname = projectname,
                    class_name  = class_name,
                    json_path   = None,
                    label       = f"nested list element for '{key}'",
                    data        = merged
                )
                if singular_name not in nested_classes:
                    nested_classes.append(singular_name)
            elif not value:
                java_type = "List<String>"
                comment   = " // TODO: verify data type - empty array in sample"
            else:
                # List of primitives
                first = value[0]
                if isinstance(first, bool):
                    java_type = "List<Boolean>"
                elif isinstance(first, int):
                    java_type = "List<Long>"
                elif isinstance(first, float):
                    java_type = "List<Double>"
                elif isinstance(first, str):
                    java_type = "List<Date>" if _is_date_string(first) else "List<String>"
                else:
                    java_type = "List<String>"

        elif isinstance(value, dict):
            # Nested object — use capitalized key as class name
            class_name = f"{cap_key}Pojo"
            java_type  = cap_key
            nested_path = os.path.join(model_dir, f"{class_name}.java")
            _write_pojo_java(
                path        = nested_path,
                projectname = projectname,
                class_name  = class_name,
                json_path   = None,
                label       = f"nested object for '{key}'",
                data        = value
            )
            if cap_key not in nested_classes:
                nested_classes.append(cap_key)

        else:
            java_type = "String"

        fields.append(f"\tprivate {java_type} {key};{comment}")
        methods.append(
            f"\tpublic {java_type} get{cap_key}() {{ return {key}; }}\n"
            f"\tpublic void set{cap_key}({java_type} {key}) {{ this.{key} = {key}; }}"
        )

    return "\n".join(fields) + "\n\n" + "\n\n".join(methods)

def _write_pojo_java(path: str, projectname: str, class_name: str,
                     json_path: str, label: str, data: dict = None):
    """
    Generate a POJO Java class in model/ from either a JSON example file (json_path)
    or a pre-parsed dict (data). Nested objects and lists of objects are recursively
    written as separate POJO files in the same directory.

    Parameters:
      path        : output file path
      projectname : used for the package declaration
      class_name  : Java class name (e.g. "SampleResponsePojo", "OutagePojo")
      json_path   : path to JSON example file — used when data is None
      label       : description for log/warn messages
      data        : pre-parsed dict — used for recursively generated nested POJOs;
                    when provided, json_path is ignored
    """
    model_dir      = os.path.dirname(path)
    nested_classes = []   # collects names of nested POJO classes generated
    pojo_fields    = ""

    if data is not None:
        # Called recursively with pre-parsed data — no file to read
        pojo_fields = _json_to_pojo_fields(data, projectname, model_dir, nested_classes)
        print(f"  [POJO] Generated nested class: '{class_name}'")

    elif json_path and os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        try:
            with open(json_path, "r", encoding="utf-8-sig") as f:
                raw = json.load(f)
            pojo_fields = _json_to_pojo_fields(raw, projectname, model_dir, nested_classes)
            print(f"  [POJO] Generated fields from {label}: '{os.path.basename(json_path)}'")
        except (json.JSONDecodeError, OSError) as e:
            print(f"  [WARN] Could not read/parse {label} '{os.path.basename(json_path)}': {e}")
    else:
        if json_path:
            print(f"  [WARN] {label} file not found or empty: {json_path}")

    # ── Build import block ──────────────────────────────────────────────────────
    import_lines = []
    if "Date"    in pojo_fields:
        import_lines.append("import java.util.Date;")
    if "List<"   in pojo_fields:
        import_lines.append("import java.util.List;")
    # Import each recursively generated nested POJO class
    for nc in nested_classes:
        import_lines.append(f"import com.telus.connector.{projectname}.model.{nc}Pojo;")

    imports = ("\n".join(import_lines) + "\n\n") if import_lines else ""
    body    = pojo_fields if pojo_fields else "\t// TODO: add fields"

    content = (
        f"package com.telus.connector.{projectname}.model;\n"
        f"\n"
        f"{imports}"
        f"public class {class_name} {{\n"
        f"\n"
        f"{body}\n"
        f"\n"
        f"}}\n"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated POJO: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated POJO: {path}")


def _json_to_conversion_logic(json_path: str, source_var: str = "pojo") -> str:
    """
    Read a JSON example file and generate complete one-to-one mapping code,
    including private helper methods for all nested objects and lists of objects.

    For to<connectorid>Entity()  — source_var = "pojo"    (responseExample JSON)
    For to<connectorid>Pojo()    — source_var = "request" (requestExample JSON)

    Returns a string containing:
      - The body lines for the top-level mapping method
      - Private helper convert methods for every nested struct/list-of-struct

    If the file is missing, empty, or unparseable, returns an empty string.
    """
    if not json_path or not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
        return ""

    try:
        with open(json_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return ""

    # Unwrap list root to first element
    if isinstance(data, list):
        data = data[0] if data and isinstance(data[0], dict) else {}

    if not isinstance(data, dict):
        return ""

    # Collect all generated helper methods (deduplicated by struct name)
    helper_methods = {}   # struct_name -> method_source_string

    def _map_fields(obj: dict, src: str) -> str:
        """
        Generate rv.setXxx(...) lines for each field in obj.
        src is the variable name to call getters on.
        Appends helper methods to helper_methods as a side-effect.
        Returns the body lines as a string (double-tab indented).
        """
        lines = []
        for key, value in obj.items():
            cap_key = key[0].upper() + key[1:] if key else key

            if isinstance(value, dict):
                # Nested object → generate a convertTo<Key>() helper
                struct_name = cap_key          # e.g. "Meta"
                pojo_class  = f"{cap_key}Pojo" # e.g. "MetaPojo"
                _ensure_helper(struct_name, pojo_class, value)
                lines.append(f"\t\trv.set{cap_key}(convertTo{struct_name}({src}.get{cap_key}()));")

            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # List of objects → generate a convertTo<Singular>() helper + loop
                singular      = _singularize(key).capitalize()  # e.g. "Outage"
                pojo_class    = f"{singular}Pojo"               # e.g. "OutagePojo"
                # Merge all elements to get the full field set
                merged = {}
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if k not in merged or merged[k] is None:
                                merged[k] = v
                _ensure_helper(singular, pojo_class, merged)
                lines.append(
                    f"\t\tfor ({pojo_class} item : safe({src}.get{cap_key}())) {{\n"
                    f"\t\t\trv.get{cap_key}().add(convertTo{singular}(item));\n"
                    f"\t\t}}"
                )

            else:
                # Primitive, date, string, list of primitives → direct mapping
                lines.append(f"\t\trv.set{cap_key}({src}.get{cap_key}());")

        return "\n".join(lines)

    def _ensure_helper(struct_name: str, pojo_class: str, obj: dict):
        """
        Generate a private convertTo<StructName>() helper method if not already done.
        Recursively processes nested fields inside obj.
        """
        if struct_name in helper_methods:
            return  # already generated

        # Reserve slot immediately to prevent infinite recursion on self-referencing types
        helper_methods[struct_name] = ""

        inner_body = _map_fields(obj, "pojo")

        method = (
            f"\tprivate {struct_name} convertTo{struct_name}({pojo_class} pojo) {{\n"
            f"\t\tif (pojo == null) return null;\n"
            f"\t\t{struct_name} rv = new {struct_name}();\n"
            f"{inner_body}\n"
            f"\t\treturn rv;\n"
            f"\t}}"
        )
        helper_methods[struct_name] = method

    # Generate the top-level body lines
    top_level_body = _map_fields(data, source_var)

    # Assemble: top-level body + all helper methods
    result_parts = [top_level_body]
    for method_src in helper_methods.values():
        if method_src:
            result_parts.append(method_src)

    return "\n\n".join(result_parts)

def _write_converter_java(path: str, projectname: str, connectorid: str,
                          request_example_stem: str, response_example_stem: str,
                          resp_json_path: str, req_json_path: str):
    """
    Generate <connectorid>Converter.java from TemplateConverter.java.txt.

    Token replacements:
      <projectname>     -> projectname
      <connectorid>     -> connectorid
      <requestExample>  -> request_example_stem (stem of requestExample filename,
                           or connectorid if None)
      <responseExample> -> response_example_stem (stem of responseExample filename)

    TODO replacements (in order of occurrence in the template):
      1st // TODO: implement the conversion logic here
          -> inside to<connectorid>Entity(): rv.setXxx(pojo.getXxx());
             derived from responseExample JSON top-level keys
      2nd // TODO: implement the conversion logic here
          -> inside to<connectorid>Pojo(): rv.setXxx(request.getXxx());
             derived from requestExample JSON top-level keys
    """
    if not os.path.exists(TEMPLATE_CONVERTER_JAVA):
        raise FileNotFoundError(
            f"TemplateConverter.java.txt not found at: {TEMPLATE_CONVERTER_JAVA}"
        )

    with open(TEMPLATE_CONVERTER_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # If no requestExample, use connectorid as a safe fallback for the token
    req_stem  = request_example_stem  if request_example_stem  else connectorid
    resp_stem = response_example_stem if response_example_stem else connectorid

    content = content.replace("<projectname>",     projectname)
    content = content.replace("<connectorid>",     connectorid)
    content = content.replace("<requestExample>",  req_stem)
    content = content.replace("<responseExample>", resp_stem)

    todo_marker = "// TODO: implement the conversion logic here"

    # ── 1st TODO: to<connectorid>Entity() — maps pojo → rv (from responseExample) ──
    entity_logic = _json_to_conversion_logic(resp_json_path, source_var="pojo")
    if entity_logic:
        content = content.replace(todo_marker, entity_logic, 1)
        print(f"  [Converter] Injected entity conversion logic "
              f"({len(entity_logic.splitlines())} fields) from responseExample")
    else:
        print(f"  [Converter] No responseExample JSON — 1st TODO retained")

    # ── 2nd TODO: to<connectorid>Pojo() — maps request → rv (from requestExample) ──
    pojo_logic = _json_to_conversion_logic(req_json_path, source_var="request")
    if pojo_logic:
        content = content.replace(todo_marker, pojo_logic, 1)
        print(f"  [Converter] Injected pojo conversion logic "
              f"({len(pojo_logic.splitlines())} fields) from requestExample")
    else:
        print(f"  [Converter] No requestExample JSON — 2nd TODO retained")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Converter java: {path}")


if __name__ == "__main__":
    main()