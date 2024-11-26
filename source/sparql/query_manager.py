import json
import logging
from typing import Dict, Union


class QueryManager:
    def __init__(self, query_file_path: str, debug: bool = False):
        """
        Initializes the QueryManager.

        Args:
            query_file_path (str): Path to the JSON file containing SPARQL queries and prefixes.
            debug (bool): Enable debug-level logging if True.
        """
        self.query_file_path = query_file_path
        self._data = None  # Cache for loaded JSON data
        
        # Set logging level
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

    def _load_queries(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """Loads SPARQL queries and prefixes from the JSON file."""
        if self._data is None:
            try:
                with open(self.query_file_path, "r", encoding="utf-8") as file:
                    self.logger.info(f"Loading SPARQL queries from {self.query_file_path}...")
                    self._data = json.load(file)
            except FileNotFoundError:
                self.logger.error(f"Query file not found: {self.query_file_path}")
                raise
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON file: {e}")
                raise
        return self._data

    @property
    def prefixes(self) -> str:
        """
        Retrieves the SPARQL prefixes from the JSON data.

        Returns:
            str: The SPARQL prefixes.
        """
        return self._load_queries().get("prefixes", "")

    @property
    def queries(self) -> Dict[str, str]:
        """
        Retrieves the SPARQL queries from the JSON data.

        Returns:
            Dict[str, str]: A dictionary of SPARQL query names and their query strings.
        """
        return self._load_queries().get("queries", {})

    def list_queries(self) -> Dict[str, str]:
        """
        Lists all available query names and their query strings.

        Returns:
            Dict[str, str]: A dictionary of query names and query strings.
        """
        return self.queries

    def get_query(self, query_name: str) -> str:
        """
        Retrieves a specific SPARQL query by name, including the prefixes.

        Args:
            query_name (str): The name of the query to retrieve.

        Returns:
            str: The full SPARQL query (prefixes + query).

        Raises:
            ValueError: If the query name does not exist.
        """
        queries = self.queries
        if query_name not in queries:
            self.logger.error(f"Query '{query_name}' not found.")
            raise ValueError(f"Query '{query_name}' not found.")
        self.logger.debug(f"Retrieved query: {query_name}")
        return self.prefixes + "\n\n" + queries[query_name]
