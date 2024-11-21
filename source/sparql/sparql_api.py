from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json

def get_sparql_query(query: str = "count_compositions_composer_name_decade") -> str:
    with open("files/sparql_queries.json") as f:
        queries = json.load(f)
    return queries[query]

def get_head(results: dict) -> dict:
    return results["head"]

def get_bindings(results: dict) -> list:
    return results["results"]["bindings"]

def get_sparql_query_results(query, endpoint: str = "https://nfdi4culture.de/sparql") -> dict:
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.queryAndConvert()
    return results

def main():
    query = get_sparql_query()
    results = get_sparql_query_results(query)
    head = get_head(results)
    bindings = get_bindings(results)
    df = pd.json_normalize(bindings)
    print(df.head())

if __name__ == "__main__":
    main()