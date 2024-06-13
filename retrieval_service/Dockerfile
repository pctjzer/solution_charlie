# Use the official Python image from the DockerHub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5002 for the retrieval service
EXPOSE 5002

# Define the command to run the application
CMD ["sh", "run.sh"]
