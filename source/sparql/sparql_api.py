import json
import logging
from typing import Any, Dict, List, Optional
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SPARQLQueryExecutor:
    """A class to handle SPARQL queries and processing results."""

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

class QueryManager:
    """A class to manage loading and retrieving SPARQL queries."""

    def __init__(self, query_file_path: str):
        self.query_file_path = query_file_path

    def load_queries(self) -> Dict[str, str]:
        """Loads SPARQL queries from a JSON file."""
        try:
            with open(self.query_file_path, "r", encoding="utf-8") as file:
                logging.info("Loading SPARQL queries from file...")
                queries = json.load(file)
                logging.info("Queries loaded successfully.")
                return queries
        except FileNotFoundError:
            logging.error(f"Query file not found at {self.query_file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON file: {e}")
            raise

    def get_query(self, query_name: str) -> str:
        """Retrieves a specific SPARQL query by name."""
        queries = self.load_queries()
        if query_name not in queries:
            logging.error(f"Query '{query_name}' not found in the query file.")
            raise ValueError(f"Query '{query_name}' not found.")
        return queries[query_name]

def convert_bindings_to_dataframe(bindings: List[Dict[str, Any]]) -> pd.DataFrame:
    """Converts SPARQL query bindings into a Pandas DataFrame."""
    try:
        logging.info("Converting bindings to DataFrame...")
        df = pd.json_normalize(bindings)
        logging.info("Conversion successful.")
        return df
    except Exception as e:
        logging.error(f"Error converting bindings to DataFrame: {e}")
        raise

def main(query_name: str = "count_compositions_composer_name_decade"):
    """Main function to execute the workflow."""
    query_file_path = "files/sparql_queries.json"
    endpoint = "https://nfdi4culture.de/sparql"

    # Instantiate managers
    query_manager = QueryManager(query_file_path)
    sparql_executor = SPARQLQueryExecutor(endpoint)

    try:
        # Load and execute query
        query = query_manager.get_query(query_name)
        results = sparql_executor.execute_query(query)

        # Process results
        head = sparql_executor.extract_head(results)
        bindings = sparql_executor.extract_bindings(results)
        logging.info(f"SPARQL endpoint response head: {head}")

        # Convert results to DataFrame
        df = convert_bindings_to_dataframe(bindings)

        # Display results
        logging.info("Query results preview:")
        print(df.head())
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
