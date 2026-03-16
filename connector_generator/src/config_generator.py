import os

try:
    from .settings import CONNECTORDIR, TEMPLATE_CONFIG_JAVA, TEMPLATE_ICONFIG_JAVA
    from .file_ops import append_service_components, projectname_to_path
except ImportError:
    from settings import CONNECTORDIR, TEMPLATE_CONFIG_JAVA, TEMPLATE_ICONFIG_JAVA
    from file_ops import append_service_components, projectname_to_path


def generate_config_per_connector(projectname: str, connectors: list):
    """Generate OSGI-INF xml, ConfigComponent java files, and update MANIFEST.MF."""
    config_dir = os.path.join(CONNECTORDIR, f"com.telus.connector.{projectname}.config")
    osgi_dir = os.path.join(config_dir, "OSGI-INF")
    src_dir = os.path.join(
        config_dir,
        "src",
        "com",
        "telus",
        "connector",
        projectname_to_path(projectname),
    )
    delete_dir = os.path.join(
        config_dir, "src", "com", "telus", "connector", "svcqualification"
    )

    os.makedirs(osgi_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

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

    for txt_name in [
        "ITemplateConfigurationComponent.java.txt",
        "TemplateConfigurationComponent.java.txt",
    ]:
        txt_path = os.path.join(delete_dir, txt_name)
        if os.path.exists(txt_path):
            os.remove(txt_path)
            print(f"  Deleted template file: {txt_path}")
        else:
            print(f"  [WARN] Template file not found for deletion: {txt_path}")
    os.rmdir(delete_dir)

    manifest_path = os.path.join(config_dir, r"META-INF\MANIFEST.MF")
    append_service_components(manifest_path, osgi_files)


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
        raise FileNotFoundError(
            f"ITemplateConfigurationComponent.java.txt not found: {TEMPLATE_ICONFIG_JAVA}"
        )
    with open(TEMPLATE_ICONFIG_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated interface config: {path}")


def _write_impl_config(path: str, projectname: str, connectorid: str):
    """Generate <connectorid>ConfigurationComponent.java from template."""
    if not os.path.exists(TEMPLATE_CONFIG_JAVA):
        raise FileNotFoundError(
            f"TemplateConfigurationComponent.java.txt not found: {TEMPLATE_CONFIG_JAVA}"
        )
    with open(TEMPLATE_CONFIG_JAVA, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = content.replace("<projectname>", projectname)
    content = content.replace("<connectorid>", connectorid)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated impl config: {path}")

