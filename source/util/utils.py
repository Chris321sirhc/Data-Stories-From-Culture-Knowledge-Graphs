from genericpath import exists
import logging
from typing import List, Dict, Optional
from os import listdir
from os.path import isfile, join
import pandas as pd
import json
from pathlib import Path
import os
from datetime import datetime

def list_dir_files(directory: str) -> List[str]:
    """
    Lists files in a directory.

    Args:
        directory (str): The directory path.

    Returns:
        List[str]: A list of file names in the directory.
    """
    try:
        logging.info(f"Listing files in directory: {directory}")
        return [f for f in listdir(directory) if isfile(join(directory, f))]
    except Exception as e:
        logging.error(f"Error listing files in directory '{directory}': {e}")
        raise


def select_from_list(options: List[str], prompt: str = "Select an option: ") -> str:
    """
    Prompts the user to select an option from a list.

    Args:
        options (List[str]): A list of options to display.
        prompt (str): The prompt message for selection.

    Returns:
        str: The selected option.

    Raises:
        ValueError: If the options list is empty.
    """
    if not options:
        raise ValueError("The list of options is empty.")
    if len(options) == 1:
        logging.info("Only one option available. Auto-selecting.")
        return options[0]

    logging.info(f"Displaying {len(options)} options to the user.")
    print("\n".join(f"{i + 1}. {option}" for i, option in enumerate(options)))

    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                logging.info(f"User selected option {choice}: {options[choice - 1]}")
                return options[choice - 1]
            print(f"Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def list_and_select_query(queries: Dict[str, str]) -> str:
    """
    Lists available queries and allows the user to select one.

    Args:
        queries (Dict[str, str]): A dictionary of query names and queries.

    Returns:
        str: The name of the selected query.
    """
    logging.info("Listing available queries for selection.")
    options = list(queries.keys())
    return select_from_list(options, "Select a query by number: ")


def display_results(results: List[Dict], key: str, count_key: str) -> None:
    """
    Displays results in a readable format.

    Args:
        results (List[Dict]): A list of result dictionaries.
        key (str): The key for the main value to display.
        count_key (str): The key for the count value.
    """
    logging.info("Displaying results.")
    for i, result in enumerate(results, start=1):
        print(
            f"{i}: {key.capitalize()}: {result[key]['value']}, Count: {result[count_key]['value']}"
        )


def get_user_selection(results: List[Dict], key: str) -> Optional[str]:
    """
    Prompts the user to select an item from the results.

    Args:
        results (List[Dict]): A list of result dictionaries.
        key (str): The key to extract the value for selection.

    Returns:
        Optional[str]: The selected item's value, or None if the user exits.
    """
    while True:
        try:
            choice = int(input(f"\nSelect an option (1-{len(results)}) or 0 to exit: "))
            if choice == 0:
                logging.info("User chose to exit selection.")
                return None
            if 1 <= choice <= len(results):
                logging.info(f"User selected option {choice}.")
                return results[choice - 1][key]["value"]
            print(f"Please select a number between 1 and {len(results)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def sort_results(results: List[Dict], count_key: str) -> List[Dict]:
    """
    Sorts results by count in descending order.

    Args:
        results (List[Dict]): A list of result dictionaries.
        count_key (str): The key to sort by.

    Returns:
        List[Dict]: The sorted results.
    """
    logging.info(f"Sorting results by key '{count_key}' in descending order.")
    try:
        return sorted(results, key=lambda x: int(x[count_key]["value"]), reverse=True)
    except Exception as e:
        logging.error(f"Error sorting results: {e}")
        raise


def suggest_top_n(
    results: List[Dict], key: str, count_key: str, top_n: int = 5
) -> List[str]:
    """
    Returns the top N most common results.

    Args:
        results (List[Dict]): A list of result dictionaries.
        key (str): The key to extract values.
        count_key (str): The key to sort by.
        top_n (int): The number of top results to return.

    Returns:
        List[str]: The top N result values.
    """
    logging.info(f"Suggesting the top {top_n} results.")
    sorted_results = sort_results(results, count_key)
    return [item[key]["value"] for item in sorted_results[:top_n]]


def display_sorted_results(results: List[Dict], key: str, count_key: str) -> None:
    """
    Displays sorted results in a readable format.

    Args:
        results (List[Dict]): A list of result dictionaries.
        key (str): The key for the main value to display.
        count_key (str): The key for the count value.
    """
    logging.info("Displaying sorted results.")
    sorted_results = sort_results(results, count_key)
    display_results(sorted_results, key, count_key)

def export_results_to_csv(results: List[Dict], filename: str):
    """
    Exports SPARQL query results to a CSV file.

    Args:
        results (List[Dict]): The query results to export.
        filename (str): The output file name.
    """
    if not filename.endswith(".csv"):
        filename += ".csv"
    try:
        df = pd.json_normalize(results)
        df.to_csv(filename, index=False)
        logging.info(f"Results exported to {filename}")
    except Exception as e:
        logging.error(f"Error exporting results to CSV: {e}")


def export_results_to_json(results: List[Dict], filename: str = "") -> None:
    """
    Exports SPARQL query results to a JSON file.

    Args:
        results (List[Dict]): The query results to export.
        filename (str): The output file name. Defaults to an auto-generated name if not provided.
    """
    if not filename:
        filename = f"{get_dir('files/results/')}/results_{get_timestamp()}.json"
    elif not filename.endswith(".json"):
        filename += ".json"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)
        logging.info(f"Results exported to {filename}")
    except Exception as e:
        logging.error(f"Error exporting results to JSON: {e}")
        raise

def get_timestamp() -> str:
    """
    Returns the current timestamp in a formatted string.

    Returns:
        str: The current timestamp in 'YYYY-MM-DD_HH-MM-SS' format.
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_dir(path: str) -> Path:
    """
    Ensures a directory exists and returns its absolute Path.

    Args:
        path (str): The directory path.

    Returns:
        Path: The resolved directory path.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return Path(path).resolve()