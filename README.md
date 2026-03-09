# ConnectorGenerator

Insight Connector Project Generator — a Python CLI that scaffolds complete Insight connector projects from a single JSON definition file.

## What it does
Given a definition JSON describing one or more connectors, the generator will:
- Copy a ready-to-build template project structure
- Replace the template placeholder name ("svcqualification") with your project name
- Generate Java implementation classes (Connector, Converter, Factory, Exception)
- Generate API IDL type files (`<connectorid>Types.model`)
- Generate OSGi configuration (component XML, manifest Service-Component entries)
- Generate a Markdown connector specification document from the provided template

See the full walkthrough in `docs/UsersGuide.md`.

## Prerequisites
- Python 3.9+ (the package metadata targets 3.9+; the script itself uses only the standard library)
- A local copy of the `Template/` directory (included in this repo)
- A base output directory to generate into

## Install (optional)
This repository is also packaged as a Python project:

```bash
python -m pip install -e .
```

## Usage
### 1) Create a connector definition JSON
Minimum structure:
```json
{
  "projectname": "inventory.tmf",
  "connectors": [
    {
      "connectorid": "CreateInventoryItem",
      "inputClass": "CreateInventoryItemRequest",
      "entityClass": "CreateInventoryItemEntity",
      "dataRecordClass": "CreateInventoryItemDataRecord",
      "apiPath": "/inventory/v1/items",
      "httpMethod": "POST",
      "requestExample": "createInventoryItemRequest.json",
      "responseExample": "createInventoryItemResponse.json"
    }
  ]
}
```

### 2) Run the generator
If running from source:
```bash
python connector_generator/src/main.py path\to\definition.json
```

Or, if installed as a package:
```bash
connector-generator path\to\definition.json
```

## Output
The generator writes into the configured `BASEDIR` (default in code: `C:\TEMP`) and creates subfolders such as:
- `connectors/` (implementation, API, and config projects)
- `build/` (ESA/feature/p2 build projects)
- `knowledgebases/` (knowledge base model directories)
- `docs/` (generated connector spec: `<projectname>-connector-spec.md`)

## Configuration
Paths are currently configured as constants at the top of `connector_generator/src/main.py` (e.g., `BASEDIR`, `TEMPLATEDIR`). Update these for your environment before running.

## Development
Run tests:
```bash
python -m pip install -e .[dev]
pytest
```

## License
Add a license file if you plan to distribute this publicly.