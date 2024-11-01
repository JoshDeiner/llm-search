# constants.py

import os

# Define the web search URL constant
# http://se_domain:8080/search"
WEB_SEARCH_URL = os.getenv("http://se_domain:8080/search", "http://localhost:8080/search")
