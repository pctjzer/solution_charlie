# Markr - Marking as a Service with Redis
> **Note:** I completed the solution by combining my knowledge of Python, Flask, Docker, and what I remembered about Redis with additional insights and assistance from GPT-4 and Copilot. The intention of this was to allow me to quickly validate ideas, get back up to speed fairly quickly, and ensure I was following best practices. I’m happy to walk through the code and decisions made, demonstrating my understanding and how I effectively used GPT-4 and Copilot as a supplementary resource. 

## Overview
This project is a prototype for Markr, a data ingestion and processing microservice for analyzing student performance on multiple-choice exams. It uses Redis for storing and retrieving data. The project is split into two services:
1. **Submission Service:** Importing exam results from an XML file via an HTTP POST request.
2. **Retrieval Service:** Retrieving aggregated test results via an HTTP GET request.

Two separate microservices have been created in distinct containers to enhance flexibility, ease management, and improve scalability in production.

## Assumptions
- The provided XML format may contain extraneous fields that can be ignored.
- Only the `<summary-marks>` element is used for calculating scores.
- Duplicate entries for a student's test results should keep the highest score.
- For this prototype, the database will reset upon restart, assuming data persistence is not critical for this prototype.
- The choice of Redis has been selected for speed and for later ease of implementation into a production environment. 
- Waitress has been used for this prototype being more suited to production use, as there is the assumption of little change being possible once shared with boss. 
- The prototype must have a basic testing service to make sure there is no issues with services after startup.

## Running the Services

### Using Docker
1. Build and start the services:
   ```bash
   docker-compose up --build
   ```
2. The submission service will be available at `http://localhost:5001`.
3. The retrieval service will be available at `http://localhost:5002`.

### API Endpoints

#### Submission Service

**Import Data**
- **URL:** `/import`
- **Method:** POST
- **Content-Type:** `text/xml+markr`
- **Description:** Accepts an XML document containing multiple-choice test results.
- **Example:**
  ```bash
  curl -X POST -H 'Content-Type: text/xml+markr' http://localhost:5001/import -d @data/sample_results.xml
  ```

#### Retrieval Service

**Retrieve Aggregate Results**
- **URL:** `/results/<test-id>/aggregate`
- **Method:** GET
- **Description:** Returns the mean, count, and percentiles (25th, 50th, 75th) of the scores for a given test ID.
- **Example:**
  ```bash
  curl http://localhost:5002/results/1234/aggregate
  ```

**Retrieve All Results**
- **URL:** `/results`
- **Method:** GET
- **Description:** Returns a list of all stored test results.
- **Example:**
  ```bash
  curl http://localhost:5002/results
  ```

### Health Endpoint
Both the Submission and Retrieval services include a health endpoint to check their status. This endpoint is designed to be compatible with Kubernetes health checks. Yes this is because I care about the DevOps gang. 

**Health Check**
- **URL:** `/health`
- **Method:** GET
- **Description:** Returns a status indicating the service is running.
- **Example:**

To check the health of the Submission service:

```bash
curl http://localhost:5001/health
```
To check the health of the Retrieval service:

```bash
curl http://localhost:5002/health
```
**Response:**
```text
{"status":"UP"}
```

### Kubernetes Health Check Configuration
In your Kubernetes deployment configuration, you can use the following settings to configure liveness and readiness probes for the services:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5001  # 5001 for retrieval service
  initialDelaySeconds: 5
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 5002  # 5002 for retrieval service
  initialDelaySeconds: 5
  periodSeconds: 10
```
This should enable the Kubernetes sercice to have an idea of when services are up, we can update the detail of health checks later.

## Running Tests

To run the tests, use Docker Compose:

```bash
docker-compose up --build tests
```

This will build the testing container, run the tests, and display the results in your terminal.


## File Descriptions
- `submission_service/app/__init__.py`: Initializes the Flask application for the submission service.
- `submission_service/app/submit_service.py`: Handles the import of XML data and stores it in Redis.
- `retrieval_service/app/__init__.py`: Initializes the Flask application for the retrieval service.
- `retrieval_service/app/retrieve_service.py`: Retrieves and calculates aggregate test results from Redis.
- `data/sample_results.xml`: Sample XML data for testing.
- `tests/test_services.py`: Unit tests for the services.
- `tests/Dockerfile`: Docker configuration for running the tests.
- `requirements.txt`: Lists the Python dependencies.
- `Dockerfile`: Docker configuration for the submission and retrieval services.
- `docker-compose.yml`: Docker Compose configuration.

## Tips for Scaling
- **Horizontal Scaling**: Deploy multiple instances of the submission and retrieval services using a container orchestration tool like Kubernetes. Use a Redis cluster to handle increased data and request loads.
- **Persistence**: Configure Redis to use persistence options like RDB snapshots or AOF logs to ensure data is saved to disk.
- **Monitoring**: Use monitoring tools like Prometheus and Grafana to monitor the health and performance of the application and Redis instances.
- **Caching**: Implement caching strategies to reduce load on Redis and improve response times for frequently accessed data.
