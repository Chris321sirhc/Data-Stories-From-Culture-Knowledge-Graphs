import json
import logging
from typing import Dict

class QueryManager:
    def __init__(self, query_file_path: str):
        self.query_file_path = query_file_path

    def load_queries(self) -> Dict[str, str]:
        """Loads SPARQL queries from a JSON file."""
        try:
            with open(self.query_file_path, "r", encoding="utf-8") as file:
                logging.info(f"Loading SPARQL queries from {self.query_file_path}...")
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Query file not found: {self.query_file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file: {e}")
            raise

    def list_queries(self) -> Dict[str, str]:
        """Lists all available queries."""
        queries = self.load_queries()["queries"]
        # logging.info(f"Available queries: {list(queries.keys())}")
        return queries

    def get_query(self, query_name: str) -> str:
        """Retrieves a specific SPARQL query by name."""
        queries = self.load_queries()
        if query_name not in queries:
            logging.error(f"Query '{query_name}' not found.")
            raise ValueError(f"Query '{query_name}' not found.")
        return queries[query_name]
