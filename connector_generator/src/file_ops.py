import os


def projectname_to_path(projectname: str) -> str:
    """Convert dots in projectname to OS path separators."""
    return projectname.replace(".", os.sep)


def replace_in_file(filepath: str, old: str, new: str):
    """Replace all occurrences of old with new in a file."""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def append_service_components(manifest_path: str, osgi_files: list):
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

