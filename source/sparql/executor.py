import json
import logging
from typing import Any, Dict, List, Optional
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


class SPARQLQueryExecutor:
    """Handles SPARQL queries and processes results."""

    def __init__(self, endpoint: str, debug: bool = False):
        """
        Initializes the SPARQLQueryExecutor.

        Args:
            endpoint (str): The SPARQL endpoint URL.
            debug (bool): Enables debug-level logging if True.
        """
        self.endpoint = endpoint
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Executes a SPARQL query and returns the results.

        Args:
            query (str): The SPARQL query string.

        Returns:
            Dict[str, Any]: The query results in JSON format.

        Raises:
            RuntimeError: If the query execution fails.
        """
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        try:
            self.logger.info("Executing SPARQL query...")
            results = sparql.queryAndConvert()
            self.logger.info("Query executed successfully.")
            return results
        except Exception as e:
            self.logger.error(f"Error executing SPARQL query: {e}")
            raise RuntimeError(f"Failed to execute SPARQL query: {e}") from e

    @staticmethod
    def extract_head(results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts the head from SPARQL query results.

        Args:
            results (Dict[str, Any]): The SPARQL results.

        Returns:
            Dict[str, Any]: The "head" part of the results.
        """
        return results.get("head", {})

    @staticmethod
    def extract_bindings(results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts bindings from SPARQL query results.

        Args:
            results (Dict[str, Any]): The SPARQL results.

        Returns:
            List[Dict[str, Any]]: A list of binding dictionaries.
        """
        return results.get("results", {}).get("bindings", [])


class QueryManager:
    """Manages SPARQL query loading and retrieval."""

    def __init__(self, query_file_path: str, debug: bool = False):
        """
        Initializes the QueryManager.

        Args:
            query_file_path (str): Path to the JSON file containing queries.
            debug (bool): Enables debug-level logging if True.
        """
        self.query_file_path = query_file_path
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self._queries = None  # Caching loaded queries

    def _load_queries(self) -> Dict[str, str]:
        """
        Loads SPARQL queries from a JSON file.

        Returns:
            Dict[str, str]: A dictionary of queries.

        Raises:
            RuntimeError: If the file is not found or contains invalid JSON.
        """
        if self._queries is None:
            try:
                with open(self.query_file_path, "r", encoding="utf-8") as file:
                    self.logger.info("Loading SPARQL queries from file...")
                    self._queries = json.load(file)
                    self.logger.info("Queries loaded successfully.")
            except FileNotFoundError:
                self.logger.error(f"Query file not found: {self.query_file_path}")
                raise RuntimeError(f"Query file not found: {self.query_file_path}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON file: {e}")
                raise RuntimeError(f"Invalid JSON in query file: {e}") from e
        return self._queries

    def get_query(self, query_name: str) -> str:
        """
        Retrieves a specific SPARQL query by name.

        Args:
            query_name (str): The name of the query to retrieve.

        Returns:
            str: The query string.

        Raises:
            ValueError: If the query is not found.
        """
        queries = self._load_queries()
        if query_name not in queries:
            self.logger.error(f"Query '{query_name}' not found.")
            raise ValueError(f"Query '{query_name}' not found.")
        self.logger.debug(f"Retrieved query: {query_name}")
        return queries[query_name]


def convert_bindings_to_dataframe(
    bindings: List[Dict[str, Any]], flatten: bool = True
) -> pd.DataFrame:
    """
    Converts SPARQL query bindings into a Pandas DataFrame.

    Args:
        bindings (List[Dict[str, Any]]): A list of binding dictionaries.
        flatten (bool): Whether to flatten nested structures.

    Returns:
        pd.DataFrame: A DataFrame containing the query results.

    Raises:
        ValueError: If bindings are empty or invalid.
    """
    logger = logging.getLogger("convert_bindings_to_dataframe")
    try:
        logger.info("Converting bindings to DataFrame...")
        if not bindings:
            raise ValueError("Bindings are empty or invalid.")
        
        # Normalize JSON bindings to a flat DataFrame
        df = pd.json_normalize(bindings) if flatten else pd.DataFrame(bindings)
        logger.info("Conversion successful.")
        return df
    except Exception as e:
        logger.error(f"Error converting bindings to DataFrame: {e}")
        raise RuntimeError(f"Failed to convert bindings to DataFrame: {e}") from e
