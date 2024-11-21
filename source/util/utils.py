import logging
from typing import List

def select_from_list(options: List[str], prompt: str = "Select an option: ") -> str:
    """Prompts the user to select an option from a list."""
    if not options:
        raise ValueError("The list of options is empty.")
    if len(options) == 1:
        return options[0]
    print("\n".join(f"{i+1}. {option}" for i, option in enumerate(options)))
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def list_and_select_query(queries: dict) -> str:
    """Lists available queries and allows the user to select one."""
    logging.info("Listing available queries...")
    options = list(queries.keys())
    return select_from_list(options, "Select a query by number: ")
