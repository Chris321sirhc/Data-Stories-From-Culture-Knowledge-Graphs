from SPARQLWrapper import SPARQLWrapper, JSON
import logging
from typing import Optional


class KnowledgeGraphExplorer:
    def __init__(self, endpoint_url: str, cache_enabled: bool = True):
        """
        Initializes the KnowledgeGraphExplorer.

        Args:
            endpoint_url (str): The SPARQL endpoint URL.
            cache_enabled (bool): Enables caching of query results.
        """
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)
        self.cache_enabled = cache_enabled
        self.cache = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute_query(self, query: str):
        """
        Executes a SPARQL query and returns results, optionally caching them.

        Args:
            query (str): The SPARQL query string.

        Returns:
            List[Dict]: Query results as a list of bindings.
        """
        if self.cache_enabled and query in self.cache:
            self.logger.info("Returning cached results.")
            return self.cache[query]

        self.sparql.setQuery(query)
        try:
            self.logger.info("Executing SPARQL query...")
            results = self.sparql.query().convert()
            bindings = results["results"]["bindings"]
            if self.cache_enabled:
                self.cache[query] = bindings
            return bindings
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise RuntimeError(f"Query execution failed: {e}")

    def fetch_types(self, limit: int = 10):
        from .queries import get_types_query
        return self.execute_query(get_types_query(limit))

    def fetch_properties(self, rdf_type: str, limit: int = 10):
        from .queries import get_properties_query
        return self.execute_query(get_properties_query(rdf_type, limit))

    def fetch_values(self, rdf_type: str, property_uri: str, limit: int = 10):
        from .queries import query_property_values
        return self.execute_query(query_property_values(rdf_type, property_uri, limit))


    def get_max_types(self) -> Optional[int]:
        """
        Queries the SPARQL endpoint for the maximum number of available types.

        Returns:
            Optional[int]: The maximum number of types or None if the query fails.
        """
        query = """
        SELECT (COUNT(DISTINCT ?type) AS ?count)
        WHERE {
            ?s a ?type .
        }
        """
        try:
            results = self.execute_query(query)
            return int(results[0]["count"]["value"]) if results else None
        except Exception as e:
            self.logger.error(f"Failed to fetch maximum number of types: {e}")
            return None

    def get_max_properties(self, rdf_type: str) -> Optional[int]:
        """
        Queries the SPARQL endpoint for the maximum number of properties for a given type.

        Args:
            rdf_type (str): The RDF type.

        Returns:
            Optional[int]: The maximum number of properties or None if the query fails.
        """
        query = f"""
        SELECT (COUNT(DISTINCT ?property) AS ?count)
        WHERE {{
            ?s a <{rdf_type}> ;
               ?property ?o .
        }}
        """
        try:
            results = self.execute_query(query)
            return int(results[0]["count"]["value"]) if results else None
        except Exception as e:
            self.logger.error(f"Failed to fetch maximum number of properties for type '{rdf_type}': {e}")
            return None