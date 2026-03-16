import json
import os
import re

try:
    from .settings import (
        CONNECTORDIR,
        TEMPLATE_CONNECTOR_JAVA,
        TEMPLATE_CONVERTER_JAVA,
        TEMPLATE_EXCEPTION_JAVA,
        TEMPLATE_FACTORY_JAVA,
    )
    from .file_ops import projectname_to_path
except ImportError:
    from settings import (
        CONNECTORDIR,
        TEMPLATE_CONNECTOR_JAVA,
        TEMPLATE_CONVERTER_JAVA,
        TEMPLATE_EXCEPTION_JAVA,
        TEMPLATE_FACTORY_JAVA,
    )
    from file_ops import projectname_to_path


def generate_impl_per_connector(projectname: str, connectors: list, definition_file: str):
    """Generate Connector, POJO, Converter, Factory, and Exception java files per connector."""
    impl_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}")
    src_base = os.path.join(
        impl_dir, "src", "com", "telus", "connector", projectname_to_path(projectname)
    )
    definition_dir = os.path.dirname(os.path.abspath(definition_file))

    for connector in connectors:
        cid = connector["connectorid"]
        http_method = connector["httpMethod"]
        api_path = connector["apiPath"]
        request_example_fname = connector.get("requestExample")
        response_example_fname = connector.get("responseExample")

        request_stem = (
            os.path.splitext(request_example_fname)[0] if request_example_fname else None
        )
        response_stem = (
            os.path.splitext(response_example_fname)[0] if response_example_fname else None
        )

        call_dir = os.path.join(src_base, "call")
        os.makedirs(call_dir, exist_ok=True)
        _write_connector_java(
            path=os.path.join(call_dir, f"{cid}Connector.java"),
            projectname=projectname,
            connectorid=cid,
            http_method=http_method,
            request_stem=request_stem,
        )

        model_dir = os.path.join(src_base, "model")
        os.makedirs(model_dir, exist_ok=True)

        if request_example_fname:
            req_path = os.path.join(definition_dir, request_example_fname)
            _write_pojo_java(
                path=os.path.join(model_dir, f"{request_stem}Pojo.java"),
                projectname=projectname,
                class_name=f"{request_stem}Pojo",
                json_path=req_path,
                label="requestExample",
            )

        if response_example_fname:
            resp_path = os.path.join(definition_dir, response_example_fname)
            _write_pojo_java(
                path=os.path.join(model_dir, f"{response_stem}Pojo.java"),
                projectname=projectname,
                class_name=f"{response_stem}Pojo",
                json_path=resp_path,
                label="responseExample",
            )

        converter_dir = os.path.join(src_base, "converter")
        os.makedirs(converter_dir, exist_ok=True)

        if response_example_fname:
            resp_path = os.path.join(definition_dir, response_example_fname)
            req_path_for_conv = (
                os.path.join(definition_dir, request_example_fname)
                if request_example_fname
                else None
            )
            _write_converter_java(
                path=os.path.join(converter_dir, f"{cid}Converter.java"),
                projectname=projectname,
                connectorid=cid,
                request_example_stem=request_stem,
                response_example_stem=response_stem,
                resp_json_path=resp_path,
                req_json_path=req_path_for_conv,
            )
        else:
            _write_java_stub(
                os.path.join(converter_dir, f"{cid}Converter.java"),
                projectname,
                cid,
                "converter",
            )

        factories_dir = os.path.join(src_base, "factories")
        os.makedirs(factories_dir, exist_ok=True)
        _write_factory_java(
            path=os.path.join(factories_dir, f"{cid}Factory.java"),
            projectname=projectname,
            connectorid=cid,
            api_path=api_path,
        )

        exception_dir = os.path.join(src_base, "exception")
        os.makedirs(exception_dir, exist_ok=True)
        _write_exception_java(
            path=os.path.join(exception_dir, f"{cid}ConversionException.java"),
            projectname=projectname,
            connectorid=cid,
        )

    template_txt_files = [
        os.path.join(src_base, "call", "TemplateConnector.java.txt"),
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


def _write_java_stub(path, projectname, connectorid, role):
    class_name = {
        "call": f"{connectorid}Connector",
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


def _write_connector_java(path: str, projectname: str, connectorid: str, http_method: str, request_stem: str = None):
    if not os.path.exists(TEMPLATE_CONNECTOR_JAVA):
        raise FileNotFoundError(f"TemplateConnector.java.txt not found: {TEMPLATE_CONNECTOR_JAVA}")
    with open(TEMPLATE_CONNECTOR_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    method_upper = http_method.upper()
    lines = content.splitlines(keepends=True)
    out_lines = []
    skip = False
    for line in lines:
        if re.match(r"\s*// ConnectorGenerator: if <httpMethod> == (\w+)", line):
            m = re.match(r"\s*// ConnectorGenerator: if <httpMethod> == (\w+)", line)
            skip = m.group(1).upper() != method_upper
            continue
        if re.match(r"\s*// ConnectorGenerator: else if <httpMethod> == (\w+)", line):
            m = re.match(r"\s*// ConnectorGenerator: else if <httpMethod> == (\w+)", line)
            skip = m.group(1).upper() != method_upper
            continue
        if re.match(r"\s*// ConnectorGenerator: end if", line):
            skip = False
            continue
        if not skip:
            out_lines.append(line)
    content = "".join(out_lines)

    req_stem = request_stem if request_stem else connectorid
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    content = content.replace("<requestExample>", req_stem)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Connector java: {path}")


def _write_factory_java(path: str, projectname: str, connectorid: str, api_path: str):
    if not os.path.exists(TEMPLATE_FACTORY_JAVA):
        raise FileNotFoundError(f"TemplateFactory.java.txt not found: {TEMPLATE_FACTORY_JAVA}")
    with open(TEMPLATE_FACTORY_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    content = content.replace("<apiPath>", api_path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Factory java: {path}")


def _write_exception_java(path: str, projectname: str, connectorid: str):
    if not os.path.exists(TEMPLATE_EXCEPTION_JAVA):
        raise FileNotFoundError(f"TemplateException.java.txt not found: {TEMPLATE_EXCEPTION_JAVA}")
    with open(TEMPLATE_EXCEPTION_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Exception java: {path}")


def _write_pojo_java(path: str, projectname: str, class_name: str, json_path: str, label: str, data: dict = None):
    pojo_fields = ""
    nested_classes = []
    model_dir = os.path.dirname(path)

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
            print(f"  [WARN] {label} file not found or empty: {json_path}")

    import_lines = []
    if "Date" in pojo_fields:
        import_lines.append("import java.util.Date;")
    if "List<" in pojo_fields:
        import_lines.append("import java.util.List;")
    for nc in nested_classes:
        import_lines.append(f"import com.telus.connector.{projectname}.model.{nc}Pojo;")

    imports = ("\n".join(import_lines) + "\n\n") if import_lines else ""
    body = pojo_fields if pojo_fields else "\t// TODO: add fields"

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


def _json_to_pojo_fields(data: dict, projectname: str, model_dir: str, nested_classes: list) -> str:
    fields = []
    methods = []

    for key, value in data.items():
        cap_key = key[0].upper() + key[1:] if key else key
        comment = ""
        java_type = "String"

        if isinstance(value, list) and value and isinstance(value[0], dict):
            singular_name = _singularize(key).capitalize()
            class_name = f"{singular_name}Pojo"
            java_type = f"List<{class_name}>"
            merged = {}
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if k not in merged or merged[k] is None:
                            merged[k] = v
            nested_path = os.path.join(model_dir, f"{class_name}.java")
            _write_pojo_java(
                path=nested_path,
                projectname=projectname,
                class_name=class_name,
                json_path=None,
                label=f"nested list element for '{key}'",
                data=merged,
            )
            if singular_name not in nested_classes:
                nested_classes.append(singular_name)
        elif isinstance(value, list) and not value:
            java_type = "List<String>"
            comment = " // TODO: verify data type - empty array in sample"
        elif isinstance(value, list):
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
            class_name = f"{cap_key}Pojo"
            java_type = f"{cap_key}Pojo"
            nested_path = os.path.join(model_dir, f"{class_name}.java")
            _write_pojo_java(
                path=nested_path,
                projectname=projectname,
                class_name=class_name,
                json_path=None,
                label=f"nested object for '{key}'",
                data=value,
            )
            if cap_key not in nested_classes:
                nested_classes.append(cap_key)
        elif isinstance(value, bool):
            java_type = "boolean"
        elif isinstance(value, int):
            java_type = "long"
        elif isinstance(value, float):
            java_type = "double"
        elif isinstance(value, str):
            java_type = "Date" if _is_date_string(value) else "String"
        elif value is None:
            java_type = "String"
            comment = " // TODO: verify data type - null in sample"

        fields.append(f"\tprivate {java_type} {key};{comment}")
        methods.append(
            f"\tpublic {java_type} get{cap_key}() {{ return {key}; }}\n"
            f"\tpublic void set{cap_key}({java_type} {key}) {{ this.{key} = {key}; }}"
        )

    return "\n".join(fields) + "\n\n" + "\n\n".join(methods)


def _json_to_conversion_logic(json_path: str, source_var: str = "pojo") -> tuple:
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

    helper_methods = {}
    nested_api_types = []

    def _map_fields(obj: dict, src: str) -> str:
        lines = []
        for key, value in obj.items():
            cap_key = key[0].upper() + key[1:] if key else key
            if isinstance(value, dict):
                struct_name = cap_key
                pojo_class = f"{cap_key}Pojo"
                _ensure_helper(struct_name, pojo_class, value)
                lines.append(f"\t\trv.set{cap_key}(convertTo{struct_name}({src}.get{cap_key}()));")
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                singular = _singularize(key).capitalize()
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
    helpers_str = "\n\n".join(m for m in helper_methods.values() if m)
    return top_level_body, helpers_str, nested_api_types


def _write_converter_java(path: str, projectname: str, connectorid: str, request_example_stem: str, response_example_stem: str, resp_json_path: str, req_json_path: str):
    if not os.path.exists(TEMPLATE_CONVERTER_JAVA):
        raise FileNotFoundError(f"TemplateConverter.java.txt not found: {TEMPLATE_CONVERTER_JAVA}")
    with open(TEMPLATE_CONVERTER_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()

    if request_example_stem:
        content = re.sub(r"// ConnectorGenerator: if <requestExample> != null\n", "", content)
        content = re.sub(r"// ConnectorGenerator: end if\n", "", content)
    else:
        content = re.sub(
            r"// ConnectorGenerator: if <requestExample> != null\n.*?// ConnectorGenerator: end if\n",
            "",
            content,
            flags=re.DOTALL,
        )

    req_stem = request_example_stem if request_example_stem else connectorid
    resp_stem = response_example_stem if response_example_stem else connectorid
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    content = content.replace("<requestExample>", req_stem)
    content = content.replace("<responseExample>", resp_stem)

    todo_marker = "// TODO: implement the conversion logic here"

    entity_body, entity_helpers, entity_api_types = _json_to_conversion_logic(
        resp_json_path, source_var="pojo"
    )
    all_api_types = list(entity_api_types)

    if entity_body:
        content = content.replace(todo_marker, entity_body, 1)
        print(f"  [Converter] Injected entity conversion logic ({len(entity_body.splitlines())} lines)")
    else:
        print("  [Converter] No responseExample JSON - 1st TODO retained")

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
        print("  [Converter] No requestExample JSON - 2nd TODO retained")

    all_helpers = "\n\n".join(h for h in [entity_helpers, pojo_helpers] if h)
    if all_helpers:
        last_brace_idx = content.rfind("\n}")
        if last_brace_idx != -1:
            content = content[:last_brace_idx] + "\n\n" + all_helpers + content[last_brace_idx:]

    if all_api_types:
        import_lines = "\n".join(
            f"import com.telus.connector.{projectname}.api.datatypes.{t};" for t in all_api_types
        )
        last_import_match = None
        for m in re.finditer(r"^import .*;", content, re.MULTILINE):
            last_import_match = m
        if last_import_match:
            insert_pos = last_import_match.end()
            content = content[:insert_pos] + "\n" + import_lines + content[insert_pos:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated Converter java: {path}")


def _singularize(name: str) -> str:
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith(("sses", "xes", "ches", "shes")):
        return name[:-2]
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _is_date_string(value: str) -> bool:
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

