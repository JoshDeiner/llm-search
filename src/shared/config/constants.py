
# constants.py

import logging

logging.basicConfig(filename="./logs/query.log", level=logging.INFO)


# Define the web search URL constant

# prod
# WEB_SEARCH_URL:str = "http://search_engine:8080/search"

# dev
WEB_SEARCH_URL: str = "http://localhost:8080/search"