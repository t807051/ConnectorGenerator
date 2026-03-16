"""
connector_generator.main
~~~~~~~~~~~~~~~~~~~~~~~~
Public entry-point shim.  All implementation lives in
connector_generator.src.*; this module re-exports the public surface so that:

  * the ``connector-generator`` CLI installed via pyproject.toml works
    (connector_generator.main:main)
  * external code that does ``from connector_generator.main import …`` keeps
    working without changes
"""
from connector_generator.src.main import (  # noqa: F401
    main,
    generate_config_per_connector,
    generate_kb_call_sfcx_per_connector,
    generate_kb_qa_per_connector,
    generate_api_per_connector,
    generate_impl_per_connector,
)
from connector_generator.src.definition_loader import load_definition  # noqa: F401
from connector_generator.src.spec_generator import generate_spec_doc  # noqa: F401

