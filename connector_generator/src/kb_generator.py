import os
import shutil

try:
    from .settings import CALLDIR, TEMPLATEKBCALLDIR, TEMPLATE_NAME, QADIR, TEMPLDATEKBQADIR
except ImportError:
    from settings import CALLDIR, TEMPLATEKBCALLDIR, TEMPLATE_NAME, QADIR, TEMPLDATEKBQADIR


# ─────────────────────────────────────────────────────────────────────────────
# da/call  —  one .sfcx per connector
# ─────────────────────────────────────────────────────────────────────────────

_TEMPLATE_FILENAME = "GetSvcQualification.sfcx"


def generate_kb_call_sfcx_per_connector(projectname: str, connectors: list):
    """Generate one call-model .sfcx file per connector from the template."""
    call_project_dir = os.path.join(CALLDIR, projectname)
    os.makedirs(call_project_dir, exist_ok=True)

    template_path = _resolve_template_path(call_project_dir)
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    generated_paths = []
    for connector in connectors:
        connector_id = connector["connectorid"]
        input_class = connector["inputClass"]
        data_record_class = connector["dataRecordClass"]

        rendered = _render_sfcx_template(
            template,
            projectname=projectname,
            connectorid=connector_id,
            input_class=input_class,
            data_record_class=data_record_class,
        )

        out_path = os.path.join(call_project_dir, f"{connector_id}.sfcx")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        generated_paths.append(out_path)
        print(f"Generated KB call model: {out_path}")

    _cleanup_legacy_template(call_project_dir, generated_paths)


def _resolve_template_path(call_project_dir: str) -> str:
    copied_template = os.path.join(call_project_dir, _TEMPLATE_FILENAME)
    if os.path.exists(copied_template):
        return copied_template

    source_template = os.path.join(TEMPLATEKBCALLDIR, TEMPLATE_NAME, _TEMPLATE_FILENAME)
    if os.path.exists(source_template):
        return source_template

    raise FileNotFoundError(
        f"SFCX template not found in '{copied_template}' or '{source_template}'"
    )


def _render_sfcx_template(
    template: str,
    projectname: str,
    connectorid: str,
    input_class: str,
    data_record_class: str,
) -> str:
    """Apply connector-specific replacements to the template SFCX content."""
    rendered = template
    rendered = rendered.replace("com.telus.connector.svcqualification", f"com.telus.connector.{projectname}")
    rendered = rendered.replace("GetSvcQualificationDataRecord", data_record_class)
    rendered = rendered.replace("GetSvcQualificationRequest", input_class)
    rendered = rendered.replace("GetSvcQualification", connectorid)
    # Fix stale display names that don't follow the GetSvcQualification pattern (issues 1 & 2)
    rendered = rendered.replace("SyncCustomerTVSubscriptionsList", connectorid)
    rendered = rendered.replace("SyncCustomerTvSubscriptionsList", connectorid)
    return rendered


def _cleanup_legacy_template(call_project_dir: str, generated_paths: list):
    legacy_template = os.path.join(call_project_dir, _TEMPLATE_FILENAME)
    generated_names = {os.path.basename(p) for p in generated_paths}
    if os.path.exists(legacy_template) and _TEMPLATE_FILENAME not in generated_names:
        os.remove(legacy_template)
        print(f"Deleted legacy KB call template: {legacy_template}")


# ─────────────────────────────────────────────────────────────────────────────
# qa/da  —  per-connector sfcx + sfrm2 subfolders + project-level model/content
# ─────────────────────────────────────────────────────────────────────────────

_QA_SFCX_TEMPLATE_NAME  = "QAIssueGetSvcQualification.sfcx"
_QA_SFRM2_TEMPLATE_NAME = "QAIssueGetSvcQualification.sfrm2"
_QA_LEGACY_SUBFOLDER    = "getsvcqualification"
_QA_LEGACY_MODEL        = "QAIssuesSvcQualification.model"
_QA_LEGACY_CONTENT_EN   = "QAIssuesSvcQualification_en_CA.content"
_QA_LEGACY_CONTENT_FR   = "QAIssuesSvcQualification_fr_CA.content"


def generate_kb_qa_per_connector(projectname: str, connectors: list):
    """
    Generate QA/DA artifacts for all connectors in a project.

    Produces, under QADIR/<projectname>/:
      <connectorid.lower()>/
          QAIssue<connectorid>.sfcx    — interactive QA process flow
          QAIssue<connectorid>.sfrm2   — input form stub
      QAIssues<Projectname>.model      — QA issue registry (all connectors)
      QAIssues<Projectname>_en_CA.content
      QAIssues<Projectname>_fr_CA.content
    """
    qa_project_dir = os.path.join(QADIR, projectname)
    os.makedirs(qa_project_dir, exist_ok=True)

    sfcx_template  = _read_qa_template(qa_project_dir, _QA_LEGACY_SUBFOLDER, _QA_SFCX_TEMPLATE_NAME)
    sfrm2_template = _read_qa_template(qa_project_dir, _QA_LEGACY_SUBFOLDER, _QA_SFRM2_TEMPLATE_NAME)

    for connector in connectors:
        _generate_qa_connector_files(
            qa_project_dir, projectname, connector, sfcx_template, sfrm2_template
        )

    _generate_qa_model_file(qa_project_dir, projectname, connectors)
    _generate_qa_content_file(qa_project_dir, projectname, connectors, "en_CA")
    _generate_qa_content_file(qa_project_dir, projectname, connectors, "fr_CA")

    _cleanup_legacy_qa_templates(qa_project_dir)


# ── internal helpers ──────────────────────────────────────────────────────────

def _read_qa_template(qa_project_dir: str, subfolder: str, filename: str) -> str:
    """Read a QA template from the already-copied output dir, falling back to source."""
    copied = os.path.join(qa_project_dir, subfolder, filename)
    if os.path.exists(copied):
        with open(copied, "r", encoding="utf-8") as f:
            return f.read()
    source = os.path.join(TEMPLDATEKBQADIR, TEMPLATE_NAME, subfolder, filename)
    if os.path.exists(source):
        with open(source, "r", encoding="utf-8") as f:
            return f.read()
    raise FileNotFoundError(
        f"QA template not found at '{copied}' or '{source}'"
    )


def _generate_qa_connector_files(
    qa_project_dir: str,
    projectname: str,
    connector: dict,
    sfcx_template: str,
    sfrm2_template: str,
):
    cid         = connector["connectorid"]
    input_class = connector["inputClass"]
    cid_lower   = cid.lower()

    connector_dir = os.path.join(qa_project_dir, cid_lower)
    os.makedirs(connector_dir, exist_ok=True)

    sfcx_path = os.path.join(connector_dir, f"QAIssue{cid}.sfcx")
    with open(sfcx_path, "w", encoding="utf-8") as f:
        f.write(_render_qa_sfcx(sfcx_template, projectname, cid, input_class))
    print(f"  Generated QA call model: {sfcx_path}")

    sfrm2_path = os.path.join(connector_dir, f"QAIssue{cid}.sfrm2")
    with open(sfrm2_path, "w", encoding="utf-8") as f:
        f.write(_render_qa_sfrm2(sfrm2_template, projectname, cid))
    print(f"  Generated QA input form: {sfrm2_path}")


def _render_qa_sfcx(
    template: str, projectname: str, connectorid: str, input_class: str
) -> str:
    """
    Apply ordered replacements to the QA sfcx template.

    Replacement order is significant:
      1. Full qualified package prefixes first (most specific)
      2. Class names that contain shorter names (e.g. Request before bare name)
      3. Composite names before their substrings
      4. Lowercase package segment (no case collision risk)
      5. Bare connector name last
    """
    rendered = template
    rendered = rendered.replace(
        "com.telus.connector.svcqualification",
        f"com.telus.connector.{projectname}",
    )
    rendered = rendered.replace("qa.da.svcqualification", f"qa.da.{projectname}")
    rendered = rendered.replace("GetSvcQualificationRequest", input_class)
    rendered = rendered.replace("QAIssueGetSvcQualification", f"QAIssue{connectorid}")
    rendered = rendered.replace("getsvcqualification", connectorid.lower())
    rendered = rendered.replace("GetSvcQualification", connectorid)
    # Fix stale display names that don't follow the GetSvcQualification pattern (issues 3 & 4)
    rendered = rendered.replace("QAIssueSTBDiagnosticQuery", f"QAIssue{connectorid}")
    rendered = rendered.replace("StbDiagnosticsQuery", connectorid)
    return rendered


def _render_qa_sfrm2(template: str, projectname: str, connectorid: str) -> str:
    """
    Apply ordered replacements to the QA sfrm2 template.

    Form input fields (e.g. lpdsId) are kept as stubs for the first pass;
    the developer should update them to match the actual inputClass fields.
    """
    rendered = template
    rendered = rendered.replace("qa.da.svcqualification", f"qa.da.{projectname}")
    rendered = rendered.replace("QAIssueGetSvcQualification", f"QAIssue{connectorid}")
    rendered = rendered.replace("getsvcqualification", connectorid.lower())
    rendered = rendered.replace("GetSvcQualification", connectorid)
    # Fix issue 5: replace stale/misspelled form title
    rendered = rendered.replace("Get Servcice Qualification", connectorid)
    return rendered


def _projectname_to_classname(projectname: str) -> str:
    """Capitalise the first letter of projectname for use in file/class names.

    Examples:
        'svcqualification'  -> 'SvcQualification'
        'inventory.tmf'     -> 'Inventory.tmf'
    """
    return projectname[0].upper() + projectname[1:] if projectname else projectname


def _generate_qa_model_file(
    qa_project_dir: str, projectname: str, connectors: list
):
    """Generate the project-level QA issue registry (.model)."""
    classname = _projectname_to_classname(projectname)
    lines = [f"package qa.da.{projectname}", ""]
    for connector in connectors:
        cid = connector["connectorid"]
        lines += [
            f"issue QAIssue{cid} {{",
            f"\tprocess qa.da.{projectname}.{cid.lower()}.QAIssue{cid}",
            "}",
            "",
        ]
    model_path = os.path.join(qa_project_dir, f"QAIssues{classname}.model")
    with open(model_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated QA model: {model_path}")


def _generate_qa_content_file(
    qa_project_dir: str, projectname: str, connectors: list, locale: str
):
    """Generate a localisation .content file for all QA issues in the project."""
    classname  = _projectname_to_classname(projectname)
    is_english = locale == "en_CA"
    lines = []
    for connector in connectors:
        cid   = connector["connectorid"]
        title = connector.get("connectordescription", "") if is_english else ""
        lines += [
            f"qa.da.{projectname}.QAIssue{cid} [",
            f'\ttitle = "{title}"',
            '\tdescription = ""',
            "]",
            "",
        ]
    content_path = os.path.join(
        qa_project_dir, f"QAIssues{classname}_{locale}.content"
    )
    with open(content_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated QA content ({locale}): {content_path}")


def _cleanup_legacy_qa_templates(qa_project_dir: str):
    """Remove legacy template artifacts copied verbatim from the template tree."""
    for legacy_file in [
        _QA_LEGACY_MODEL,
        _QA_LEGACY_CONTENT_EN,
        _QA_LEGACY_CONTENT_FR,
    ]:
        path = os.path.join(qa_project_dir, legacy_file)
        if os.path.exists(path):
            os.remove(path)
            print(f"  Deleted legacy QA artifact: {path}")

    legacy_sub = os.path.join(qa_project_dir, _QA_LEGACY_SUBFOLDER)
    if os.path.exists(legacy_sub):
        shutil.rmtree(legacy_sub)
        print(f"  Deleted legacy QA subfolder: {legacy_sub}")

