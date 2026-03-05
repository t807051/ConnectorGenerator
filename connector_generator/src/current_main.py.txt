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
TEMPLATE_ICONFIG_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME + ".config",
    "src", "com", "telus", "connector", TEMPLATE_NAME, "ITemplateConfigurationComponent.java.txt"
)
TEMPLATE_CONFIG_JAVA = os.path.join(
    TEMPLATECONNECTORDIR, "com.telus.connector." + TEMPLATE_NAME + ".config",
    "src", "com", "telus", "connector", TEMPLATE_NAME, "TemplateConfigurationComponent.java.txt"
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
        raise ValueError(f"JSON definition file is invalid: {e}")

    if "projectname" not in data:
        raise ValueError("Missing required field: 'projectname'")
    if "connectors" not in data or not data["connectors"]:
        raise ValueError("Missing or empty required field: 'connectors'")

    for connector in data["connectors"]:
        for field in ["connectorid", "inputClass", "entityClass", "dataRecordClass", "apiPath", "httpMethod"]:
            if field not in connector:
                raise ValueError(f"Connector missing required field: '{field}'")

    return data


# ─────────────────────────────────────────────
# 3. COPY TEMPLATES
# ─────────────────────────────────────────────

def copy_templates(projectname: str):
    """Copy all template directories recursively to their target locations."""
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
    """Edit .project, pom.xml, and MANIFEST.MF in the config project directory.
    Also strips any pre-existing Service-Component entries from MANIFEST.MF
    (copied from the template) before the generated ones are appended later."""
    import re as _re

    config_dir    = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    manifest_path = os.path.join(config_dir, r"META-INF\MANIFEST.MF")

    _replace_in_file(os.path.join(config_dir, ".project"), "svcqualification", projectname)
    _replace_in_file(os.path.join(config_dir, "pom.xml"),  "svcqualification", projectname)
    _replace_in_file(manifest_path,                        "svcqualification", projectname)

    # Remove any pre-existing Service-Component: lines (and preceding blank lines)
    # that were copied from the template, so only the generated ones remain.
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            content = f.read()

        content = _re.sub(
            r'\n[\t ]*\nService-Component:[^\n]*(\n[ \t]+[^\n]*)*',
            '',
            content
        )
        content = _re.sub(
            r'\nService-Component:[^\n]*(\n[ \t]+[^\n]*)*',
            '',
            content
        )

        with open(manifest_path, "w") as f:
            f.write(content)
        print(f"  Cleaned Service-Component entries from: {manifest_path}")


# ─────────────────────────────────────────────
# 4b. EDIT BUILD FILES
# ─────────────────────────────────────────────

def edit_build_files(projectname: str):
    """Edit .project and pom.xml in each build project subdirectory.
    Also edits category.xml in the p2 directory and feature.xml in the
    feature directory, replacing 'svcqualification' with <projectname>."""
    build_suffixes = [
        "api.esa",
        "build",
        "config.esa",
        "esa",
        "feature",
        "p2",
    ]
    for suffix in build_suffixes:
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

    # Edit category.xml in the p2 directory
    category_xml = os.path.join(BUILDDIR, f"com.telus.connector.{projectname}.p2",
                                "category.xml")
    if os.path.exists(category_xml):
        _replace_in_file(category_xml, "svcqualification", projectname)
    else:
        print(f"[WARN] category.xml not found, skipping: {category_xml}")

    # Edit feature.xml in the feature directory
    feature_xml = os.path.join(BUILDDIR, f"com.telus.connector.{projectname}.feature",
                               "feature.xml")
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
    """Edit .project, pom.xml, MANIFEST.MF, and Constants.java in the
    implementation project, then rename the src package folder."""
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

    # Edit Constants.java in the renamed package folder
    constants_file = os.path.join(new_pkg, "Constants.java")
    if os.path.exists(constants_file):
        _replace_in_file(constants_file, "svcqualification", projectname)
    else:
        print(f"  [WARN] Constants.java not found, skipping: {constants_file}")

# ─────────────────────────────────────────────
# 7. GENERATE CONFIG FILES PER CONNECTOR
# ─────────────────────────────────────────────

def generate_config_per_connector(projectname: str, connectors: list):
    """Generate OSGI-INF xml, ConfigComponent java files, and update MANIFEST.MF.
    Also deletes the ITemplateConfigurationComponent.java.txt and
    TemplateConfigurationComponent.java.txt template files from src_dir after use.
    """
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

    # Delete the copied template .txt files — they have been consumed above
    for txt_name in ["ITemplateConfigurationComponent.java.txt",
                     "TemplateConfigurationComponent.java.txt"]:
        txt_path = os.path.join(delete_dir, txt_name)
        if os.path.exists(txt_path):
            os.remove(txt_path)
            print(f"  Deleted template file: {txt_path}")
        else:
            print(f"  [WARN] Template file not found for deletion: {txt_path}")
    # remove delete_dir
    os.rmdir(delete_dir)

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
    delete_dir = os.path.join(api_dir, "src", "com", "telus", "connector", "svcqualification")

    os.makedirs(osgi_inf_dir, exist_ok=True)
    _write_connectors_xml(connectors_xml, projectname, connectors)

    # Proper nested path: src\com\telus\connector\<projectname>\api\datatypes
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

        # --- Read & convert requestExample -> IDL fields ---
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

        # --- Read & convert responseExample -> IDL fields ---
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

        # Write the Types IDL file
        types_path = os.path.join(datatypes_dir, f"{cid}Types.model")
        _write_types_idl(types_path, projectname, cid,
                         request_fields, entity_fields,
                         request_structs, entity_structs)


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
    After all connectors are processed, deletes the copied template .java.txt files
    from the impl project src directories.
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
        request_stem  = os.path.splitext(request_example_fname)[0]  if request_example_fname  else None
        response_stem = os.path.splitext(response_example_fname)[0] if response_example_fname else None

        # --- call: generated from TemplateConnector.java.txt ---
        call_dir = os.path.join(src_base, "call")
        os.makedirs(call_dir, exist_ok=True)
        _write_connector_java(
            path         = os.path.join(call_dir, f"{cid}Connector.java"),
            projectname  = projectname,
            connectorid  = cid,
            http_method  = http_method,
            request_stem = request_stem
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

    # ── Delete copied template .java.txt files after all connectors are processed ──
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
        edit_build_files(projectname)
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


def _infer_fields_from_list(items: list, indent: int,
                            top_level_structs: list) -> str:
    """
    Infer IDL fields from a list of JSON objects by scanning ALL elements,
    not just the first. Nested struct definitions are collected into
    top_level_structs (not inlined).
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


def _json_to_idl_fields(data, indent: int = 1,
                        top_level_structs: list = None) -> str:
    """
    Recursively convert a parsed JSON object (dict or list) into IDL field
    declarations. Nested struct definitions are collected into top_level_structs
    and emitted as separate top-level structs, not inlined.
    """
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
    """
    Map a single JSON primitive or list-of-primitives value to a tuple of
    (idl_type_string, comment_string).
    """
    if isinstance(value, bool):
        return ("bool", "")
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
            return ("string[]", "// TODO: verify data type - empty array in sample")
        first = value[0]
        if isinstance(first, bool):
            return ("bool[]", "")
        elif isinstance(first, int):
            return ("long[]", "")
        elif isinstance(first, float):
            return ("double[]", "")
        elif isinstance(first, str):
            if _is_date_string(first):
                return ("date[]", "")
            return ("string[]", "")
        else:
            return ("string[]", "// TODO: verify data type - empty array in sample")
    else:
        return ("string", "")


def _write_types_idl(path: str, projectname: str, connectorid: str,
                     request_fields: str, entity_fields: str,
                     request_structs: list = None,
                     entity_structs: list = None):
    """
    Generate the connectorid Types.model IDL file in the API datatypes package.
    Nested struct definitions are emitted as separate top-level structs.
    The entity field inside DataRecord is named 'entityy' to avoid keyword clash.
    """
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
        f"struct {connectorid}Entity {{{entity_body}}}\n"
        f"{extra_block}\n"
        f"\n"
        f"struct {connectorid}DataRecord : AbstractDataRecord {{\n"
        f"\t{connectorid}Entity entityy\n"
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
        f'  <property name="target" value="com.telus.connector.{projectname}.{connectorid}"/>\n'
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
    """Generate I<connectorid>ConfigurationComponent.java
    from ITemplateConfigurationComponent.java.txt.
    Token replacements:
      <projectname>  → projectname
      <connectorid>  → connectorid
    """
    if not os.path.exists(TEMPLATE_ICONFIG_JAVA):
        raise FileNotFoundError(
            f"ITemplateConfigurationComponent.java.txt not found at: {TEMPLATE_ICONFIG_JAVA}"
        )

    with open(TEMPLATE_ICONFIG_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>",  connectorid)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated interface config: {path}")

def _write_impl_config(path: str, projectname: str, connectorid: str):
    """Generate <connectorid>ConfigurationComponent.java
    from TemplateConfigurationComponent.java.txt.
    Token replacements:
      <projectname>  → projectname
      <connectorid>  → connectorid
    """
    if not os.path.exists(TEMPLATE_CONFIG_JAVA):
        raise FileNotFoundError(
            f"TemplateConfigurationComponent.java.txt not found at: {TEMPLATE_CONFIG_JAVA}"
        )

    with open(TEMPLATE_CONFIG_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>",  connectorid)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated impl config: {path}")

def _append_service_components(manifest_path, osgi_files):
    """Append OSGI-INF/<filename> entries to Service-Component in MANIFEST.MF.
    Each entry is prefaced with 'OSGI-INF/' so the result is e.g.:
      Service-Component: OSGI-INF/com.telus.connector.inventory.tmf.CreateInventoryItem.xml
    """
    entries = ",\n ".join([f"OSGI-INF/{os.path.basename(f)}" for f in osgi_files])
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


def _write_connector_java(path: str, projectname: str, connectorid: str,
                          http_method: str, request_stem: str = None):
    """Generate Connector.java from TemplateConnector.java.txt. Token replacements:
      <projectname>    → projectname
      <connectorid>    → connectorid
      <requestExample> → request_stem (stem of requestExample filename,
                         or connectorid if None/absent)
    """
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

    # Safe fallback for <requestExample> if no requestExample provided
    req_stem = request_stem if request_stem else connectorid

    content = "".join(output_lines)
    content = content.replace("<projectname>",    projectname)
    content = content.replace("<connectorid>",    connectorid)
    content = content.replace("<requestExample>", req_stem)

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
      list of objects   -> List<SingularClassNamePojo>  (generates SingularClassNamePojo.java)
      list (other)      -> List<String>
      dict              -> ClassNamePojo  (generates ClassNamePojo.java)
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
                java_type     = f"List<{singular_name}Pojo>"
                # Collect all keys across all elements (best non-null per key)
                merged = {}
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if k not in merged or merged[k] is None:
                                merged[k] = v
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
            class_name  = f"{cap_key}Pojo"
            java_type   = f"{cap_key}Pojo"
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
    """
    model_dir      = os.path.dirname(path)
    nested_classes = []
    pojo_fields    = ""

    if data is not None:
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

    # Build import block
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


def _json_to_conversion_logic(json_path: str, source_var: str = "pojo") -> tuple:
    """
    Read a JSON example file and generate complete one-to-one mapping code,
    including private helper methods for all nested objects and lists of objects.

    Returns a tuple: (top_level_body: str, helpers: str, nested_api_types: list)
      - top_level_body  : the rv.setXxx(...) lines only — injected into the TODO
                          marker inside the method body. The template already
                          provides 'return rv;' and the closing '}'.
      - helpers         : private convertToXxx() methods — injected before the
                          class closing '}'.
      - nested_api_types: struct names needing:
                          import com.telus.connector.<projectname>.api.datatypes.<Name>;
    If the file is missing/empty/unparseable, returns ("", "", []).
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

    helper_methods   = {}  # struct_name -> method_source_string (ordered, deduped)
    nested_api_types = []  # struct names that need api.datatypes imports

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
        helper_methods[struct_name] = ""  # reserve slot to prevent infinite recursion
        if struct_name not in nested_api_types:
            nested_api_types.append(struct_name)  # track for import generation
        inner_body = _map_fields(obj, "pojo")
        method = (
            f"\tprivate {struct_name} convertTo{struct_name}({pojo_class} pojo) {{\n"
            f"\t\tif (pojo == null) return null;\n"
            f"\t\t{struct_name} rv = {struct_name}.create();\n"  # use .create() not new
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
    """
    Generate <connectorid>Converter.java from TemplateConverter.java.txt.

    Processing steps:
      1. Read template (UTF-8, BOM-safe).
      2. Process '// ConnectorGenerator: if <requestExample> != null' block:
           - If request_example_stem is present  → keep body, strip directive lines.
           - If request_example_stem is absent    → strip entire block including body.
      3. Apply token replacements:
           <projectname>     → projectname
           <connectorid>     → connectorid
           <requestExample>  → request_example_stem (or connectorid if None)
           <responseExample> → response_example_stem
      4. Replace 1st TODO marker with entity body lines (from responseExample).
      5. Replace 2nd TODO marker with pojo body lines (from requestExample).
      6. Inject helper methods (convertToXxx) before the class closing '}'.
      7. Inject missing api.datatypes imports after the last existing import line.
      8. Write output file (UTF-8).
    """
    import re

    if not os.path.exists(TEMPLATE_CONVERTER_JAVA):
        raise FileNotFoundError(
            f"TemplateConverter.java.txt not found at: {TEMPLATE_CONVERTER_JAVA}"
        )

    with open(TEMPLATE_CONVERTER_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # ── Step 2: process '// ConnectorGenerator: if <requestExample> != null' block ──
    re_cg_if    = re.compile(r'[ \t]*//\s*ConnectorGenerator:\s*if\s+<requestExample>\s*!=\s*null[ \t]*\r?\n')
    re_cg_endif = re.compile(r'[ \t]*//\s*ConnectorGenerator:\s*end\s+if[ \t]*\r?\n?')

    if_match    = re_cg_if.search(content)
    endif_match = re_cg_endif.search(content)

    if if_match and endif_match and if_match.start() < endif_match.start():
        block_start = if_match.start()
        block_end   = endif_match.end()
        block_body  = content[if_match.end():endif_match.start()]  # lines between directives

        if request_example_stem:
            # Keep the body, strip only the directive lines
            content = content[:block_start] + block_body + content[block_end:]
        else:
            # Strip the entire block including body
            content = content[:block_start] + content[block_end:]

    # ── Step 3: token replacements ──
    req_stem  = request_example_stem  if request_example_stem  else connectorid
    resp_stem = response_example_stem if response_example_stem else connectorid

    content = content.replace("<projectname>",     projectname)
    content = content.replace("<connectorid>",     connectorid)
    content = content.replace("<requestExample>",  req_stem)
    content = content.replace("<responseExample>", resp_stem)

    todo_marker   = "// TODO: implement the conversion logic here"
    all_api_types = []

    # ── Step 4: 1st TODO — entity body lines from responseExample ──
    entity_body, entity_helpers, entity_api_types = _json_to_conversion_logic(
        resp_json_path, source_var="pojo"
    )
    all_api_types.extend(entity_api_types)

    if entity_body:
        content = content.replace(todo_marker, entity_body, 1)
        print(f"  [Converter] Injected entity conversion logic "
              f"({len(entity_body.splitlines())} lines) from responseExample")
    else:
        print(f"  [Converter] No responseExample JSON — 1st TODO retained")

    # ── Step 5: 2nd TODO — pojo body lines from requestExample ──
    pojo_body, pojo_helpers, pojo_api_types = _json_to_conversion_logic(
        req_json_path, source_var="request"
    )
    all_api_types.extend(pojo_api_types)

    if pojo_body:
        content = content.replace(todo_marker, pojo_body, 1)
        print(f"  [Converter] Injected pojo conversion logic "
              f"({len(pojo_body.splitlines())} lines) from requestExample")
    else:
        print(f"  [Converter] No requestExample JSON — 2nd TODO retained")

    # ── Step 6: inject helper methods before the class's final closing '}' ──
    all_helpers = "\n\n".join(h for h in [entity_helpers, pojo_helpers] if h)
    if all_helpers:
        last_brace_idx = content.rfind("\n}")
        if last_brace_idx != -1:
            content = (content[:last_brace_idx]
                       + "\n\n"
                       + all_helpers
                       + content[last_brace_idx:])

    # ── Step 7: inject api.datatypes imports for nested struct types ──
    if all_api_types:
        import_lines = "\n".join(
            f"import com.telus.connector.{projectname}.api.datatypes.{t};"
            for t in all_api_types
        )
        # Insert after the last "import ...;" line in the file
        last_import_match = None
        for m in re.finditer(r'^import .*;', content, re.MULTILINE):
            last_import_match = m
        if last_import_match:
            insert_pos = last_import_match.end()
            content = content[:insert_pos] + "\n" + import_lines + content[insert_pos:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Converter java: {path}")


if __name__ == "__main__":
    main()