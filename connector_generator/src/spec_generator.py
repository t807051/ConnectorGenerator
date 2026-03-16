import datetime
import json
import os
import re
from typing import Callable

try:
    from .settings import BASEDIR, TEMPLATE_SPEC_MD
except ImportError:
    from settings import BASEDIR, TEMPLATE_SPEC_MD


def generate_spec_doc(
    projectname: str,
    connectors: list,
    definition: dict,
    definition_file: str,
    json_to_idl_fields: Callable,
):
    """Generate the Markdown connector specification document from template directives."""
    if not os.path.exists(TEMPLATE_SPEC_MD):
        print(f"[WARN] ConnectorSpecTemplate not found, skipping spec doc: {TEMPLATE_SPEC_MD}")
        return

    with open(TEMPLATE_SPEC_MD, "r", encoding="utf-8-sig") as f:
        template = f.read()

    definition_dir = os.path.dirname(os.path.abspath(definition_file))
    today = datetime.date.today().strftime("%Y-%m-%d")
    projectdesc = definition.get("projectdescription", "")
    hosts = definition.get("hosts", [])

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

    def _json_block(fname):
        raw = _raw_file(fname)
        return f"```json\n{raw}\n```" if raw else "_No example provided._"

    def _idl_block_for_spec(fname, struct_name):
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
        fields = json_to_idl_fields(data, indent=1, top_level_structs=nested_structs)

        parent_block = f"struct {struct_name} {{\n{fields}\n}}"
        all_blocks = [parent_block] + nested_structs

        code_lines = ["```"]
        for i, block in enumerate(all_blocks):
            code_lines.append(block)
            if i < len(all_blocks) - 1:
                code_lines.append("")
        code_lines.append("```")
        result = "\n".join(code_lines)

        warning_lines = []
        for block in all_blocks:
            struct_match = re.match(r"struct (\w+)", block)
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

    def _nodemanager_block(host, connector):
        hostname = host.get("hostname", "")
        auth = host.get("authentication", "").lower()
        cid = connector["connectorid"]
        api_path = connector.get("apiPath", "")
        service_id = f"com.telus.connector.{projectname}.{cid}.rest"
        endpoint = f"{hostname}/{api_path.lstrip('/')}"

        if auth == "basic":
            return (
                f'    <service serviceId="{service_id}">\n'
                f'        <property name="endpoint" type="string">{endpoint}</property>\n'
                f'        <property name="password" type="string">'
                f"Oa0rDOv9oP+P14jitaDWgf3/woLmsq14+oNU8NEORxN+hv2+2six76JPm1WvbGzwSJ1V6kOI1E5SH0+23PsJkw==</property>\n"
                f'        <property name="authenticationType" type="string">basic</property>\n'
                f'        <property name="timeout" type="int">4000</property>\n'
                f'        <property name="username" type="string">APP_SOLVATIO</property>\n'
                f"    </service>"
            )
        return (
            f'    <service serviceId="{service_id}">\n'
            f'        <property name="endpoint" type="string">{endpoint}</property>\n'
            f'        <property name="authenticationType" type="string">kong</property>\n'
            f'        <property name="timeout" type="int">4000</property>\n'
            f"    </service>"
        )

    template = template.replace("//SpecGenerator: insert today's date in yyyy-mm-dd format", today)
    template = template.replace(
        "// SpecGenerator: Insert <projectdescription>",
        projectdesc if projectdesc else "_No description provided._",
    )

    host_rows = (
        "\n".join(
            f"| {h.get('env', '')} | {h.get('hostname', '')} | {h.get('authentication', '')} |"
            for h in hosts
        )
        if hosts
        else "| | | |"
    )

    template = re.sub(
        r"\|[^\n]*SpecGenerator: Insert <hosts\.env>[^\n]*\|[^\n]*\n?",
        host_rows + "\n",
        template,
    )

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
        r"// SpecGenerator: define nodemanager definition.*?// SpecGenerator: Insert pagebreak",
        nodemanager_output + "\n\n// SpecGenerator: Insert pagebreak",
        template,
        count=1,
        flags=re.DOTALL,
    )

    def_for_pattern = re.compile(
        r"// SpecGenerator: for each <connectorid>\s*\n"
        r"(.*?)"
        r"// SpecGenerator: end for\b(?! loop)",
        re.DOTALL,
    )

    def _expand_definitions(match):
        body_template = match.group(1)
        blocks = []
        for connector in connectors:
            cid = connector["connectorid"]
            connectordesc = connector.get("connectordescription", "")
            req_fname = connector.get("requestExample")
            resp_fname = connector.get("responseExample")

            body = body_template
            body = body.replace(r"\<connectorid\>", cid)
            body = body.replace(r"\<projectname\>", projectname)

            body = body.replace(
                "// SpecGenerator: Insert <connectordescription>",
                connectordesc if connectordesc else "_No description provided._",
            )

            body = re.sub(
                r"// SpecGenerator: Insert \\<requestExample\\>Request object definition from IDL",
                _idl_block_for_spec(req_fname, f"{cid}Request"),
                body,
            )
            body = re.sub(
                r"// SpecGenerator: Insert \\<responseExample\\>Entity object definition from IDL",
                _idl_block_for_spec(resp_fname, f"{cid}Entity"),
                body,
            )

            blocks.append(body.rstrip())

        return "\n\n".join(blocks) + "\n"

    template = def_for_pattern.sub(_expand_definitions, template)

    appendix_for_pattern = re.compile(
        r"// SpecGenerator: for each <connectorid>\s*\n"
        r"(.*?)"
        r"// SpecGenerator: end for loop",
        re.DOTALL,
    )

    def _expand_appendix(match):
        body_template = match.group(1)
        blocks = []
        for connector in connectors:
            cid = connector["connectorid"]
            api_path = connector.get("apiPath", "")
            req_fname = connector.get("requestExample")
            resp_fname = connector.get("responseExample")

            body = body_template
            body = body.replace("<connectorid>", cid)
            body = body.replace("<projectname>", projectname)
            body = body.replace("<apiPath>", api_path)

            body = body.replace(
                "// SpecGenerator: Insert <requestExample>", _json_block(req_fname)
            )
            body = body.replace(
                "// SpecGenerator: Insert <responseExample>", _json_block(resp_fname)
            )

            body = re.sub(r"// SpecGenerator: Insert pagebreak\s*", "\n---\n\n", body)
            blocks.append(body.rstrip())

        return "\n\n".join(blocks) + "\n"

    template = appendix_for_pattern.sub(_expand_appendix, template)

    def _to_anchor(text):
        anchor = text.lower().strip()
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        anchor = re.sub(r"\s+", "-", anchor)
        return anchor

    toc_lines = []
    for line in template.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{text}](#{_to_anchor(text)})")

    toc_output = "\n".join(toc_lines) if toc_lines else "_No sections found._"
    template = template.replace("// SpecGenerator: Insert links to document sections", toc_output)

    template = re.sub(r"// SpecGenerator: Insert pagebreak\s*", "\n---\n\n", template)

    docs_dir = os.path.join(BASEDIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, f"{projectname}-connector-spec.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"Generated spec doc: {out_path}")

