from SPARQLWrapper import SPARQLWrapper, JSON
import logging
from typing import Any, Dict, List

class SPARQLQueryExecutor:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Executes a SPARQL query and returns the results."""
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        try:
            logging.info("Executing SPARQL query...")
            results = sparql.queryAndConvert()
            logging.info("Query executed successfully.")
            return results
        except Exception as e:
            logging.error(f"Error executing SPARQL query: {e}")
            raise

    @staticmethod
    def extract_head(results: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts the head from the SPARQL query results."""
        return results.get("head", {})

    @staticmethod
    def extract_bindings(results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extracts bindings from the SPARQL query results."""
        return results.get("results", {}).get("bindings", [])
