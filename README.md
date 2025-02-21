# Car API

This project is a FastAPI-based application for managing a collection of cars. It provides endpoints for creating, retrieving, updating, and deleting car records, as well as searching and sorting cars based on various criteria.

## Files

- `app.py`: Contains the FastAPI application and endpoint definitions.
- `models.py`: Contains the Pydantic models used for data validation and serialization.

## Installation

1. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI application:
    ```sh
    uvicorn app:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## How It Works

### Application Structure

- **`app.py`**: This file contains the main FastAPI application and defines the endpoints for interacting with the car collection. It includes endpoints for creating, retrieving, updating, and deleting cars, as well as searching and sorting cars.
- **`models.py`**: This file defines the Pydantic models used for data validation and serialization. It includes models for car data and search parameters.

### Endpoints

#### Create a Car

- **URL**: `/cars/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "brand": "Toyota",
        "model": "Camry",
        "production_year": 2020,
        "price": 24000.0,
        "horsepower": 203,
        "engine_displacement": 2.5,
        "dors": 4,
        "color": "White",
        "mileage": 15000,
        "fuel_type": "Gasoline",
        "fuel_consumption": 28.0,
        "max_speed": 130,
        "image": "https://example.com/toyota_camry.jpg",
        "transmission": "Automatic",
        "drivetrain": "FWD",
        "seats": 5,
        "description": "A reliable and fuel-efficient sedan."
    }
    ```
- **Response**: Returns the created car object.

#### Get All Cars

- **URL**: `/cars/all/`
- **Method**: `GET`
- **Query Parameters**:
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Number of records to return (default: 10)
    - `sort_by`: Field to sort by (optional)
    - `sort_order`: Sort order (`asc` or `desc`, default: `asc`)
- **Response**: Returns a list of car objects.

#### Search Cars

- **URL**: `/cars/`
- **Method**: `GET`
- **Query Parameters**:
    - `brand`: Brand of the car (optional)
    - `model`: Model of the car (optional)
    - `year`: Production year of the car (optional)
    - `min_price`: Minimum price of the car (optional)
    - `max_price`: Maximum price of the car (optional)
    - `color`: Color of the car (optional)
    - `mileage`: Mileage of the car (optional)
    - `limit`: Number of results to return (default: 10)
    - `sort_by`: Field to sort by (optional)
    - `sort_order`: Sort order (`asc` or `desc`, default: `asc`)
- **Response**: Returns a list of car objects matching the search criteria.

#### Update a Car

- **URL**: `/cars/{car_id}`
- **Method**: `PUT`
- **Request Body**: Partial or full car object with fields to update.
- **Response**: Returns the updated car object.

#### Delete a Car

- **URL**: `/cars/{car_id}`
- **Method**: `DELETE`
- **Response**: Returns a status message indicating the car was deleted.

### Models

#### Car

The `Car` model represents a car object with the following fields:

- `id`: Optional string (automatically generated)
- `brand`: Optional string
- `model`: Optional string
- `production_year`: Optional integer
- `price`: Optional float
- `horsepower`: Optional integer
- `engine_displacement`: Optional float
- `dors`: Optional integer (default: 5)
- `color`: Optional string
- `mileage`: Optional integer
- `fuel_type`: Optional string
- `fuel_consumption`: Optional float
- `max_speed`: Optional integer
- `image`: Optional string (URL)
- `transmission`: Optional string
- `drivetrain`: Optional string
- `seats`: Optional integer
- `description`: Optional string

#### CarSearchParams

The `CarSearchParams` model is used for search queries and includes the following fields:

- `brand`: Optional string (min length: 1)
- `model`: Optional string
- `year`: Optional integer
- `min_price`: Optional float
- `max_price`: Optional float
- `color`: Optional string
- `mileage`: Optional integer
- `limit`: Integer (default: 10)
- `sort_by`: Optional `SortFields` enum
- `sort_order`: Optional `SortOrder` enum (default: `asc`)

#### SortFields

The `SortFields` enum defines the fields that can be used for sorting:

- `brand`
- `model`
- `production_year`
- `price`
- `horsepower`
- `mileage`
- `color`

#### SortOrder

The `SortOrder` enum defines the sort order:

- `asc`: Ascending
- `desc`: Descending

## Examples

### Creating a Car

To create a new car, send a `POST` request to `/cars/` with the car details in the request body:

```sh
curl -X POST "http://127.0.0.1:8000/cars/" -H "Content-Type: application/json" -d '{
    "brand": "Toyota",
    "model": "Camry",
    "production_year": 2020,
    "price": 24000.0,
    "horsepower": 203,
    "engine_displacement": 2.5,
    "dors": 4,
    "color": "White",
    "mileage": 15000,
    "fuel_type": "Gasoline",
    "fuel_consumption": 28.0,
    "max_speed": 130,
    "image": "https://example.com/toyota_camry.jpg",
    "transmission": "Automatic",
    "drivetrain": "FWD",
    "seats": 5,
    "description": "A reliable and fuel-efficient sedan."
}'