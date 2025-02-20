from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import HTMLResponse
from bson import ObjectId
from database import animals_collection
import os

router1 = APIRouter()

VALID_FAMILIES = ["mammals", "birds", "amphibians", "reptiles", "fishes"]

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

def obj_to_dict(obj):
    if isinstance(obj, dict):
        return {k: obj_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [obj_to_dict(v) for v in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj

def capitalize_words(text: str) -> str:
    return ' '.join([word.capitalize() for word in text.split()])

@router1.get("/animal/", response_class=HTMLResponse)
async def get_animal(family: str = Query(...), name: str = Query(...)):
    doc = await animals_collection.find_one({"family": family.lower(), "name": name.lower()})
    if not doc:
        raise HTTPException(status_code=404, detail="Animal not found.")
    doc = obj_to_dict(doc)
    if "image_data" in doc:
        del doc["image_data"]

    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                h1 {{
                    text-align: center;
                    color: #FC8004;
                    margin-top: 50px;
                    font-size: 36px;
                }}
                .animal-details {{
                    max-width: 800px;
                    margin: auto;
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }}
                .animal-details p {{
                    font-size: 18px;
                    margin: 10px 0;
                }}
                .animal-details img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    margin-top: 20px;
                }}
                .btn-back {{
                    display: block;
                    width: 200px;
                    margin: 30px auto 0;
                    padding: 12px;
                    background-color: #FC8004;
                    color: white;
                    font-size: 18px;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 8px;
                    transition: background-color 0.3s;
                }}
                .btn-back:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <h1>Animal Details</h1>
            <div class="animal-details">
                <p><strong>Family:</strong> {capitalize_words(doc['family'])}</p>
                <p><strong>Name:</strong> {capitalize_words(doc['name'])}</p>
                <p><strong>Description:</strong> {doc['description']}</p>
    """
    if "origin" in doc:
        html_content += f"<p><strong>Origin:</strong> {capitalize_words(doc['origin'])}</p>"
    html_content += f"""
                <img src="/app1/image/{doc['name']}" alt="{doc['name']}">
                <a href="/app1/animals/" class="btn-back">Back to Animal List</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router1.get("/animals/", response_class=HTMLResponse)
async def list_animals():
    cursor = animals_collection.find({})
    animals = []
    async for document in cursor:
        doc = obj_to_dict(document)
        animals.append(doc)

    animal_list_html = "<ul style='padding-left: 20px;'>"
    for animal in animals:
        animal_list_html += f"""
        <li style='font-size: 20px; margin: 15px 0;'>
            {capitalize_words(animal['family'])} - {capitalize_words(animal['name'])} - 
            <a href='/app1/animal/?family={animal['family']}&name={animal['name']}' style='color: #FC8004; text-decoration: none; font-weight: 600;'>View Details</a>
        </li>
        """
    animal_list_html += "</ul>"
    
    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                h1 {{
                    text-align: center;
                    color: #FC8004;
                    padding: 30px;
                    font-size: 36px;
                }}
                ul {{
                    list-style-type: none;
                    text-align: center;
                    padding: 0;
                }}
                li {{
                    margin: 20px;
                }}
                a {{
                    color: #FC8004;
                    font-size: 18px;
                    text-decoration: none;
                    padding: 6px 12px;
                    border-radius: 8px;
                    transition: background-color 0.3s;
                    font-weight: 500;
                }}
                a:hover {{
                    background-color: #f1f1f1;
                }}
            </style>
        </head>
        <body>
            <h1>List of Animals</h1>
            {animal_list_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router1.get("/image/{animal_name}")
async def get_image(animal_name: str):
    doc = await animals_collection.find_one({"name": animal_name.lower()})
    if not doc or "image_data" not in doc or doc["image_data"] is None:
        raise HTTPException(status_code=404, detail="Image not found.")
    image_data = doc["image_data"]

    ext = os.path.splitext(doc["image_name"])[1].lower() if doc["image_name"] else ".bin"
    if ext == ".png":
        media_type = "image/png"
    elif ext in [".jpg", ".jpeg"]:
        media_type = "image/jpeg"
    else:
        media_type = "application/octet-stream"
    return Response(content=image_data, media_type=media_type)
