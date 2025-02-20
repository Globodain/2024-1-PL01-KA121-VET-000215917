from fastapi import APIRouter, HTTPException, Form, Query, UploadFile, File, Response
from fastapi.responses import HTMLResponse
from bson import ObjectId, Binary
from typing import Optional
from database import animals_collection
import os

router2 = APIRouter()

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

@router2.post("/animal/", response_class=HTMLResponse)
async def add_animal(
    family: str = Form(...),
    name: str = Form(...),
    origin: str = Form(...),
    description: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    if family.lower() not in VALID_FAMILIES:
        raise HTTPException(
            status_code=400,
            detail="Invalid animal family. Allowed families: mammals, birds, amphibians, reptiles, fishes."
        )
    existing = await animals_collection.find_one({
        "family": family.lower(),
        "name": name.lower()
    })
    if existing:
        raise HTTPException(status_code=400, detail="Animal already exists in the database.")
    image_name = None
    image_data = None
    if image:
        content = await image.read()
        image_name = image.filename
        image_data = Binary(content)
    document = {
        "family": family.lower(),
        "name": name.lower(),
        "origin": origin,
        "description": description,
        "image_name": image_name,
        "image_data": image_data
    }
    await animals_collection.insert_one(document)

    response_doc = obj_to_dict(document)
    if "image_data" in response_doc:
        del response_doc["image_data"]
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
                    color: #4CAF50;
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
            <h1>Animal added successfully</h1>
            <div class="animal-details">
                <p><strong>Family:</strong> {response_doc['family']}</p>
                <p><strong>Name:</strong> {response_doc['name']}</p>
                <p><strong>Origin:</strong> {response_doc['origin']}</p>
                <p><strong>Description:</strong> {response_doc['description']}</p>
                <img src="/app2/image/{response_doc['name']}" alt="{response_doc['name']}">
                <a href="/app2/animals/" class="btn-back">Back to Animal List</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router2.delete("/animal/", response_class=HTMLResponse)
async def delete_animal(family: str = Form(...), name: str = Form(...)):
    result = await animals_collection.delete_one({"family": family.lower(), "name": name.lower()})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found.")
    html_content = """
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
            </style>
        </head>
        <body>
            <h1>Animal deleted successfully</h1>
            <a href="/app2/animals/" class="btn-back">Back to Animal List</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router2.put("/animal/description/", response_class=HTMLResponse)
async def update_animal_description(family: str = Form(...), name: str = Form(...), description: str = Form(...)):
    result = await animals_collection.update_one(
        {"family": family.lower(), "name": name.lower()},
        {"$set": {"description": description}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Animal not found.")
    html_content = """
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
            </style>
        </head>
        <body>
            <h1>Animal description updated successfully</h1>
            <a href="/app2/animals/" class="btn-back">Back to Animal List</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router2.get("/animal_origin/", response_class=HTMLResponse)
async def get_animal_origin(family: str = Query(...), name: str = Query(...)):
    document = await animals_collection.find_one({"family": family.lower(), "name": name.lower()})
    if not document or "origin" not in document:
        raise HTTPException(status_code=404, detail="Animal origin not found.")
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
                p {{
                    font-size: 18px;
                    margin: 20px;
                }}
            </style>
        </head>
        <body>
            <h1>Animal Origin</h1>
            <p><strong>Family:</strong> {document['family'].capitalize()}</p>
            <p><strong>Name:</strong> {document['name'].capitalize()}</p>
            <p><strong>Origin:</strong> {document['origin'].capitalize()}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router2.get("/image/{animal_name}")
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
