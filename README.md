# Project README

## Application Breakdown

This project consists of two main services designed to work together:
- **app**: The main application, which runs `lang_search.py` to interact with the meta search engine and perform additional tasks as defined in your script.
- **search_engine**: A SearxNG meta search engine, which aggregates search results from multiple sources and provides a single, unified list of results for user queries.

### What is a Meta Search Engine?

A meta search engine aggregates results from multiple search engines without directly crawling the web. When a user submits a query, the meta search engine forwards it to other search engines, gathers their responses, and presents a unified list of results. This allows users to see results from various sources in one place, broadening their access to diverse information. You can learn more about meta search engines on [Wikipedia](https://en.wikipedia.org/wiki/Metasearch_engine).

## Getting Started

This section provides instructions on installing Docker, setting up the project, and starting the application.

### Prerequisites

- **Docker** and **Docker Compose** are required for running the application. If these are not installed, follow the steps below.

### Installing Docker and Docker Compose

1. **Install Docker**:
   - **Windows / macOS**: Download Docker Desktop from [Docker's official site](https://www.docker.com/products/docker-desktop/), then install and launch Docker Desktop.
   - **Linux**: Follow the instructions on [Docker's Linux installation guide](https://docs.docker.com/engine/install/).

2. **Verify Docker Installation**:
   After installation, check if Docker is installed correctly by running:

   ```bash
   docker --version
   ```

3. **Install Docker Compose** (if not included with Docker):
   - **Windows/macOS**: Docker Compose comes pre-installed with Docker Desktop.
   - **Linux**: Install Docker Compose by following [Docker's installation instructions](https://docs.docker.com/compose/install/).

4. **Verify Docker Compose Installation**:
   Ensure Docker Compose is installed by running:

   ```bash
   docker-compose --version
   ```

### Setting Up the Project

1. **Clone the Repository**:
   Clone the repository to your local machine and navigate to the project directory:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Configure Search Engine Settings**:
   Make sure the configuration files for SearxNG, `settings.yml` and `uwsgi.ini`, are correctly set up. These files should be located in the root of the project directory.

3. **Starting the Services**:
   Build and start the services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the `app` container using the provided `Dockerfile`.
   - Set up the `search_engine` container for SearxNG with configurations from `settings.yml` and `uwsgi.ini`.
   - Start both containers, with the `app` service depending on the `search_engine` service.

4. **Accessing the Application**:
   - **App Service**: Runs `lang_search.py` inside `app_container`.
   - **Search Engine Service**: The SearxNG meta search engine can be accessed via `http://localhost:8080`.

5. **Stopping the Services**:
   To stop and remove all containers defined in `docker-compose.yml`, use:

   ```bash
   docker-compose down
   ```

### Additional Commands

- **Rebuild Without Cache**:
  ```bash
  docker-compose up --build --no-cache
  ```

- **Run in Detached Mode**:
  ```bash
  docker-compose up -d
  ```

## Troubleshooting

- If dependencies are missing, check `requirements.txt` or the Conda environment, update as needed, and rebuild the image.
- Ensure that `settings.yml` and `uwsgi.ini` are correctly configured for the `search_engine` service.
