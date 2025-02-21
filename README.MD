# Car API

This project is a FastAPI-based web service designed to manage car-related data and provide advanced search and statistics features. The API allows users to interact with a MongoDB database that contains detailed information about various cars, including their specifications, pricing, fuel type, and more.

## Table of Contents

- [Technologies](#technologies)
- [Endpoints](#api-endpoints)
- [Car Model](#car-model)
- [Screenshots](#screenshots)

## Technologies

- **FastAPI**: Web framework for building APIs with Python 3.7+ based on standard Python-type hints.
- **MongoDB**: NoSQL database for storing car data.
- **Pydantic**: Data validation and settings management.
- **PyMongo**: Python driver for MongoDB.
- **dotenv**: Load environment variables from a `.env` file.

## API Endpoints

### Cars

- **GET /cars**

  - Retrieve a list of all cars in the database.
  - Query Parameters:
    - `limit`: (optional) Number of cars to retrieve (default: 0, meaning no limit).

- **GET /cars/{vin}**

  - Retrieve a car by its VIN.
  - Path Parameter:
    - `vin`: Vehicle Identification Number (VIN) of the car.

- **POST /cars**

  - Add new cars to the database.
  - Body: List of `Car` objects to be added.

- **PUT /cars/{vin}**

  - Update a car's details by its VIN.
  - Path Parameter:
    - `vin`: Vehicle Identification Number (VIN) of the car.
  - Body: Fields to update in the car.

- **DELETE /cars/{vin}**
  - Delete a car by its VIN.
  - Path Parameter:
    - `vin`: Vehicle Identification Number (VIN) of the car.

### Car Search

- **GET /cars/search**
  - Search for cars based on various filters and sorting options.
  - Query Parameters:
    - `limit`: (optional) Number of cars to retrieve (default: 0).
    - `brand`: (optional) Brand of the car.
    - `model`: (optional) Model of the car.
    - `year`: (optional) Year of the car.
    - `milage`: (optional) Mileage of the car.
    - `vin`: (optional) VIN of the car.
    - `price`: (optional) Price of the car.
    - `year_from`: (optional) Minimum year of the car.
    - `year_to`: (optional) Maximum year of the car.
    - `milage_from`: (optional) Minimum mileage of the car.
    - `milage_to`: (optional) Maximum mileage of the car.
    - `price_from`: (optional) Minimum price of the car.
    - `price_to`: (optional) Maximum price of the car.
    - `sort_by`: (optional) Field to sort the results by (e.g., `brand_asc`, `price_desc`, etc.).

### Statistics

- **GET /cars/stats**
  - Retrieve statistical information about the cars in the database.
  - Response includes:
    - Most common brand.
    - Fastest car.
    - Most expensive car.
    - Most fuel-efficient car.
    - Most powerful car.
    - Most spacious car.
    - Most economical car.
    - Slowest car.
    - Cheapest car.
    - Least efficient car.
    - Least powerful car.
    - Least spacious car.
    - Least economical car.
    - Oldest car.
    - Newest car.
    - Average year.
    - Average maximum speed.
    - Average price.
    - Average trunk capacity.
    - Average acceleration.
    - Most common fuel type.
    - Most common transmission.

### Car Model

The Car model contains the following fields:

| Field                       | Type      | Description                                                            |
| --------------------------- | --------- | ---------------------------------------------------------------------- |
| `id`                        | `string`  | Unique identifier for the car (ObjectId).                              |
| `brand`                     | `string`  | Brand of the car (e.g., Toyota, BMW, etc.).                            |
| `model`                     | `string`  | Model of the car (e.g., Camry, 3 Series, etc.).                        |
| `vin`                       | `string`  | Vehicle Identification Number (unique).                                |
| `year`                      | `integer` | Manufacturing year of the car.                                         |
| `milage`                    | `integer` | Total mileage of the car in kilometers.                                |
| `price`                     | `integer` | Price of the car in the respective currency.                           |
| `gears`                     | `integer` | Number of gears in the car.                                            |
| `seats`                     | `integer` | Number of seats in the car.                                            |
| `doors`                     | `integer` | Number of doors in the car.                                            |
| `trunk_capacity`            | `float`   | The trunk capacity in liters.                                          |
| `max_speed`                 | `integer` | Maximum speed of the car in km/h.                                      |
| `acceleration`              | `float`   | Acceleration time (0-100 km/h) in seconds.                             |
| `horse_power`               | `integer` | Horsepower of the car's engine.                                        |
| `fuel_type`                 | `string`  | Type of fuel used by the car (e.g., gasoline, diesel, electric, etc.). |
| `transmission`              | `string`  | Transmission type (e.g., manual, automatic, semi-automatic, CVT).      |
| `fuel_consumption_city`     | `float`   | Fuel consumption in the city (L/100km).                                |
| `fuel_consumption_highway`  | `float`   | Fuel consumption on the highway (L/100km).                             |
| `fuel_consumption_combined` | `float`   | Combined fuel consumption (L/100km).                                   |
| `fuel_tank_capacity`        | `float`   | Capacity of the fuel tank in liters.                                   |
| `range_city`                | `float`   | Range on the city roads (km).                                          |
| `range_highway`             | `float`   | Range on the highway (km).                                             |
| `range_combined`            | `float`   | Combined range (km).                                                   |


### Screenshots

![Screenshot 1](https://raw.githubusercontent.com/Globodain/2024-1-PL01-KA121-VET-000215917/refs/heads/krzysztof-padlo-fastapi/screenshots/01.png)

![Screenshot 1](https://raw.githubusercontent.com/Globodain/2024-1-PL01-KA121-VET-000215917/refs/heads/krzysztof-padlo-fastapi/screenshots/02.png)

![Screenshot 1](https://raw.githubusercontent.com/Globodain/2024-1-PL01-KA121-VET-000215917/refs/heads/krzysztof-padlo-fastapi/screenshots/03.png)
