FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Specify the command to run when the container starts
CMD ["python", "lang_search.py"]
