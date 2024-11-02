import subprocess
import logging

def cli():
    # Prompt user for a search term
    search_term = input("Enter your search term: ")
    logging.info(search_term)

    return search_term

    
if __name__ == "__main__":
    cli()
