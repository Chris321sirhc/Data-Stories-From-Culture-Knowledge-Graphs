import logging
from pathlib import Path
from source.sparql.manager import QueryManager
from source.sparql.executor import SPARQLQueryExecutor
from source.sparql.process import convert_bindings_to_dataframe
from source.util import (
    list_dir_files,
    list_and_select_query,
    display_sorted_results,
    select_from_list,
)
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def select_query_file(directory: str) -> Path:
    """
    Prompts the user to select a query file from the specified directory.

    Args:
        directory (str): Directory containing query files.

    Returns:
        Path: Path to the selected query file.
    """
    try:
        files = list_dir_files(directory)
        selected_file = Path(directory) / select_from_list(files, "Select a query file: ")
        return selected_file.resolve()
    except Exception as e:
        logger.error(f"Error selecting query file: {e}")
        raise


def execute_and_display_query(
    query_manager: QueryManager, sparql_executor: SPARQLQueryExecutor
):
    """
    Handles query selection, execution, and displaying results.

    Args:
        query_manager (QueryManager): Instance of QueryManager to manage queries.
        sparql_executor (SPARQLQueryExecutor): Instance of SPARQLQueryExecutor to execute queries.
    """
    try:
        # List and select query
        queries = query_manager.list_queries()
        query_name = list_and_select_query(queries)
        query = query_manager.get_query(query_name)
        logger.info(f"Selected query: {query_name}")

        # Execute query
        results = sparql_executor.execute_query(query)

        # Extract and process bindings
        bindings = sparql_executor.extract_bindings(results)
        if not bindings:
            logger.warning("Query returned no results.")
            return

        # Convert to DataFrame
        df = convert_bindings_to_dataframe(bindings)

        # Display sorted results as an example
        if "value" in df.columns and "count" in df.columns:
            display_sorted_results(df.to_dict("records"), "value", "count")
        else:
            logger.info("\nQuery Results Preview:")
            logger.info(f"\n{df.head()}")

    except Exception as e:
        logger.error("An error occurred during query execution:")
        logger.error(traceback.format_exc())


def main():
    """
    Main entry point for the application.
    """
    try:
        # Select query file
        query_file_path = select_query_file("files")
        logger.info(f"Using query file: {query_file_path}")

        # Initialize components
        endpoint = "https://nfdi4culture.de/sparql"
        query_manager = QueryManager(query_file_path)
        sparql_executor = SPARQLQueryExecutor(endpoint)

        # Execute query and display results
        execute_and_display_query(query_manager, sparql_executor)

    except Exception as e:
        logger.error("Critical error in main execution:")
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
