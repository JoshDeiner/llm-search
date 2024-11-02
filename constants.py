# constants.py

import os

# Define the web search URL constant

is_docker = os.getenv("IS_DOCKER")
WEB_SEARCH_URL = (
    "http://localhost:8080/search" if is_docker else "http://search_engine:8080/search"
)
