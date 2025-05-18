# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY simple-logger/log_data.py /app/

# Install required libraries
RUN pip install --upgrade pip
RUN pip install requests python-logging-loki prometheus_client

# Command to run the Python script
CMD ["python", "log_data.py"]
