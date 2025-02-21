# FastAPI Animal Management API

## Overview

This is a simple FastAPI-based REST API for managing animals. The API allows users to add, retrieve, update, delete, and filter animals stored in a MongoDB database.

## Features

- Add a new animal
- Retrieve all animals with pagination
- Retrieve a specific animal by ID
- Filter animals by name, type, and age range
- Update an animal's information
- Delete an animal
- Basic root endpoint returning "Hello World"

## Technologies Used

- **FastAPI** (Python-based web framework)
- **MongoDB** (NoSQL database)
- **Motor** (Asynchronous MongoDB driver)
- **Pydantic** (Data validation and serialization)

## Installation

### Prerequisites

Ensure you have Python 3.8+ installed on your machine.

### Steps to Run the Application

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Globodain/2024-1-PL01-KA121-VET-000215917.git
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Set up MongoDB:** Ensure MongoDB is running locally or use a remote MongoDB instance. Update the database connection settings accordingly in `database.py`.

4. **Run the FastAPI application:**

   ```sh
   uvicorn main:app --reload
   ```

5. **Access API documentation:** Open your browser and navigate to:

   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### Root Endpoint

- `GET /`\
  Returns "Hello World"

### Animal Management

- `POST /animals/`\
  Add a new animal to the database.

- `GET /animals/`\
  Retrieve all animals with optional pagination (`limit`, `skip`).

- `GET /animals/{animal_id}`\
  Retrieve a specific animal by ID.

- `GET /animals/filter/`\
  Retrieve animals based on filters (`name`, `type`, `min_age`, `max_age`).

- `PUT /animals/{animal_id}`\
  Update an animal's information.

- `DELETE /animals/{animal_id}`\
  Remove an animal from the database.

## Example Request

### Adding an Animal

```sh
curl -X 'POST' 'http://127.0.0.1:8000/animals/' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Buddy",
    "type": "Dog",
    "age": 5
  }'
```

### Response

```json
{
  "id": "60f8a3f7b24e4c5b9d9c5a6b",
  "name": "Buddy",
  "type": "Dog",
  "age": 5
}
```
