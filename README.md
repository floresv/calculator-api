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
