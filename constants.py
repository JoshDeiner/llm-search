# constants.py

import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename="./logs/query.log", level=logging.INFO)


# Define the web search URL constant

# prod
WEB_SEARCH_URL = "http://search_engine:8080/search"

# dev
# WEB_SEARCH_URL = "http://localhost:8080/search"
