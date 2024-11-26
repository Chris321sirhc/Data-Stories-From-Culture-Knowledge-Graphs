import logging
from explorer.explorer import KnowledgeGraphExplorer
from explorer.ui import select_type, select_property, handle_values

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def knowledge_graph_explorer(endpoint: str) -> None:
    """
    Main workflow for the Knowledge Graph Explorer.

    Args:
        endpoint (str): The SPARQL endpoint URL.
    """
    explorer = KnowledgeGraphExplorer(endpoint_url=endpoint, cache_enabled=True)
    logger.info("Welcome to the Knowledge Graph Explorer!")

    while True:
        selected_type = select_type(explorer)
        if not selected_type:
            logger.info("No type selected. Exiting application.")
            print("Exiting.")
            break

        selected_property = select_property(explorer, selected_type)
        if not selected_property:
            logger.info("No property selected. Returning to type selection.")
            continue

        handle_values(explorer, selected_type, selected_property)
        logger.info("Returning to type selection.")


if __name__ == "__main__":
    try:
        endpoint = "https://nfdi4culture.de/sparql"  # Replace with your endpoint
        knowledge_graph_explorer(endpoint)
    except Exception as e:
        logger.critical(f"An unrecoverable error occurred: {e}", exc_info=True)
