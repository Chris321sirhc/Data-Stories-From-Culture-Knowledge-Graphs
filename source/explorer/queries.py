def get_types_query(limit: int = 10) -> str:
    return f"""
    SELECT ?type (COUNT(?s) AS ?count)
    WHERE {{
        ?s a ?type .
    }}
    GROUP BY ?type
    ORDER BY DESC(?count)
    LIMIT {limit}
    """

def get_properties_query(rdf_type: str, limit: int = 10) -> str:
    return f"""
    SELECT ?property (COUNT(?o) AS ?count)
    WHERE {{
        ?s a <{rdf_type}> ;
           ?property ?o .
    }}
    GROUP BY ?property
    ORDER BY DESC(?count)
    LIMIT {limit}
    """

def query_property_values(rdf_type: str, property_uri: str, limit: int = 10) -> str:
    return f"""
    SELECT ?value (COUNT(?s) AS ?count)
    WHERE {{
        ?s a <{rdf_type}> ;
           <{property_uri}> ?value .
    }}
    GROUP BY ?value
    ORDER BY DESC(?count)
    LIMIT {limit}
    """
