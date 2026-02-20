"""Main entry point for the Connector Generator."""


def generate_connector(name: str, connector_type: str) -> dict:
    """Generate a connector configuration.

    Args:
        name: The name of the connector.
        connector_type: The type of the connector (e.g. 'http', 'database').

    Returns:
        A dictionary representing the connector configuration.
    """
    if not name:
        raise ValueError("Connector name must not be empty.")
    if not connector_type:
        raise ValueError("Connector type must not be empty.")

    return {
        "name": name,
        "type": connector_type,
        "version": "1.0",
    }


def main() -> None:
    """Run the Connector Generator CLI."""
    print("Insight Connector Generator")
    print("Use generate_connector(name, connector_type) to create a connector.")


if __name__ == "__main__":
    main()
