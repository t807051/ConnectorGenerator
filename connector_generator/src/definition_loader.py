import json
import os


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
        for field in [
            "connectorid",
            "inputClass",
            "entityClass",
            "dataRecordClass",
            "apiPath",
            "httpMethod",
        ]:
            if field not in connector:
                raise ValueError(f"Connector missing required field: '{field}'")
    return data

