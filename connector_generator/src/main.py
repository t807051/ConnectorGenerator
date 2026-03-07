import os
import re
import json
import shutil
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ─────────────────────────────────────────────
# 1. CONSTANTS
# ─────────────────────────────────────────────

#BASEDIR          = r"C:\github\Insight10.8\Insight"
BASEDIR          = r"C:\TEMP"
CONNECTORDIR     = os.path.join(BASEDIR, "connectors")
BUILDDIR         = os.path.join(BASEDIR, "build")
KBDIR            = os.path.join(BASEDIR, r"knowledgebases\com.telus.falcon.knowledgebase")
MODELDIR         = os.path.join(KBDIR, "model")
CALLDIR          = os.path.join(MODELDIR, r"da\call")
QADIR            = os.path.join(MODELDIR, r"qa\da")

#TEMPLATEDIR          = r"C:\cb\Insight10.8\Template"
TEMPLATEDIR          = r"C:\github\t807051\ConnectorGenerator\Template"
TEMPLATECONNECTORDIR = os.path.join(TEMPLATEDIR, "connectors")
TEMPLATEBUILDDIR     = os.path.join(TEMPLATEDIR, "build")
TEMPLATEKBCALLDIR    = os.path.join(TEMPLATEDIR, r"knowledgebases\com.telus.falcon.knowledgebase\models\da\call")
TEMPLDATEKBQADIR     = os.path.join(TEMPLATEDIR, r"knowledgebases\com.telus.falcon.knowledgebase\models\qa\da")

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
TEMPLATE_ICONFIG_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME + ".config",
    "src", "com", "telus", "connector", TEMPLATE_NAME, "ITemplateConfigurationComponent.java.txt"
)
TEMPLATE_CONFIG_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME + ".config",
    "src", "com", "telus", "connector", TEMPLATE_NAME, "TemplateConfigurationComponent.java.txt"
)
TEMPLATE_SPEC_MD = os.path.join(TEMPLATEDIR, "ConnectorSpecTemplate.md.txt")


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
        raise ValueError(f"JSON definition file is invalid: {e}")

    if "projectname" not in data:
        raise ValueError("Missing required field: 'projectname'")
    if "connectors" not in data or not data["connectors"]:
        raise ValueError("Missing or empty required field: 'connectors'")
    for connector in data["connectors"]:
        for field in ["connectorid", "inputClass", "entityClass",
                      "dataRecordClass", "apiPath", "httpMethod"]:
            if field not in connector:
                raise ValueError(f"Connector missing required field: '{field}'")
    return data


# ─────────────────────────────────────────────
# 3. COPY TEMPLATES
# ─────────────────────────────────────────────

def copy_templates(projectname: str):
    """Copy all template directories recursively to their target locations."""
    copies = [
        (f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}",
         f"{CONNECTORDIR}\\com.telus.connector.{projectname}"),
        (f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}.api",
         f"{CONNECTORDIR}\\com.telus.connector.{projectname}.api"),
        (f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}.config",
         f"{CONNECTORDIR}\\com.telus.connector.{projectname}.config"),
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
    """Edit .project, pom.xml, and MANIFEST.MF in the config project directory.
    Strips pre-existing Service-Component entries from MANIFEST.MF."""
    config_dir    = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    manifest_path = os.path.join(config_dir, r"META-INF\MANIFEST.MF")

    _replace_in_file(os.path.join(config_dir, ".project"), "svcqualification", projectname)
    _replace_in_file(os.path.join(config_dir, "pom.xml"),  "svcqualification", projectname)
    _replace_in_file(manifest_path,                         "svcqualification", projectname)

    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            content = f.read()
        content = re.sub(r'\n[\t ]*\nService-Component:[^\n]*(\n[ \t]+[^\n]*)*', '', content)
        content = re.sub(r'\nService-Component:[^\n]*(\n[ \t]+[^\n]*)*',          '', content)
        with open(manifest_path, "w") as f:
            f.write(content)
        print(f"  Cleaned Service-Component entries from: {manifest_path}")


# ─────────────────────────────────────────────
# 4b. EDIT BUILD FILES
# ─────────────────────────────────────────────

def edit_build_files(projectname: str):
    """Edit .project and pom.xml in each build subdirectory, plus
    category.xml in p2 and feature.xml in feature directory."""
    for suffix in ["api.esa", "build", "config.esa", "esa", "feature", "p2"]:
        build_dir    = os.path.join(BUILDDIR, f"com.telus.connector.{projectname}.{suffix}")
        project_file = os.path.join(build_dir, ".project")
        pom_file     = os.path.join(build_dir, "pom.xml")
        if os.path.exists(project_file):
            _replace_in_file(project_file, "svcqualification", projectname)
        else:
            print(f"[WARN] .project not found, skipping: {project_file}")
        if os.path.exists(pom_file):
            _replace_in_file(pom_file, "svcqualification", projectname)
        else:
            print(f"[WARN] pom.xml not found, skipping: {pom_file}")

    category_xml = os.path.join(BUILDDIR, f"com.telus.connector.{projectname}.p2", "category.xml")
    if os.path.exists(category_xml):
        _replace_in_file(category_xml, "svcqualification", projectname)
    else:
        print(f"[WARN] category.xml not found, skipping: {category_xml}")

    feature_xml = os.path.join(BUILDDIR, f"com.telus.connector.{projectname}.feature", "feature.xml")
    if os.path.exists(feature_xml):
        _replace_in_file(feature_xml, "svcqualification", projectname)
    else:
        print(f"[WARN] feature.xml not found, skipping: {feature_xml}")


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
    """Edit .project, pom.xml, MANIFEST.MF, Constants.java and rename src package."""
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

    constants_file = os.path.join(new_pkg, "Constants.java")
    if os.path.exists(constants_file):
        _replace_in_file(constants_file, "svcqualification", projectname)
    else:
        print(f"  [WARN] Constants.java not found, skipping: {constants_file}")


# ─────────────────────────────────────────────
# 7. GENERATE CONFIG FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_config_per_connector(projectname: str, connectors: list):
    """Generate OSGI-INF xml, ConfigComponent java files, and update MANIFEST.MF."""
    config_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    osgi_dir   = os.path.join(config_dir, "OSGI-INF")
    src_dir    = os.path.join(config_dir, "src", "com", "telus", "connector",
                              _projectname_to_path(projectname))
    delete_dir = os.path.join(config_dir, "src", "com", "telus", "connector", "svcqualification")

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

    for txt_name in ["ITemplateConfigurationComponent.java.txt",
                     "TemplateConfigurationComponent.java.txt"]:
        txt_path = os.path.join(delete_dir, txt_name)
        if os.path.exists(txt_path):
            os.remove(txt_path)
            print(f"  Deleted template file: {txt_path}")
        else:
            print(f"  [WARN] Template file not found for deletion: {txt_path}")
    os.rmdir(delete_dir)

    manifest_path = os.path.join(config_dir, r"META-INF\MANIFEST.MF")
    _append_service_components(manifest_path, osgi_files)


# ─────────────────────────────────────────────
# 8. GENERATE API FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_api_per_connector(projectname: str, connectors: list, definition_file: str):
    """Generate connectors.xml and <connectorid>Types.model IDL for each connector."""
    api_dir        = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.api")
    osgi_inf_dir   = os.path.join(api_dir, "OSGI-INF", "solvatio")
    connectors_xml = os.path.join(osgi_inf_dir, "connectors.xml")

    os.makedirs(osgi_inf_dir, exist_ok=True)
    _write_connectors_xml(connectors_xml, projectname, connectors)

    datatypes_dir = os.path.join(
        api_dir, "src", "com", "telus", "connector",
        _projectname_to_path(projectname), "api", "datatypes"
    )
    os.makedirs(datatypes_dir, exist_ok=True)

    definition_dir = os.path.dirname(os.path.abspath(definition_file))

    for connector in connectors:
        cid                    = connector["connectorid"]
        request_example_fname  = connector.get("requestExample")
        response_example_fname = connector.get("responseExample")

        request_fields  = ""
        request_structs = []
        if request_example_fname:
            req_path = os.path.join(definition_dir, request_example_fname)
            if os.path.exists(req_path) and os.path.getsize(req_path) > 0:
                try:
                    with open(req_path, "r", encoding="utf-8-sig") as f:
                        req_data = json.load(f)
                    request_fields = _json_to_idl_fields(req_data, indent=1,
                                                         top_level_structs=request_structs)
                    print(f"  [Types] Converted requestExample '{request_example_fname}' -> IDL fields")
                except (json.JSONDecodeError, OSError) as e:
                    print(f"  [WARN] Could not read/parse requestExample '{request_example_fname}': {e}")
            else:
                print(f"  [WARN] requestExample file not found or empty: {req_path}")

        entity_fields  = ""
        entity_structs = []
        if response_example_fname:
            resp_path = os.path.join(definition_dir, response_example_fname)
            if os.path.exists(resp_path) and os.path.getsize(resp_path) > 0:
                try:
                    with open(resp_path, "r", encoding="utf-8-sig") as f:
                        resp_data = json.load(f)
                    entity_fields = _json_to_idl_fields(resp_data, indent=1,
                                                        top_level_structs=entity_structs)
                    print(f"  [Types] Converted responseExample '{response_example_fname}' -> IDL fields")
                except (json.JSONDecodeError, OSError) as e:
                    print(f"  [WARN] Could not read/parse responseExample '{response_example_fname}': {e}")
            else:
                print(f"  [WARN] responseExample file not found or empty: {resp_path}")

        types_path = os.path.join(datatypes_dir, f"{cid}Types.model")
        _write_types_idl(types_path, projectname, cid,
                         request_fields, entity_fields,
                         request_structs, entity_structs)


# ─────────────────────────────────────────────
# 9. GENERATE IMPLEMENTATION FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_impl_per_connector(projectname: str, connectors: list, definition_file: str):
    """Generate Connector, POJO, Converter, Factory, and Exception java files per connector."""
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

        request_stem  = os.path.splitext(request_example_fname)[0]  if request_example_fname  else None
        response_stem = os.path.splitext(response_example_fname)[0] if response_example_fname else None

        call_dir = os.path.join(src_base, "call")
        os.makedirs(call_dir, exist_ok=True)
        _write_connector_java(
            path         = os.path.join(call_dir, f"{cid}Connector.java"),
            projectname  = projectname,
            connectorid  = cid,
            http_method  = http_method,
            request_stem = request_stem
        )

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
            _write_java_stub(
                os.path.join(converter_dir, f"{cid}Converter.java"),
                projectname, cid, "converter"
            )

        factories_dir = os.path.join(src_base, "factories")
        os.makedirs(factories_dir, exist_ok=True)
        _write_factory_java(
            path        = os.path.join(factories_dir, f"{cid}Factory.java"),
            projectname = projectname,
            connectorid = cid,
            api_path    = api_path
        )

        exception_dir = os.path.join(src_base, "exception")
        os.makedirs(exception_dir, exist_ok=True)
        _write_exception_java(
            path        = os.path.join(exception_dir, f"{cid}ConversionException.java"),
            projectname = projectname,
            connectorid = cid
        )

    template_txt_files = [
        os.path.join(src_base, "call",      "TemplateConnector.java.txt"),
        os.path.join(src_base, "converter", "TemplateConverter.java.txt"),
        os.path.join(src_base, "exception", "TemplateException.java.txt"),
        os.path.join(src_base, "factories", "TemplateFactory.java.txt"),
    ]
    for txt_path in template_txt_files:
        if os.path.exists(txt_path):
            os.remove(txt_path)
            print(f"  Deleted template file: {txt_path}")
        else:
            print(f"  [WARN] Template file not found for deletion: {txt_path}")


# ─────────────────────────────────────────────
# 10. GENERATE SPEC DOCUMENT
# ─────────────────────────────────────────────

def generate_spec_doc(projectname: str, connectors: list, definition: dict, definition_file: str):
    """
    Generate a Markdown connector specification document from
    ConnectorSpecTemplate.md.txt, processing all // SpecGenerator: directives.

    Output: BASEDIR\docs\<projectname>-connector-spec.md
    """
    if not os.path.exists(TEMPLATE_SPEC_MD):
        print(f"[WARN] ConnectorSpecTemplate not found, skipping spec doc: {TEMPLATE_SPEC_MD}")
        return

    with open(TEMPLATE_SPEC_MD, "r", encoding="utf-8-sig") as f:
        template = f.read()

    definition_dir = os.path.dirname(os.path.abspath(definition_file))
    today          = datetime.date.today().strftime("%Y-%m-%d")
    projectdesc    = definition.get("projectdescription", "")
    hosts          = definition.get("hosts", [])

    # ── Helper: load raw file text ─────────────────────────────────────────
    def _raw_file(fname):
        if not fname:
            return ""
        path = os.path.join(definition_dir, fname)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print(f"  [WARN] Example file not found or empty: {path}")
            return ""
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return f.read().strip()
        except OSError as e:
            print(f"  [WARN] Could not read example file '{fname}': {e}")
            return ""

    # ── Helper: fenced JSON code block ─────────────────────────────────────
    def _json_block(fname):
        raw = _raw_file(fname)
        return f"```json\n{raw}\n```" if raw else "_No example provided._"

    # ── Helper: fenced IDL block with named parent struct + nested structs ──
    def _idl_block_for_spec(fname, struct_name):
        """
        Wraps top-level IDL fields in 'struct <struct_name> { }',
        emits nested structs after (separated by blank lines),
        and appends a WARNINGS section for any empty-array TODO comments.
        """
        if not fname:
            return "_No example provided._"
        path = os.path.join(definition_dir, fname)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print(f"  [WARN] Example file not found or empty for IDL: {path}")
            return "_Example file not found._"
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  [WARN] Could not parse '{fname}' for IDL: {e}")
            return "_Could not parse example file._"

        nested_structs = []
        fields = _json_to_idl_fields(data, indent=1, top_level_structs=nested_structs)

        # Parent struct first, then nested structs
        parent_block = f"struct {struct_name} {{\n{fields}\n}}"
        all_blocks   = [parent_block] + nested_structs

        # Build fenced code block
        code_lines = ["```"]
        for i, block in enumerate(all_blocks):
            code_lines.append(block)
            if i < len(all_blocks) - 1:
                code_lines.append("")   # blank line between structs
        code_lines.append("```")
        result = "\n".join(code_lines)

        # Collect WARNINGS for empty-array TODO comments
        warning_lines = []
        for block in all_blocks:
            struct_match = re.match(r'struct (\w+)', block)
            sname = struct_match.group(1) if struct_match else struct_name
            for line in block.splitlines():
                if "// TODO: verify data type - empty array in sample" in line:
                    parts = line.strip().split()
                    field = parts[1] if len(parts) >= 2 else "?"
                    warning_lines.append(
                        f"Unverified data type for {sname}.{field} - empty array in sample<br>"
                    )

        if warning_lines:
            result += "\n**WARNINGS:**\n<br>" + "\n".join(warning_lines)

        return result

    # ── Helper: build nodemanager XML block for one host + one connector ───
    def _nodemanager_block(host, connector):
        hostname   = host.get("hostname", "")
        auth       = host.get("authentication", "").lower()
        cid        = connector["connectorid"]
        api_path   = connector.get("apiPath", "")
        service_id = f"com.telus.connector.{projectname}.{cid}.rest"
        endpoint   = f"{hostname}/{api_path.lstrip('/')}"

        if auth == "basic":
            return (
                f'    <service serviceId="{service_id}">\n'
                f'        <property name="endpoint" type="string">{endpoint}</property>\n'
                f'        <property name="password" type="string">'
                f'Oa0rDOv9oP+P14jitaDWgf3/woLmsq14+oNU8NEORxN+hv2+2six76JPm1WvbGzwSJ1V6kOI1E5SH0+23PsJkw==</property>\n'
                f'        <property name="authenticationType" type="string">basic</property>\n'
                f'        <property name="timeout" type="int">4000</property>\n'
                f'        <property name="username" type="string">APP_SOLVATIO</property>\n'
                f'    </service>'
            )
        else:  # kong (default)
            return (
                f'    <service serviceId="{service_id}">\n'
                f'        <property name="endpoint" type="string">{endpoint}</property>\n'
                f'        <property name="authenticationType" type="string">kong</property>\n'
                f'        <property name="timeout" type="int">4000</property>\n'
                f'    </service>'
            )

    # ── Step 1: today's date (both occurrences — header table + footer) ────
    template = template.replace(
        "//SpecGenerator: insert today's date in yyyy-mm-dd format",
        today
    )

    # ── Step 2: projectdescription ─────────────────────────────────────────
    template = template.replace(
        "// SpecGenerator: Insert <projectdescription>",
        projectdesc if projectdesc else "_No description provided._"
    )

    # ── Step 3: Endpoints table — replace placeholder row with real rows ───
    host_rows = "\n".join(
        f"| {h.get('env', '')} | {h.get('hostname', '')} | {h.get('authentication', '')} |"
        for h in hosts
    ) if hosts else "| | | |"

    template = re.sub(
        r'\|[^\n]*SpecGenerator: Insert <hosts\.env>[^\n]*\|[^\n]*\n?',
        host_rows + "\n",
        template
    )

    # ── Step 4: Nodemanager Definitions block ──────────────────────────────
    nodemanager_lines = []
    for host in hosts:
        env = host.get("env", "")
        nodemanager_lines.append(f"\n### {env}\n")
        for connector in connectors:
            cid = connector["connectorid"]
            nodemanager_lines.append(f"\n#### {cid}\n")
            nodemanager_lines.append("```xml")
            nodemanager_lines.append(_nodemanager_block(host, connector))
            nodemanager_lines.append("```\n")

    nodemanager_output = "\n".join(nodemanager_lines)

    template = re.sub(
        r'// SpecGenerator: define nodemanager definition.*?// SpecGenerator: Insert pagebreak',
        nodemanager_output + "\n\n// SpecGenerator: Insert pagebreak",
        template,
        count=1,
        flags=re.DOTALL
    )

    # ── Step 5: Connector Definitions for-each loop ────────────────────────
    # Marker: "// SpecGenerator: for each <connectorid>" ... "// SpecGenerator: end for"
    def_for_pattern = re.compile(
        r'// SpecGenerator: for each <connectorid>\s*\n'
        r'(.*?)'
        r'// SpecGenerator: end for\b(?! loop)',   # "end for" but NOT "end for loop"
        re.DOTALL
    )

    def _expand_definitions(match):
        body_template = match.group(1)
        blocks = []
        for connector in connectors:
            cid           = connector["connectorid"]
            connectordesc = connector.get("connectordescription", "")
            req_fname     = connector.get("requestExample")
            resp_fname    = connector.get("responseExample")

            body = body_template

            # Substitute connector identity tokens (escaped brackets in template)
            body = body.replace(r"\<connectorid\>", cid)
            body = body.replace(r"\<projectname\>", projectname)

            # connectordescription
            body = body.replace(
                "// SpecGenerator: Insert <connectordescription>",
                connectordesc if connectordesc else "_No description provided._"
            )

            # IDL blocks — named struct wrappers with WARNINGS
            body = re.sub(
                r'// SpecGenerator: Insert \\<requestExample\\>Request object definition from IDL',
                _idl_block_for_spec(req_fname, f"{cid}Request"),
                body
            )
            body = re.sub(
                r'// SpecGenerator: Insert \\<responseExample\\>Entity object definition from IDL',
                _idl_block_for_spec(resp_fname, f"{cid}Entity"),
                body
            )

            blocks.append(body.rstrip())

        return "\n\n".join(blocks) + "\n"

    template = def_for_pattern.sub(_expand_definitions, template)

    # ── Step 6: Appendix A for-each loop ───────────────────────────────────
    # Marker: "// SpecGenerator: for each <connectorid>" ... "// SpecGenerator: end for loop"
    # Inside the loop body:
    #   <apiPath>                              → connector["apiPath"]
    #   <projectname>                          → projectname
    #   <connectorid>                          → cid (unescaped, no backslashes)
    #   // SpecGenerator: Insert <requestExample>   → fenced JSON block
    #   // SpecGenerator: Insert <responseExample>  → fenced JSON block
    #   // SpecGenerator: Insert pagebreak     → \n---\n\n  (between connectors)
    appendix_for_pattern = re.compile(
        r'// SpecGenerator: for each <connectorid>\s*\n'
        r'(.*?)'
        r'// SpecGenerator: end for loop',
        re.DOTALL
    )

    def _expand_appendix(match):
        body_template = match.group(1)
        blocks = []
        for connector in connectors:
            cid       = connector["connectorid"]
            api_path  = connector.get("apiPath", "")
            req_fname = connector.get("requestExample")
            resp_fname = connector.get("responseExample")

            body = body_template

            # Token substitutions (unescaped in this section of the template)
            body = body.replace("<connectorid>", cid)
            body = body.replace("<projectname>", projectname)
            body = body.replace("<apiPath>",     api_path)

            # Insert raw JSON blocks (unescaped directive syntax)
            body = body.replace(
                "// SpecGenerator: Insert <requestExample>",
                _json_block(req_fname)
            )
            body = body.replace(
                "// SpecGenerator: Insert <responseExample>",
                _json_block(resp_fname)
            )

            # Pagebreak inside the loop becomes a horizontal rule
            body = re.sub(
                r'// SpecGenerator: Insert pagebreak\s*',
                '\n---\n\n',
                body
            )

            blocks.append(body.rstrip())

        return "\n\n".join(blocks) + "\n"

    template = appendix_for_pattern.sub(_expand_appendix, template)

    # ── Step 7: TOC — scan headings in the now-processed template ──────────
    def _to_anchor(text):
        anchor = text.lower().strip()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        return anchor

    toc_lines = []
    for line in template.splitlines():
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level  = len(m.group(1))
            text   = m.group(2).strip()
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{text}](#{_to_anchor(text)})")

    toc_output = "\n".join(toc_lines) if toc_lines else "_No sections found._"
    template = template.replace(
        "// SpecGenerator: Insert links to document sections",
        toc_output
    )

    # ── Step 8: remaining pagebreaks → Markdown horizontal rules ───────────
    template = re.sub(
        r'// SpecGenerator: Insert pagebreak\s*',
        '\n---\n\n',
        template
    )

    # ── Step 9: write output ───────────────────────────────────────────────
    docs_dir = os.path.join(BASEDIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, f"{projectname}-connector-spec.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"Generated spec doc: {out_path}")
# ─────────────────────────────────────────────
# 11. MAIN ORCHESTRATOR
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
        edit_build_files(projectname)
        edit_api_files(projectname)
        edit_impl_files(projectname)
        generate_config_per_connector(projectname, connectors)
        generate_api_per_connector(projectname, connectors, json_file)
        generate_impl_per_connector(projectname, connectors, json_file)
        generate_spec_doc(projectname, connectors, definition, json_file)
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}")
        sys.exit(1)

    print("\n=== Generation Complete ===")


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def _projectname_to_path(projectname: str) -> str:
    """Convert dots in projectname to OS path separators."""
    return projectname.replace(".", os.sep)


def _replace_in_file(filepath: str, old: str, new: str):
    """Replace all occurrences of old with new in a file."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def _append_service_components(manifest_path: str, osgi_files: list):
    """Append Service-Component entries to MANIFEST.MF."""
    if not osgi_files:
        return
    entries = [f"OSGI-INF/{os.path.basename(p)}" for p in osgi_files]
    service_component_line = "Service-Component: " + entries[0]
    for entry in entries[1:]:
        service_component_line += ",\n " + entry

    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.endswith("\n"):
        content += "\n"
    content += service_component_line + "\n"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated MANIFEST.MF with Service-Component entries: {manifest_path}")


def _write_osgi_xml(path: str, projectname: str, connectorid: str):
    """Generate the OSGI-INF component XML for a connector."""
    content = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<scr:component xmlns:scr="http://www.osgi.org/xmlns/scr/v1.2.0"'
        f' activate="configure"'
        f' configuration-pid="com.telus.connector.{projectname}.{connectorid}.rest"'
        f' configuration-policy="require"'
        f' immediate="true"'
        f' name="com.telus.connector.{projectname}.{connectorid}">\n'
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
    """Generate I<connectorid>ConfigurationComponent.java from template."""
    if not os.path.exists(TEMPLATE_ICONFIG_JAVA):
        raise FileNotFoundError(f"ITemplateConfigurationComponent.java.txt not found: {TEMPLATE_ICONFIG_JAVA}")
    with open(TEMPLATE_ICONFIG_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>",  connectorid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated interface config: {path}")


def _write_impl_config(path: str, projectname: str, connectorid: str):
    """Generate <connectorid>ConfigurationComponent.java from template."""
    if not os.path.exists(TEMPLATE_CONFIG_JAVA):
        raise FileNotFoundError(f"TemplateConfigurationComponent.java.txt not found: {TEMPLATE_CONFIG_JAVA}")
    with open(TEMPLATE_CONFIG_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>",  connectorid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated impl config: {path}")


def _write_connectors_xml(connectors_xml: str, projectname: str, connectors: list):
    """Build OSGI-INF/solvatio/connectors.xml programmatically."""
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
    lines      = [line for line in pretty_xml.splitlines() if line.strip()]
    lines[0]   = '<?xml version="1.0" encoding="UTF-8"?>'
    final_xml  = "\n".join(lines)

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


def _write_connector_java(path: str, projectname: str, connectorid: str,
                          http_method: str, request_stem: str = None):
    """Generate <connectorid>Connector.java from TemplateConnector.java.txt."""
    if not os.path.exists(TEMPLATE_CONNECTOR_JAVA):
        raise FileNotFoundError(f"TemplateConnector.java.txt not found: {TEMPLATE_CONNECTOR_JAVA}")
    with open(TEMPLATE_CONNECTOR_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    method_upper = http_method.upper()
    lines     = content.splitlines(keepends=True)
    out_lines = []
    skip      = False
    for line in lines:
        if re.match(r'\s*// ConnectorGenerator: if <httpMethod> == (\w+)', line):
            m    = re.match(r'\s*// ConnectorGenerator: if <httpMethod> == (\w+)', line)
            skip = (m.group(1).upper() != method_upper)
            continue
        elif re.match(r'\s*// ConnectorGenerator: else if <httpMethod> == (\w+)', line):
            m    = re.match(r'\s*// ConnectorGenerator: else if <httpMethod> == (\w+)', line)
            skip = (m.group(1).upper() != method_upper)
            continue
        elif re.match(r'\s*// ConnectorGenerator: end if', line):
            skip = False
            continue
        if not skip:
            out_lines.append(line)
    content = "".join(out_lines)

    req_stem = request_stem if request_stem else connectorid
    content  = content.replace("<projectname>",    projectname)
    content  = content.replace("<connectorid>",    connectorid)
    content  = content.replace("<requestExample>", req_stem)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Connector java: {path}")


def _write_factory_java(path: str, projectname: str, connectorid: str, api_path: str):
    """Generate <connectorid>Factory.java from TemplateFactory.java.txt."""
    if not os.path.exists(TEMPLATE_FACTORY_JAVA):
        raise FileNotFoundError(f"TemplateFactory.java.txt not found: {TEMPLATE_FACTORY_JAVA}")
    with open(TEMPLATE_FACTORY_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    content = content.replace("<apiPath>",     api_path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Factory java: {path}")


def _write_exception_java(path: str, projectname: str, connectorid: str):
    """Generate <connectorid>ConversionException.java from TemplateException.java.txt."""
    if not os.path.exists(TEMPLATE_EXCEPTION_JAVA):
        raise FileNotFoundError(f"TemplateException.java.txt not found: {TEMPLATE_EXCEPTION_JAVA}")
    with open(TEMPLATE_EXCEPTION_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Exception java: {path}")


def _write_pojo_java(path: str, projectname: str, class_name: str,
                     json_path: str, label: str, data: dict = None):
    """Generate a POJO Java class from a JSON example file."""
    pojo_fields    = ""
    nested_classes = []
    model_dir      = os.path.dirname(path)

    if data is not None:
        pojo_fields = _json_to_pojo_fields(data, projectname, model_dir, nested_classes)
    elif json_path:
        if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
            try:
                with open(json_path, "r", encoding="utf-8-sig") as f:
                    raw = json.load(f)
                if isinstance(raw, list):
                    raw = raw[0] if raw and isinstance(raw[0], dict) else {}
                if isinstance(raw, dict):
                    pojo_fields = _json_to_pojo_fields(raw, projectname, model_dir, nested_classes)
            except (json.JSONDecodeError, OSError) as e:
                print(f"  [WARN] Could not parse '{os.path.basename(json_path)}': {e}")
        else:
            if json_path:
                print(f"  [WARN] {label} file not found or empty: {json_path}")

    import_lines = []
    if "Date"  in pojo_fields:
        import_lines.append("import java.util.Date;")
    if "List<" in pojo_fields:
        import_lines.append("import java.util.List;")
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


def _json_to_pojo_fields(data: dict, projectname: str, model_dir: str,
                         nested_classes: list) -> str:
    """Convert a JSON dict to Java POJO field declarations + getters/setters."""
    fields  = []
    methods = []

    for key, value in data.items():
        cap_key   = key[0].upper() + key[1:] if key else key
        comment   = ""
        java_type = "String"

        if isinstance(value, list) and value and isinstance(value[0], dict):
            singular_name = _singularize(key).capitalize()
            class_name    = f"{singular_name}Pojo"
            java_type     = f"List<{class_name}>"
            merged = {}
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if k not in merged or merged[k] is None:
                            merged[k] = v
            nested_path = os.path.join(model_dir, f"{class_name}.java")
            _write_pojo_java(path=nested_path, projectname=projectname,
                             class_name=class_name, json_path=None,
                             label=f"nested list element for '{key}'", data=merged)
            if singular_name not in nested_classes:
                nested_classes.append(singular_name)
        elif isinstance(value, list) and not value:
            java_type = "List<String>"
            comment   = " // TODO: verify data type - empty array in sample"
        elif isinstance(value, list):
            first = value[0]
            if isinstance(first, bool):    java_type = "List<Boolean>"
            elif isinstance(first, int):   java_type = "List<Long>"
            elif isinstance(first, float): java_type = "List<Double>"
            elif isinstance(first, str):   java_type = "List<Date>" if _is_date_string(first) else "List<String>"
            else:                          java_type = "List<String>"
        elif isinstance(value, dict):
            class_name  = f"{cap_key}Pojo"
            java_type   = f"{cap_key}Pojo"
            nested_path = os.path.join(model_dir, f"{class_name}.java")
            _write_pojo_java(path=nested_path, projectname=projectname,
                             class_name=class_name, json_path=None,
                             label=f"nested object for '{key}'", data=value)
            if cap_key not in nested_classes:
                nested_classes.append(cap_key)
        elif isinstance(value, bool):  java_type = "boolean"
        elif isinstance(value, int):   java_type = "long"
        elif isinstance(value, float): java_type = "double"
        elif isinstance(value, str):   java_type = "Date" if _is_date_string(value) else "String"
        elif value is None:
            java_type = "String"
            comment   = " // TODO: verify data type - null in sample"

        fields.append(f"\tprivate {java_type} {key};{comment}")
        methods.append(
            f"\tpublic {java_type} get{cap_key}() {{ return {key}; }}\n"
            f"\tpublic void set{cap_key}({java_type} {key}) {{ this.{key} = {key}; }}"
        )

    return "\n".join(fields) + "\n\n" + "\n\n".join(methods)


def _write_types_idl(path: str, projectname: str, connectorid: str,
                     request_fields: str, entity_fields: str,
                     request_structs: list = None, entity_structs: list = None):
    """Generate the <connectorid>Types.model IDL file."""
    req_body    = f"\n{request_fields}\n" if request_fields else ""
    entity_body = f"\n{entity_fields}\n" if entity_fields else ""

    extra_structs = []
    for s in (request_structs or []):
        if s not in extra_structs:
            extra_structs.append(s)
    for s in (entity_structs or []):
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
            nested_fields = _json_to_idl_fields(value, 1, top_level_structs)
            struct_block  = f"struct {struct_name} {{\n{nested_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{struct_name} {key}")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            singular_name = _singularize(key).capitalize()
            elem_fields   = _infer_fields_from_list(value, 1, top_level_structs)
            struct_block  = f"struct {singular_name} {{\n{elem_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{singular_name}[] {key}")
        else:
            idl_type, comment = _json_value_to_idl_type(key, value, indent)
            field_line = f"{tab}{idl_type} {key}"
            if comment:
                field_line = f"{field_line}  {comment}"
            lines.append(field_line)

    return "\n".join(lines)


def _json_value_to_idl_type(key: str, value, indent: int) -> tuple:
    """Map a single JSON value to (idl_type, comment)."""
    if isinstance(value, bool):    return ("bool",   "")
    elif isinstance(value, int):   return ("long",   "")
    elif isinstance(value, float): return ("double", "")
    elif isinstance(value, str):
        return ("date", "") if _is_date_string(value) else ("string", "")
    elif value is None:
        return ("string", "// TODO: verify data type - null in sample")
    elif isinstance(value, list):
        if not value:
            return ("string[]", "// TODO: verify data type - empty array in sample")
        first = value[0]
        if isinstance(first, bool):    return ("bool[]",   "")
        elif isinstance(first, int):   return ("long[]",   "")
        elif isinstance(first, float): return ("double[]", "")
        elif isinstance(first, str):
            return ("date[]", "") if _is_date_string(first) else ("string[]", "")
        else:
            return ("string[]", "// TODO: verify data type - empty array in sample")
    return ("string", "")


def _infer_fields_from_list(items: list, indent: int, top_level_structs: list) -> str:
    """Infer IDL fields from a list of JSON objects by scanning ALL elements."""
    tab   = "\t" * indent
    lines = []
    if not items or not isinstance(items[0], dict):
        return ""
    keys = list(items[0].keys())
    for key in keys:
        best_value = _first_non_null_value(items, key)
        if best_value is None:
            lines.append(f"{tab}string {key}  // TODO: verify data type - all values null in sample")
        elif isinstance(best_value, dict):
            struct_name   = key.capitalize()
            nested_fields = _json_to_idl_fields(best_value, 1, top_level_structs)
            struct_block  = f"struct {struct_name} {{\n{nested_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{struct_name} {key}")
        elif isinstance(best_value, list) and best_value and isinstance(best_value[0], dict):
            singular_name = _singularize(key).capitalize()
            elem_fields   = _infer_fields_from_list(best_value, 1, top_level_structs)
            struct_block  = f"struct {singular_name} {{\n{elem_fields}\n}}"
            if struct_block not in top_level_structs:
                top_level_structs.append(struct_block)
            lines.append(f"{tab}{singular_name}[] {key}")
        else:
            idl_type, comment = _json_value_to_idl_type(key, best_value, indent)
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
    elif name.endswith(("sses", "xes", "ches", "shes")):
        return name[:-2]
    elif name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _is_date_string(value: str) -> bool:
    """Return True if the string looks like a date or datetime."""
    patterns = [
        r'^\d{4}-\d{2}-\d{2}$',
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}',
        r'^\d{2}/\d{2}/\d{4}$',
        r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
    ]
    for pattern in patterns:
        if re.match(pattern, value, re.IGNORECASE):
            return True
    return False


def _json_to_conversion_logic(json_path: str, source_var: str = "pojo") -> tuple:
    """
    Read a JSON example file and generate mapping code + helper methods.
    Returns (top_level_body, helpers_str, nested_api_types).
    """
    if not json_path or not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
        return "", "", []
    try:
        with open(json_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return "", "", []

    if isinstance(data, list):
        data = data[0] if data and isinstance(data[0], dict) else {}
    if not isinstance(data, dict):
        return "", "", []

    helper_methods   = {}
    nested_api_types = []

    def _map_fields(obj: dict, src: str) -> str:
        lines = []
        for key, value in obj.items():
            cap_key = key[0].upper() + key[1:] if key else key
            if isinstance(value, dict):
                struct_name = cap_key
                pojo_class  = f"{cap_key}Pojo"
                _ensure_helper(struct_name, pojo_class, value)
                lines.append(f"\t\trv.set{cap_key}(convertTo{struct_name}({src}.get{cap_key}()));")
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                singular   = _singularize(key).capitalize()
                pojo_class = f"{singular}Pojo"
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
                lines.append(f"\t\trv.set{cap_key}({src}.get{cap_key}());")
        return "\n".join(lines)

    def _ensure_helper(struct_name: str, pojo_class: str, obj: dict):
        if struct_name in helper_methods:
            return
        helper_methods[struct_name] = ""
        if struct_name not in nested_api_types:
            nested_api_types.append(struct_name)
        inner_body = _map_fields(obj, "pojo")
        method = (
            f"\tprivate {struct_name} convertTo{struct_name}({pojo_class} pojo) {{\n"
            f"\t\tif (pojo == null) return null;\n"
            f"\t\t{struct_name} rv = {struct_name}.create();\n"
            f"{inner_body}\n"
            f"\t\treturn rv;\n"
            f"\t}}"
        )
        helper_methods[struct_name] = method

    top_level_body = _map_fields(data, source_var)
    helpers_str    = "\n\n".join(m for m in helper_methods.values() if m)
    return top_level_body, helpers_str, nested_api_types


def _write_converter_java(path: str, projectname: str, connectorid: str,
                          request_example_stem: str, response_example_stem: str,
                          resp_json_path: str, req_json_path: str):
    """Generate <connectorid>Converter.java from TemplateConverter.java.txt."""
    if not os.path.exists(TEMPLATE_CONVERTER_JAVA):
        raise FileNotFoundError(f"TemplateConverter.java.txt not found: {TEMPLATE_CONVERTER_JAVA}")
    with open(TEMPLATE_CONVERTER_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    if request_example_stem:
        content = re.sub(r'// ConnectorGenerator: if <requestExample> != null\n', '', content)
        content = re.sub(r'// ConnectorGenerator: end if\n', '', content)
    else:
        content = re.sub(
            r'// ConnectorGenerator: if <requestExample> != null\n.*?// ConnectorGenerator: end if\n',
            '', content, flags=re.DOTALL)

    req_stem  = request_example_stem  if request_example_stem  else connectorid
    resp_stem = response_example_stem if response_example_stem else connectorid
    content   = content.replace("<projectname>",     projectname)
    content   = content.replace("<connectorid>",     connectorid)
    content   = content.replace("<requestExample>",  req_stem)
    content   = content.replace("<responseExample>", resp_stem)

    todo_marker = "// TODO: implement the conversion logic here"

    entity_body, entity_helpers, entity_api_types = _json_to_conversion_logic(
        resp_json_path, source_var="pojo"
    )
    all_api_types = list(entity_api_types)

    if entity_body:
        content = content.replace(todo_marker, entity_body, 1)
        print(f"  [Converter] Injected entity conversion logic ({len(entity_body.splitlines())} lines)")
    else:
        print(f"  [Converter] No responseExample JSON — 1st TODO retained")

    pojo_body, pojo_helpers, pojo_api_types = _json_to_conversion_logic(
        req_json_path, source_var="request"
    )
    for t in pojo_api_types:
        if t not in all_api_types:
            all_api_types.append(t)

    if pojo_body:
        content = content.replace(todo_marker, pojo_body, 1)
        print(f"  [Converter] Injected pojo conversion logic ({len(pojo_body.splitlines())} lines)")
    else:
        print(f"  [Converter] No requestExample JSON — 2nd TODO retained")

    all_helpers = "\n\n".join(h for h in [entity_helpers, pojo_helpers] if h)
    if all_helpers:
        last_brace_idx = content.rfind("\n}")
        if last_brace_idx != -1:
            content = (content[:last_brace_idx] + "\n\n" + all_helpers + content[last_brace_idx:])

    if all_api_types:
        import_lines = "\n".join(
            f"import com.telus.connector.{projectname}.api.datatypes.{t};"
            for t in all_api_types
        )
        last_import_match = None
        for m in re.finditer(r'^import .*;', content, re.MULTILINE):
            last_import_match = m
        if last_import_match:
            insert_pos = last_import_match.end()
            content    = content[:insert_pos] + "\n" + import_lines + content[insert_pos:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Converter java: {path}")


if __name__ == "__main__":
    main()