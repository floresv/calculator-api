# calculator-api

Calculator Backend

# Calculator API

This is a Flask API for a calculator application with a PostgreSQL database. It includes the following endpoints:

## Authentication

- `POST /v1/login`: Log in a user
- `POST /v1/logout`: Log out a user
- `POST /v1/signup`: Register a new user

## User

- `GET /v1/me`: Get details of the current user

## Operations

- `POST /v1/operations`: Create a new operation
- `GET /v1/operations`: Get all operation records
- `DELETE /v1/operations/<id>`: Delete an operation record

## Setup

1. Create a PostgreSQL database
2. Create a `.env` file with the following variables:
   - `DATABASE_URL`: URL for the PostgreSQL database
   - `SECRET_KEY`: Secret key for Flask app
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `flask run`

## Docker

### Running Tests with Docker Compose

This guide outlines how to leverage Docker Compose to build and execute tests for your Python application.

Prerequisites:

- Docker installed on your system.
- Docker Compose installed on your system.
- A docker-compose.yml file configured for your project.
- A requirements.txt file listing project dependencies.
- A test framework like pytest or unittest integrated into your project.

`docker-compose build`

This command constructs Docker images for all services defined in your docker-compose.yml file. These images encapsulate your application and any necessary dependencies, ensuring a clean and isolated test environment.


### Running Services

`docker-compose up`

This command initiates all services defined in your docker-compose.yml file. This typically includes your application service and any database or other services crucial for testing.

### Executing Tests

`docker-compose exec api python manage.py cov`

This command executes the following steps:

- It utilizes docker-compose exec to enter an interactive shell session within the container named api (assuming your application service is named api in docker-compose.yml).
- Inside the container, it executes the python manage.py cov command. This command (specific to the coverage library) typically runs your test suite and generates reports detailing code coverage.