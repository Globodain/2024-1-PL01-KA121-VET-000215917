from fastapi import FastAPI, APIRouter, HTTPException, Form, UploadFile
from fastapi.responses import HTMLResponse
from bson import ObjectId
from database import animals_collection
import os
import json

app = FastAPI()
router_ws = APIRouter()

from app1 import router1
app.include_router(router1, prefix="/app1")

from app2 import router2
app.include_router(router2, prefix="/app2")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background: linear-gradient(135deg, #F4A9FF, #EB61FF);
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }
                h1 {
                    color: black;
                    text-align: center;
                    padding: 20px;
                }
                p {
                    font-size: 18px;
                    text-align: center;
                }
                .menu {
                    background-color: white;
                    padding: 20px;
                    margin-top: 30px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                    width: 60%;
                    margin-left: auto;
                    margin-right: auto;
                    color: #3498db;
                }
                .menu h2 {
                    text-align: center;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                    text-align: center;
                }
                li {
                    margin: 10px 0;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                    font-size: 20px;
                }
                a:hover {
                    text-decoration: underline;
                }
                h2{
                    color: black;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Animal Database!</h1>
            <div class="menu">
                <h2>Choose an application to proceed:</h2>
                <ul>
                    <li><a href="/app1/animals_form/">List of Animals</a></li>
                    <li><a href="/app2/options/">Animal Database Options</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app1/animals_form/", response_class=HTMLResponse)
async def animals_form():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background: linear-gradient(135deg, #F4A9FF, #EB61FF);
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }
                h2 {
                    color: black;
                    text-align: center;
                    margin-top: 50px;
                }
                form {
                    max-width: 600px;
                    margin: auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                }
                label {
                    font-size: 18px;
                    margin-bottom: 10px;
                    display: block;
                }
                select, input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 15px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    background-color: #3498db;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #ffb24d;
                }
                #animalDetails {
                    margin-top: 30px;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                }
                img {
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                }
            </style>
            <script>
                async function fetchAnimals(family) {
                    const response = await fetch(`/get_animals_by_family?family=${family}`);
                    const data = await response.json();
                    const animalsList = document.getElementById("animalsList");
                    animalsList.innerHTML = "";
                    data.forEach(animal => {
                        const option = document.createElement("option");
                        option.value = animal.name;
                        option.text = animal.name.charAt(0).toUpperCase() + animal.name.slice(1);
                        animalsList.add(option);
                    });
                }
                
                async function displayAnimalDetails(animalName) {
                    const family = document.getElementById("familySelect").value;
                    const response = await fetch(`/get_animal_details?family=${family}&name=${animalName.toLowerCase()}`);
                    const data = await response.json();
                    const animalDetails = document.getElementById("animalDetails");
                    animalDetails.innerHTML = `
                        <h3>Animal Details</h3>
                        <p><strong>Family:</strong> ${data.family.charAt(0).toUpperCase() + data.family.slice(1)}</p>
                        <p><strong>Name:</strong> ${data.name.charAt(0).toUpperCase() + data.name.slice(1)}</p>
                        <p><strong>Origin:</strong> ${data.origin}</p>
                        <p><strong>Description:</strong> ${data.description}</p>
                        <img src="/app1/image/${data.name}" alt="${data.name}">
                    `;
                }

                function confirmDisplayDetails() {
                    const animalsList = document.getElementById("animalsList");
                    const selectedAnimal = animalsList.options[animalsList.selectedIndex].value;
                    if (selectedAnimal) {
                        displayAnimalDetails(selectedAnimal);
                    } else {
                        alert("Please select an animal to display details.");
                    }
                }
            </script>
        </head>
        <body>
            <h2>Select Animal Family and Animal</h2>
            <form>
                <label for="familySelect">Select Family:</label>
                <select id="familySelect" name="family" onchange="fetchAnimals(this.value)">
                    <option value="">--Select a Family--</option>
                    <option value="mammals">Mammals</option>
                    <option value="birds">Birds</option>
                    <option value="amphibians">Amphibians</option>
                    <option value="reptiles">Reptiles</option>
                    <option value="fishes">Fishes</option>
                </select><br><br>

                <label for="animalsList">Select Animal:</label>
                <select id="animalsList" name="animal">
                    <option value="">--Select an Animal--</option>
                </select><br><br>

                <button type="button" onclick="confirmDisplayDetails()">Display Details</button>
            </form>
            <div id="animalDetails"></div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/get_animals_by_family")
async def get_animals_by_family(family: str):
    cursor = animals_collection.find({"family": family.lower()})
    animals = []
    async for document in cursor:
        animals.append({"name": document["name"]})
    return animals

@app.get("/get_animal_details")
async def get_animal_details(family: str, name: str):
    document = await animals_collection.find_one({"family": family.lower(), "name": name.lower()})
    if not document:
        raise HTTPException(status_code=404, detail="Animal not found.")
    return {
        "family": document["family"],
        "name": document["name"],
        "origin": document.get("origin", ""),
        "description": document.get("description", "")
    }

@app.get("/app2/options/", response_class=HTMLResponse)
async def app2_options():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background: linear-gradient(135deg, #F4A9FF, #EB61FF);
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }
                h1 {
                    color: black;
                    text-align: center;
                    padding: 20px;
                }
                .menu {
                    background-color: white;
                    padding: 20px;
                    margin-top: 30px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                    width: 60%;
                    margin-left: auto;
                    margin-right: auto;
                }
                .menu{
                    text-align: center;
                    color: #3498db;
                }
                h2{
                    text-align: center;
                    color: black;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                    text-align: center;
                }
                li {
                    margin: 10px 0;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                    font-size: 20px;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Animal Database Options</h1>
            <div class="menu">
                <h2>Choose an option</h2>
                <ul>
                    <li><a href="/app2/add_animal_form/">Add Animal to Database</a></li>
                    <li><a href="/app2/delete_animal_form/">Delete Animal from Database</a></li>
                    <li><a href="/app2/update_animal_description_form/">Update Animal Description</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app2/add_animal_form/", response_class=HTMLResponse)
async def add_animal_form():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background: linear-gradient(135deg, #F4A9FF, #EB61FF);
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }
                h1 {
                    text-align: center;
                    color: #3498db;
                    padding: 20px;
                }
                form {
                    max-width: 600px;
                    margin: auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                }
                label {
                    font-size: 18px;
                    margin-bottom: 10px;
                    display: block;
                }
                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 15px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    background-color: #3498db;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #ffb24d;
                }
            </style>
        </head>
        <body>
            <h1>Add Animal</h1>
            <form action="/app2/animal/" method="post" enctype="multipart/form-data">
                <label for="family">Family:</label>
                <input type="text" id="family" name="family" required><br><br>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br><br>
                <label for="origin">Origin:</label>
                <input type="text" id="origin" name="origin" required><br><br>
                <label for="description">Description:</label>
                <textarea id="description" name="description" required></textarea><br><br>
                <label for="image">Image:</label>
                <input type="file" id="image" name="image"><br><br>
                <input type="submit" value="Add Animal">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app2/delete_animal_form/", response_class=HTMLResponse)
async def delete_animal_form():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background: linear-gradient(135deg, #F4A9FF, #EB61FF);
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }
                h1 {
                    text-align: center;
                    color: #3498db;
                    padding: 20px;
                }
                form {
                    max-width: 600px;
                    margin: auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                }
                label {
                    font-size: 18px;
                    margin-bottom: 10px;
                    display: block;
                }
                input {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 15px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    background-color: #3498db;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #ffb24d;
                }
            </style>
        </head>
        <body>
            <h1>Delete Animal</h1>
            <form action="/app2/delete_animal/" method="delete">
                <label for="family">Family:</label>
                <input type="text" id="family" name="family" required><br><br>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br><br>
                <input type="submit" value="Delete Animal">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app2/update_animal_description_form/", response_class=HTMLResponse)
async def update_animal_description_form():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    background: linear-gradient(135deg, #F4A9FF, #EB61FF);
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }
                h1 {
                    text-align: center;
                    color: #3498db;
                    padding: 20px;
                }
                form {
                    max-width: 600px;
                    margin: auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                }
                label {
                    font-size: 18px;
                    margin-bottom: 10px;
                    display: block;
                }
                textarea {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 15px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    background-color: #3498db;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #ffb24d;
                }
            </style>
        </head>
        <body>
            <h1>Update Animal Description</h1>
            <form action="/app2/update_animal_description/" method="post">
                <label for="family">Family:</label>
                <input type="text" id="family" name="family" required><br><br>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br><br>
                <label for="description">New Description:</label>
                <textarea id="description" name="description" required></textarea><br><br>
                <input type="submit" value="Update Description">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
