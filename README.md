# Dictionary Lookup API

A simple FastAPI backend service that provides dictionary lookup functionality using the Dictionary API.

## Features

- Healthcheck endpoint
- Word lookup endpoint that fetches definitions from an external dictionary API

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

3. Access the API documentation:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

- `GET /health`: Healthcheck endpoint
- `GET /lookup/{word}`: Lookup a word in the dictionary 