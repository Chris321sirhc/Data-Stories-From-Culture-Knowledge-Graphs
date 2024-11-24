import logging
from source.sparql.query_manager import QueryManager
from source.sparql.sparql_exec import SPARQLQueryExecutor
from source.sparql.process import convert_bindings_to_dataframe
from source.util import list_and_select_query

def main():
    query_file_path = "files/sparql_queries.json"
    endpoint = "https://nfdi4culture.de/sparql"

    # Initialize components
    query_manager = QueryManager(query_file_path)
    sparql_executor = SPARQLQueryExecutor(endpoint)

    try:
        # List and select query
        queries = query_manager.list_queries()
        query_name = list_and_select_query(queries)
        query = queries[query_name]

        # Execute query
        results = sparql_executor.execute_query(query)

        # Process results
        bindings = sparql_executor.extract_bindings(results)
        df = convert_bindings_to_dataframe(bindings)

        # Display results
        print("\nQuery Results Preview:")
        print(df.head())
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()

