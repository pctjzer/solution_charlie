# Use the official Python image from the DockerHub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .. /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r submission_service/requirements.txt
RUN pip install --no-cache-dir -r retrieval_service/requirements.txt
RUN pip install requests

# Run the tests
CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
