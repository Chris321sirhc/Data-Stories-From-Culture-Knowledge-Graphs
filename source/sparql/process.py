import pandas as pd
import logging
from typing import List, Dict, Any

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
