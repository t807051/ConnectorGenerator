# Insight Connector Project Generator — User's Guide

## 1. Overview

The **Connector Project Generator** is a Python CLI package that automates the creation of a complete Insight connector project from a single JSON definition file. Given a definition file describing one or more connectors, the tool:

- Copies the template project structure to the target output directories.
- Renames all template placeholders (`svcqualification`) to your project name.
- Generates all required Java source files, IDL type files, OSGI configuration files, and XML descriptors — ready for import into your IDE.

A single run produces a fully scaffolded, compilable connector project with no manual file editing required.

---

## 2. Prerequisites

|Requirement|Details|
|---|---|
|**Python**|Standard library only — no third-party packages needed. Python 3.9+ required (per `pyproject.toml`).|
|**Template directories**|Must exist at `TEMPLATEDIR` (default: `C:\github\t807051\ConnectorGenerator\Template`).|
|**Output base directory**|Must exist at `BASEDIR` (default: `C:\TEMP`). The tool will create subdirectories under it.|
|**Definition JSON file**|You must author this file before running (see Section 4).|
|**Example JSON files**|Optional but recommended — placed in the same folder as the definition file (see Section 5).|

---

## 3. Running the Generator

**Option A — from source (no install required):**

```
python connector_generator/src/main.py <definition.json>
```

**Option B — installed package:**

```bash
pip install -e .
connector-generator <definition.json>
```

**Example (from source):**
```
python connector_generator/src/main.py C:\MyProject\inventory.tmf.json
```

The tool prints progress to the console as it works through each step. Warnings are prefixed with `[WARN]` and errors with `[ERROR]`. A successful run ends with:

```
=== Generation Complete ===
```

If the tool fails, it prints `[ERROR] Generation failed: <reason>` and exits. No partial cleanup is performed, so you may need to manually remove any partially created output directories before re-running.

---

## 4. Authoring the Definition JSON File

The definition file is the only input you need to create. It is a UTF-8 encoded JSON file that describes your connector project.

### 4.1 File Structure


```
{
  "projectname": "<projectname>",
  "connectors": [
    {
      "connectorid": "<connectorid>",
      "inputClass": "<inputClass>",
      "entityClass": "<entityClass>",
      "dataRecordClass": "<dataRecordClass>",
      "apiPath": "<apiPath>",
      "httpMethod": "<httpMethod>",
      "requestExample": "<requestExampleFilename>",
      "responseExample": "<responseExampleFilename>"
    }
  ]
}
```

### 4.2 Field Reference

| Field             | Required   | Description                                                                                                                                                                    |
| ----------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `projectname`     | ✅ Yes      | The source system name. Either `<sourceSystem>` or `<sourceSystem>.tmf`. Always **lowercase**. e.g. `"inventory"` or `"inventory.tmf"`                                         |
| `connectorid`     | ✅ Yes      | Unique identifier for this connector within the project. Drives all generated file and class names. e.g. `"CreateInventoryItem"`                                               |
| `inputClass`      | ✅ Yes      | Name of the input/request class. e.g. `"CreateInventoryItemRequest"`                                                                                                           |
| `entityClass`     | ✅ Yes      | Name of the entity class. e.g. `"CreateInventoryItemEntity"`                                                                                                                   |
| `dataRecordClass` | ✅ Yes      | Name of the data record class. e.g. `"CreateInventoryItemDataRecord"`                                                                                                          |
| `apiPath`         | ✅ Yes      | The REST API endpoint path. e.g. `"/inventory/v1/items"`                                                                                                                       |
| `httpMethod`      | ✅ Yes      | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`                                                                                                                        |
| `requestExample`  | ⬜ Optional | Filename of a JSON file representing a sample API **request** body. Must be in the same directory as the definition file. Omit or set `null` if not applicable (e.g. for GET). |
| `responseExample` | ⬜ Optional | Filename of a JSON file representing a sample API **response** body. Must be in the same directory as the definition file. Omit or set `null` if not applicable.               |

### 4.3 Multiple Connectors

A single project can contain multiple connectors. Add one object per connector to the `"connectors"` array:

```
{
  "projectname": "inventory.tmf",
  "connectors": [
    {
      "connectorid": "GetInventoryItem",
      "inputClass": "GetInventoryItemRequest",
      "entityClass": "GetInventoryItemEntity",
      "dataRecordClass": "GetInventoryItemDataRecord",
      "apiPath": "/inventory/v1/items/{id}",
      "httpMethod": "GET",
      "requestExample": null,
      "responseExample": "getInventoryItemResponse.json"
    },
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

### 4.4 Validation Rules

The tool validates the definition file on startup and exits with an error if:

- The file does not exist or is empty.
- The file is not valid JSON.
- `"projectname"` is missing.
- `"connectors"` is missing or empty.
- Any connector entry is missing one of the six required fields: `connectorid`, `inputClass`, `entityClass`, `dataRecordClass`, `apiPath`, `httpMethod`.

---

## 5. Example JSON Files (Optional but Recommended)

The `requestExample` and `responseExample` files are plain JSON files that represent a real sample request body and response body for the API endpoint. They must be placed in the **same directory** as the definition file.

### 5.1 What They Are Used For

|File|Used to generate|
|---|---|
|`responseExample`|IDL fields in `<connectorid>Entity` struct; Java POJO class `<responseStem>Pojo.java`; conversion logic in `<connectorid>Converter.java` (mapping response JSON → entity)|
|`requestExample`|IDL fields in `<connectorid>Request` struct; Java POJO class `<requestStem>Pojo.java`; conversion logic in `<connectorid>Converter.java` (mapping request entity → request POJO)|

### 5.2 Tips for Writing Example Files

- Use **realistic, non-null values** wherever possible. Null values result in `// TODO: verify data type` comments in the generated code.
- For **list fields**, include at least one element so the tool can infer the list element type.
- For **nested objects**, include all expected fields — the tool reads the full structure recursively.
- If the root of the JSON is a list (array), the tool uses the **first element** for field inference.

### 5.3 JSON-to-Java Type Mapping

The tool maps JSON value types to Java/IDL types as follows:

|JSON value type|Java (POJO)|IDL|
|---|---|---|
|`true` / `false`|`boolean`|`bool`|
|Integer number|`long`|`long`|
|Decimal number|`double`|`double`|
|String (date-like)|`Date`|`date`|
|String (other)|`String`|`string`|
|`null`|`String` + TODO comment|`string` + TODO comment|
|Array of objects|`List<SingularNamePojo>`|`SingularName[]`|
|Array of strings|`List<String>`|`string[]`|
|Nested object|`NestedNamePojo`|`NestedName` struct|

---

## 6. What the Tool Generates

After a successful run, the following output is produced under `C:\TEMP\` (or your configured `BASEDIR`):

### 6.1 Connector Project (`connectors\com.telus.connector.<projectname>\`)

|File|Description|
|---|---|
|`.project`, `pom.xml`, `META-INF\MANIFEST.MF`|Project metadata, updated with your project name|
|`src\...\call\<connectorid>Connector.java`|REST connector class — HTTP method-specific code auto-selected|
|`src\...\model\<responseStem>Pojo.java`|POJO for deserializing the API response JSON|
|`src\...\model\<requestStem>Pojo.java`|POJO for serializing the API request JSON (POST/PUT/PATCH only)|
|`src\...\model\<NestedClass>Pojo.java`|Additional POJOs for any nested objects in the example JSON|
|`src\...\converter\<connectorid>Converter.java`|Converter class with auto-generated field mapping logic|
|`src\...\factories\<connectorid>Factory.java`|Factory class wired to the API path|
|`src\...\exception\<connectorid>ConversionException.java`|Custom exception class|

### 6.2 API Project (`connectors\com.telus.connector.<projectname>.api\`)

|File|Description|
|---|---|
|`OSGI-INF\solvatio\connectors.xml`|Connector registry — one `<connector>` block per connector|
|`src\...\api\datatypes\<connectorid>Types.model`|IDL type definitions: `<connectorid>Request`, `<connectorid>Entity`, `<connectorid>DataRecord`, plus any nested structs|

### 6.3 Config Project (`connectors\com.telus.connector.<projectname>.config\`)

|File|Description|
|---|---|
|`OSGI-INF\com.telus.connector.<projectname>.<connectorid>.xml`|OSGi component descriptor|
|`src\...\I<connectorid>ConfigurationComponent.java`|Configuration interface|
|`src\...\<connectorid>ConfigurationComponent.java`|Configuration implementation|
|`META-INF\MANIFEST.MF`|Updated with `Service-Component: OSGI-INF/<connectorid>.xml` entries|

### 6.4 Build Projects (`build\com.telus.connector.<projectname>.*`)

Six build subdirectories (`api.esa`, `build`, `config.esa`, `esa`, `feature`, `p2`) are copied and updated with your project name, including `feature.xml` and `category.xml`.

### 6.5 Knowledge Base Directories

Two Knowledge Base directories are copied under `knowledgebases\com.telus.falcon.knowledgebase\model\`.

---

## 7. Understanding the Generated Converter

The converter (`<connectorid>Converter.java`) is the most complex generated file. Here is what it contains:

- **`convert(JsonNode input)`** — The main entry point. Deserializes the raw JSON response into the response POJO, then calls `to<connectorid>Entity()`.
- **`to<connectorid>Entity(<responseStem>Pojo pojo)`** — Maps the response POJO fields to the IDL entity struct. Field mapping is auto-generated from `responseExample`.
- **`to<connectorid>Pojo(<connectorid>Request request)`** — Maps the IDL request struct fields to the request POJO. Only generated if `requestExample` is provided.
- **`private convertTo<NestedType>(...)`** — Helper methods auto-generated for each nested object or list of objects found in the example JSON. These use `.create()` (not `new`) to instantiate API datatype structs.

**After generation**, review the converter for any `// TODO:` comments — these indicate fields where the tool could not determine the type (e.g. null values in the example JSON) and require manual attention.

---

## 8. Configuring Output Directories

The tool's directory paths are defined as constants in `connector_generator/src/settings.py`. If your environment differs from the defaults, edit these values before running:

|Constant|Default|Description|
|---|---|---|
|`BASEDIR`|`C:\TEMP`|Root output directory|
|`TEMPLATEDIR`|`C:\github\t807051\ConnectorGenerator\Template`|Location of the template projects|

The alternate `BASEDIR` (`C:\github\Insight10.8\Insight`) and `TEMPLATEDIR` (`C:\cb\Insight10.8\Template`) are commented out in `settings.py` and can be swapped in by editing those constants.

---

## 9. Warnings and Troubleshooting

|Message|Meaning|Action|
|---|---|---|
|`[WARN] .project not found, skipping`|A build subdirectory's `.project` file was not found|Check that the template was copied correctly|
|`[WARN] category.xml not found, skipping`|`p2\category.xml` is missing from the template|Verify the template's `p2` directory|
|`[WARN] feature.xml not found, skipping`|`feature\feature.xml` is missing from the template|Verify the template's `feature` directory|
|`[WARN] Constants.java not found, skipping`|The impl project's `Constants.java` was not found after package rename|Not critical — add manually if needed|
|`[WARN] requestExample file not found or empty`|The JSON file named in `requestExample` does not exist|Check the filename and that it is in the same directory as the definition file|
|`[WARN] Template file not found for deletion`|A template `.java.txt` file was expected but not found|Usually harmless — the file may already have been removed|
|`[ERROR] Generation failed`|An unhandled exception occurred|Read the error message; common causes are missing template directories or a malformed definition file|
|`// TODO: verify data type` in generated code|A JSON field was `null` or an empty array in the example|Replace with the correct Java type manually|
|`// TODO: implement the conversion logic here` in converter|No `responseExample` or `requestExample` was provided|Add example JSON files and re-run, or implement the logic manually|

---

## 10. Complete Example

**Directory layout before running:**

```
C:\MyProject\
	inventory.tmf.json
	createInventoryItemRequest.json
	createInventoryItemResponse.json
```

**`inventory.tmf.json`:**
```
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

**`createInventoryItemResponse.json`:**
```
{
  "version": "1.0",
  "account": "ACC-001",
  "msisdn": "4161234567",
  "signal": {
    "cellular": "LTE",
    "wifi": "802.11ac"
  },
  "smartphones": [
    {
      "name": "iPhone 15",
      "manufacturer": "Apple",
      "model": "A3092",
      "os": "iOS 17",
      "active": true
    }
  ]
}
```


**Run:**
```
python connector_generator/src/main.py C:\MyProject\inventory.tmf.json
```

**Key generated files:**
```
C:\MyProject\connectors\com.telus.connector.inventory.tmf\
  src\com\telus\connector\inventory\tmf\
    call\CreateInventoryItemConnector.java
    model\CreateInventoryItemResponse2Pojo.java
    model\SignalPojo.java
    model\SmartphonePojo.java
    converter\CreateInventoryItemConverter.java
    factories\CreateInventoryItemFactory.java
    exception\CreateInventoryItemConversionException.java

C:\MyProject\connectors\com.telus.connector.inventory.tmf.api\
  src\com\telus\connector\inventory\tmf\api\datatypes\
    CreateInventoryItemTypes.model
  OSGI-INF\solvatio\connectors.xml

C:\MyProject\connectors\com.telus.connector.inventory.tmf.config\
  OSGI-INF\com.telus.connector.inventory.tmf.CreateInventoryItem.xml
  src\com\telus\connector\inventory\tmf\
    ICreateInventoryItemConfigurationComponent.java
    CreateInventoryItemConfigurationComponent.java
```


