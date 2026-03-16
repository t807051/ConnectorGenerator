try:
    from .definition_loader import load_definition
    from .template_ops import (
        copy_templates,
        edit_api_files,
        edit_build_files,
        edit_config_files,
        edit_impl_files,
    )
    from .spec_generator import generate_spec_doc
    from .config_generator import generate_config_per_connector as _generate_config_per_connector
    from .kb_generator import (
        generate_kb_call_sfcx_per_connector as _generate_kb_call_sfcx_per_connector,
    )
    from .kb_generator import (
        generate_kb_qa_per_connector as _generate_kb_qa_per_connector,
    )
    from .api_generator import (
        generate_api_per_connector as _generate_api_per_connector,
        json_to_idl_fields as _api_json_to_idl_fields,
    )
    from .impl_generator import generate_impl_per_connector as _generate_impl_per_connector
except ImportError:
    from definition_loader import load_definition
    from template_ops import (
        copy_templates,
        edit_api_files,
        edit_build_files,
        edit_config_files,
        edit_impl_files,
    )
    from spec_generator import generate_spec_doc
    from config_generator import generate_config_per_connector as _generate_config_per_connector
    from kb_generator import (
        generate_kb_call_sfcx_per_connector as _generate_kb_call_sfcx_per_connector,
    )
    from kb_generator import (
        generate_kb_qa_per_connector as _generate_kb_qa_per_connector,
    )
    from api_generator import (
        generate_api_per_connector as _generate_api_per_connector,
        json_to_idl_fields as _api_json_to_idl_fields,
    )
    from impl_generator import generate_impl_per_connector as _generate_impl_per_connector


def generate_config_per_connector(projectname: str, connectors: list):
    """Compatibility wrapper delegating to config_generator.generate_config_per_connector."""
    return _generate_config_per_connector(projectname, connectors)


def generate_api_per_connector(projectname: str, connectors: list, definition_file: str):
    """Compatibility wrapper delegating to api_generator.generate_api_per_connector."""
    return _generate_api_per_connector(projectname, connectors, definition_file)


def generate_impl_per_connector(projectname: str, connectors: list, definition_file: str):
    """Compatibility wrapper delegating to impl_generator.generate_impl_per_connector."""
    return _generate_impl_per_connector(projectname, connectors, definition_file)


def generate_kb_call_sfcx_per_connector(projectname: str, connectors: list):
    """Compatibility wrapper delegating to kb_generator.generate_kb_call_sfcx_per_connector."""
    return _generate_kb_call_sfcx_per_connector(projectname, connectors)


def generate_kb_qa_per_connector(projectname: str, connectors: list):
    """Compatibility wrapper delegating to kb_generator.generate_kb_qa_per_connector."""
    return _generate_kb_qa_per_connector(projectname, connectors)


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
    connectors = definition["connectors"]

    print(f"\n=== Generating Connector Project: {projectname} ===\n")

    try:
        copy_templates(projectname)
        edit_config_files(projectname)
        edit_build_files(projectname)
        edit_api_files(projectname)
        edit_impl_files(projectname)
        generate_kb_call_sfcx_per_connector(projectname, connectors)
        generate_kb_qa_per_connector(projectname, connectors)
        generate_config_per_connector(projectname, connectors)
        generate_api_per_connector(projectname, connectors, json_file)
        generate_impl_per_connector(projectname, connectors, json_file)
        generate_spec_doc(
            projectname,
            connectors,
            definition,
            json_file,
            json_to_idl_fields=_api_json_to_idl_fields,
        )
    except Exception as e:
        print(f"\n[ERROR] Generation failed: {e}")
        sys.exit(1)

    print("\n=== Generation Complete ===")




if __name__ == "__main__":
    main()