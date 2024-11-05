# tests/conftest.py
import os
import logging
import pytest

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to output to logs/tests.log
logging.basicConfig(
    filename="logs/tests.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",  # Overwrite the log file each test run
)

# Optional: A fixture to log debug information for specific tests
@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    logging.info(f"Starting test: {request.node.name}")
    yield
    logging.info(f"Finished test: {request.node.name}")
