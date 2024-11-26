import logging
from source.util import display_results, export_results_to_json, get_user_selection
from typing import Callable, Dict, List, Optional



logger = logging.getLogger(__name__)

def fetch_and_select(
    fetch_method: Callable[[int], List[Dict]], key: str, count_key: str, limit: int = 10
) -> Optional[str]:
    """
    Fetches data using a provided method and allows the user to select an option.

    Args:
        fetch_method (Callable[[int], List[Dict]]): A method that fetches results.
        key (str): The key for the main value to display and select.
        count_key (str): The key for the count value to display.
        limit (int): Number of results to fetch.

    Returns:
        Optional[str]: The selected value or None if the user exits.
    """
    try:
        logger.info(f"Fetching data with limit={limit}...")
        results = fetch_method(limit)
        if not results:
            logger.warning(f"No results found for key '{key}'.")
            return None

        display_results(results, key=key, count_key=count_key)
        return get_user_selection(results, key=key)
    except Exception as e:
        logger.error(f"Error during fetch and select for key '{key}': {e}")
        return None
    

def select_type(explorer) -> Optional[str]:
    """
    Prompts the user to select a type.

    Args:
        explorer (KnowledgeGraphExplorer): Explorer instance to fetch types.

    Returns:
        Optional[str]: The selected type or None if user exits.
    """
    logger.info("Starting type selection step.")
    max_limit = explorer.get_max_types() or 10  # Default to 10 if the query fails
    limit = query_user_limit(max_limit, "Enter the number of types to fetch")
    return fetch_and_select(
        fetch_method=explorer.fetch_types,
        key="type",
        count_key="count",
        limit=limit,
    )

def select_property(explorer, rdf_type: str) -> Optional[str]:
    """
    Prompts the user to select a property for a given type.

    Args:
        explorer (KnowledgeGraphExplorer): Explorer instance to fetch properties.
        rdf_type (str): RDF type for which properties are fetched.

    Returns:
        Optional[str]: The selected property or None if user exits.
    """
    logger.info(f"Starting property selection step for type: {rdf_type}.")
    max_limit = explorer.get_max_properties(rdf_type) or 10  # Default to 10 if the query fails
    limit = query_user_limit(max_limit, "Enter the number of properties to fetch")
    return fetch_and_select(
        fetch_method=lambda limit: explorer.fetch_properties(rdf_type, limit),
        key="property",
        count_key="count",
        limit=limit,
    )


def handle_values(explorer, rdf_type, property_uri, limit=10):
    """
    Fetches, displays, and optionally exports values for a property.

    Args:
        explorer (KnowledgeGraphExplorer): Explorer instance to fetch values.
        rdf_type (str): RDF type.
        property_uri (str): Property URI.
        limit (int): Limit for the number of values to fetch.
    """
    logger.info(f"Fetching values for property: {property_uri}.")
    values = explorer.fetch_values(rdf_type, property_uri, limit)

    if not values:
        logger.warning(f"No values found for property: {property_uri}.")
        print(f"No values found for property: {property_uri}.")
        return

    logger.info("Displaying values for the selected property.")
    display_results(values, key="value", count_key="count")

    if input("Do you want to export the results? (y/n): ").strip().lower() == "y":
        logger.info("Exporting results.")
        export_results_to_json(values)

def query_user_limit(max_limit: int, prompt: str) -> int:
    """
    Prompts the user to enter a limit constrained by the maximum value.

    Args:
        max_limit (int): The maximum allowable limit.
        prompt (str): The prompt to display to the user.

    Returns:
        int: The user-selected limit.
    """
    while True:
        try:
            user_input = input(f"{prompt} (max {max_limit}): ").strip()
            limit = int(user_input)
            if 1 <= limit <= max_limit:
                return limit
            print(f"Please enter a number between 1 and {max_limit}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
