import os
import re
import shutil

try:
    from .settings import *
    from .file_ops import projectname_to_path, replace_in_file
except ImportError:
    from settings import *
    from file_ops import projectname_to_path, replace_in_file


def copy_templates(projectname: str):
    """Copy all template directories recursively to their target locations."""
    copies = [
        (
            f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}",
            f"{CONNECTORDIR}\\com.telus.connector.{projectname}",
        ),
        (
            f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}.api",
            f"{CONNECTORDIR}\\com.telus.connector.{projectname}.api",
        ),
        (
            f"{TEMPLATECONNECTORDIR}\\com.telus.connector.{TEMPLATE_NAME}.config",
            f"{CONNECTORDIR}\\com.telus.connector.{projectname}.config",
        ),
        (
            f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.api.esa",
            f"{BUILDDIR}\\com.telus.connector.{projectname}.api.esa",
        ),
        (
            f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.build",
            f"{BUILDDIR}\\com.telus.connector.{projectname}.build",
        ),
        (
            f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.config.esa",
            f"{BUILDDIR}\\com.telus.connector.{projectname}.config.esa",
        ),
        (
            f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.esa",
            f"{BUILDDIR}\\com.telus.connector.{projectname}.esa",
        ),
        (
            f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.feature",
            f"{BUILDDIR}\\com.telus.connector.{projectname}.feature",
        ),
        (
            f"{TEMPLATEBUILDDIR}\\com.telus.connector.{TEMPLATE_NAME}.p2",
            f"{BUILDDIR}\\com.telus.connector.{projectname}.p2",
        ),
        (f"{TEMPLATEKBCALLDIR}\\{TEMPLATE_NAME}", f"{CALLDIR}\\{projectname}"),
        (f"{TEMPLDATEKBQADIR}\\{TEMPLATE_NAME}", f"{QADIR}\\{projectname}"),
    ]
    for src, dst in copies:
        shutil.copytree(src, dst)
        print(f"Copied: {src} -> {dst}")


def edit_config_files(projectname: str):
    """Edit .project, pom.xml, and MANIFEST.MF in the config project directory."""
    config_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    manifest_path = os.path.join(config_dir, r"META-INF\MANIFEST.MF")

    replace_in_file(os.path.join(config_dir, ".project"), "svcqualification", projectname)
    replace_in_file(os.path.join(config_dir, "pom.xml"), "svcqualification", projectname)
    replace_in_file(manifest_path, "svcqualification", projectname)

    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(
            r"\n[\t ]*\nService-Component:[^\n]*(\n[ \t]+[^\n]*)*", "", content
        )
        content = re.sub(r"\nService-Component:[^\n]*(\n[ \t]+[^\n]*)*", "", content)
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Cleaned Service-Component entries from: {manifest_path}")


def edit_build_files(projectname: str):
    """Edit .project and pom.xml in build subdirectories, plus category/feature XMLs."""
    for suffix in ["api.esa", "build", "config.esa", "esa", "feature", "p2"]:
        build_dir = os.path.join(BUILDDIR, f"com.telus.connector.{projectname}.{suffix}")
        project_file = os.path.join(build_dir, ".project")
        pom_file = os.path.join(build_dir, "pom.xml")
        if os.path.exists(project_file):
            replace_in_file(project_file, "svcqualification", projectname)
        else:
            print(f"[WARN] .project not found, skipping: {project_file}")
        if os.path.exists(pom_file):
            replace_in_file(pom_file, "svcqualification", projectname)
        else:
            print(f"[WARN] pom.xml not found, skipping: {pom_file}")

    category_xml = os.path.join(
        BUILDDIR, f"com.telus.connector.{projectname}.p2", "category.xml"
    )
    if os.path.exists(category_xml):
        replace_in_file(category_xml, "svcqualification", projectname)
    else:
        print(f"[WARN] category.xml not found, skipping: {category_xml}")

    feature_xml = os.path.join(
        BUILDDIR, f"com.telus.connector.{projectname}.feature", "feature.xml"
    )
    if os.path.exists(feature_xml):
        replace_in_file(feature_xml, "svcqualification", projectname)
    else:
        print(f"[WARN] feature.xml not found, skipping: {feature_xml}")


def edit_api_files(projectname: str):
    """Edit API project metadata and rename the source package folder."""
    api_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.api")

    replace_in_file(os.path.join(api_dir, ".project"), "svcqualification", projectname)
    replace_in_file(os.path.join(api_dir, "pom.xml"), "svcqualification", projectname)
    replace_in_file(
        os.path.join(api_dir, r"META-INF\MANIFEST.MF"), "svcqualification", projectname
    )

    src_roots = ["src", "src-gen"]
    renamed_any = False
    for src_root in src_roots:
        old_pkg = os.path.join(
            api_dir, src_root, "com", "telus", "connector", TEMPLATE_NAME, "api"
        )
        new_pkg = os.path.join(
            api_dir,
            src_root,
            "com",
            "telus",
            "connector",
            projectname_to_path(projectname),
            "api",
        )
        if os.path.exists(old_pkg):
            os.makedirs(os.path.dirname(new_pkg), exist_ok=True)
            os.rename(old_pkg, new_pkg)
            print(f"Renamed package folder: {old_pkg} -> {new_pkg}")
            renamed_any = True

    if not renamed_any:
        print("  [INFO] No template API package folder found to rename (src/src-gen)")


def edit_impl_files(projectname: str):
    """Edit implementation project metadata and rename source package folder."""
    impl_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}")

    replace_in_file(os.path.join(impl_dir, ".project"), "svcqualification", projectname)
    replace_in_file(os.path.join(impl_dir, "pom.xml"), "svcqualification", projectname)
    replace_in_file(
        os.path.join(impl_dir, r"META-INF\MANIFEST.MF"), "svcqualification", projectname
    )

    old_pkg = os.path.join(impl_dir, "src", "com", "telus", "connector", TEMPLATE_NAME)
    new_pkg = os.path.join(
        impl_dir,
        "src",
        "com",
        "telus",
        "connector",
        projectname_to_path(projectname),
    )
    if os.path.exists(old_pkg):
        os.makedirs(os.path.dirname(new_pkg), exist_ok=True)
        os.rename(old_pkg, new_pkg)
        print(f"Renamed package folder: {old_pkg} -> {new_pkg}")
    else:
        print(f"[WARN] Package folder not found, skipping rename: {old_pkg}")

    constants_file = os.path.join(new_pkg, "Constants.java")
    if os.path.exists(constants_file):
        replace_in_file(constants_file, "svcqualification", projectname)
    else:
        print(f"  [WARN] Constants.java not found, skipping: {constants_file}")

