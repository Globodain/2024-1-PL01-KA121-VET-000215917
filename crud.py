from bson import ObjectId
from database import animals_collection

def create_animal(animal):
    animal_dict = animal.dict()
    result = animals_collection.insert_one(animal_dict)
    animal_dict["id"] = str(result.inserted_id)
    return animal_dict

def get_all_animals():
    animals = animals_collection.find()
    result = []
    for animal in animals:
        animal["id"] = str(animal["_id"])
        del animal["_id"]
        result.append(animal)
    return result

def get_animal_by_id(animal_id):
    try:
        obj_id = ObjectId(animal_id)
    except Exception:
        return None

    animal = animals_collection.find_one({"_id": obj_id})
    if animal:
        animal["id"] = str(animal["_id"])
        del animal["_id"]
        return animal
    return None

def update_animal(animal_id, animal):
    try:
        obj_id = ObjectId(animal_id)
    except Exception:
        return None

    update_data = animal.dict()
    updated = animals_collection.update_one({"_id": obj_id}, {"$set": update_data})
    if updated.modified_count:
        return get_animal_by_id(animal_id)
    return None

def delete_animal(animal_id):
    try:
        obj_id = ObjectId(animal_id)
    except Exception:
        return {"deleted_count": 0}

    result = animals_collection.delete_one({"_id": obj_id})
    return {"deleted_count": result.deleted_count}

def filter_animals(name=None, species=None, min_age=None, max_age=None):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if species:
        query["species"] = {"$regex": species, "$options": "i"}
    if min_age is not None and max_age is not None:
        query["age"] = {"$gte": min_age, "$lte": max_age}
    elif min_age is not None:
        query["age"] = {"$gte": min_age}
    elif max_age is not None:
        query["age"] = {"$lte": max_age}

    animals = animals_collection.find(query)
    result = []
    for animal in animals:
        animal["id"] = str(animal["_id"])
        del animal["_id"]
        result.append(animal)
    return result
