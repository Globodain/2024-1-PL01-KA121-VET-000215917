import math

from db import cars_collection
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/stats',name='Get cars statistics')
def get_all_cars_stats():
    try:
        pipeline = [
            {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        most_common_brand = list(cars_collection.aggregate(pipeline))
        most_common_brand = most_common_brand[0] if most_common_brand else None

        fastest_car = cars_collection.find_one(sort=[("max_speed", -1)])
        most_expensive_car = cars_collection.find_one(sort=[("price", -1)])
        most_efficient_car = cars_collection.find_one(sort=[("range_combined", -1)])
        most_powerful_car = cars_collection.find_one(sort=[("horse_power", -1)])
        most_spacious_car = cars_collection.find_one(sort=[("trunk_capacity", -1)])
        most_economical_car = cars_collection.find_one(sort=[("fuel_consumption_combined", 1)])

        slowest_car = cars_collection.find_one(sort=[("max_speed", 1)])
        cheapest_car = cars_collection.find_one(sort=[("price", 1)])
        least_efficient_car = cars_collection.find_one(sort=[("range_combined", 1)])
        least_powerful_car = cars_collection.find_one(sort=[("horse_power", 1)])
        least_spacious_car = cars_collection.find_one(sort=[("trunk_capacity", 1)])
        least_economical_car = cars_collection.find_one(sort=[("fuel_consumption_combined", -1)])

        oldest_car = cars_collection.find_one(sort=[("year", 1)])
        newest_car = cars_collection.find_one(sort=[("year", -1)])

        avg_year = list(cars_collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$year"}}}])) 
        avg_year = avg_year[0]["avg"] if avg_year else 0

        avg_maxspeed = list(cars_collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$max_speed"}}}]))
        avg_maxspeed = avg_maxspeed[0]["avg"] if avg_maxspeed else 0

        avg_price = list(cars_collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$price"}}}]))
        avg_price = avg_price[0]["avg"] if avg_price else 0

        avg_trunkcapacity = list(cars_collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$trunk_capacity"}}}]))
        avg_trunkcapacity = avg_trunkcapacity[0]["avg"] if avg_trunkcapacity else 0

        avg_acceleration = list(cars_collection.aggregate([{"$group": {"_id": None, "avg": {"$avg": "$acceleration"}}}]))
        avg_acceleration = avg_acceleration[0]["avg"] if avg_acceleration else 0

        most_common_fuel_type = list(cars_collection.aggregate([{"$group": {"_id": "$fuel_type", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 1}]))
        most_common_fuel_type = most_common_fuel_type[0] if most_common_fuel_type else None

        most_common_transmission = list(cars_collection.aggregate([{"$group": {"_id": "$transmission", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 1}]))
        most_common_transmission = most_common_transmission[0] if most_common_transmission else None

        def serialize_car(car):
            if car:
                car["_id"] = str(car["_id"])
            return car

        return {
            "most_common_brand": most_common_brand,
            "fastest_car": serialize_car(fastest_car),
            "most_expensive_car": serialize_car(most_expensive_car),
            "most_efficient_car": serialize_car(most_efficient_car),
            "most_powerful_car": serialize_car(most_powerful_car),
            "most_spacious_car": serialize_car(most_spacious_car),
            "most_economical_car": serialize_car(most_economical_car),
            "slowest_car": serialize_car(slowest_car),
            "cheapest_car": serialize_car(cheapest_car),
            "least_efficient_car": serialize_car(least_efficient_car),
            "least_powerful_car": serialize_car(least_powerful_car),
            "least_spacious_car": serialize_car(least_spacious_car),
            "least_economical_car": serialize_car(least_economical_car),
            "oldest_car": serialize_car(oldest_car),
            "newest_car": serialize_car(newest_car),
            "avg_year": round(avg_year),
            "avg_maxspeed": round(avg_maxspeed),
            "avg_price": round(avg_price),
            "avg_trunkcapacity": round(avg_trunkcapacity),
            "avg_acceleration": round(avg_acceleration, 2),
            "most_common_fuel_type": most_common_fuel_type,
            "most_common_transmission": most_common_transmission
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))