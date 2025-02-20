from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes import router as animal_router
from fastapi.staticfiles import StaticFiles
from database import database
from fastapi import APIRouter

app = FastAPI()
router = APIRouter()

app.include_router(animal_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Animal API</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="navbar">
                <a href="/">Home</a>
                <a href="/animals">View all Animals</a>
            </div>
            <div class="container">
                <h1>Welcome to the Animal API!</h1>
            </div>
        </body>
    </html>
    """

@app.get("/animals", response_class=HTMLResponse)
async def get_all_animals_html(filter_age: int = None, filter_species: str = None, search_name: str = None):
    query = {}

    if filter_age is not None:
        query["age"] = filter_age
    if filter_species:
        query["species"] = {"$regex": filter_species, "$options": "i"}
    if search_name:
        query["name"] = {"$regex": search_name, "$options": "i"}

    animals_cursor = database.animals.find(query)
    animals = await animals_cursor.to_list(length=100)

    if search_name:
        animals.sort(key=lambda x: (x['name'].lower().find(search_name.lower()), x['name']))

    animal_list_html = """
<html>
    <head>
        <title>Animals List</title>
        <link rel="stylesheet" href="/static/style.css">
        <script>
            function toggleFilterPanel() {
                const panel = document.getElementById("filterPanel");
                panel.style.display = panel.style.display === "none" ? "block" : "none";
            }

            function applyFilter() {
                const age = document.getElementById("filterAge").value;
                const species = document.getElementById("filterSpecies").value;
                const name = document.getElementById("filterName").value;
                let url = "/animals?";
                if (age) url += `filter_age=${age}&`;
                if (species) url += `filter_species=${species}&`;
                if (name) url += `search_name=${name}&`;
                window.location.href = url;
            }

            function resetFilter() {
                document.getElementById("filterAge").value = "";
                document.getElementById("filterSpecies").value = "";
                document.getElementById("filterName").value = "";
                window.location.href = "/animals";  
            }
        </script>
        <style>
            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                margin-bottom: 20px;
            }

            .header-container h1 {
                margin: 0;
                text-align: center;
                width: 100%;
                margin-left: 85px;
            }

            .header-container button {
                background-color: #4CAF50;
                color: white;
                border-radius: 20px;
                padding: 10px 15px;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }
        
            .animal-cards {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }

            .card {
                background: #f4f4f4;
                padding: 15px;
                border-radius: 8px;
                width: 220px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                text-align: center;
            }

            .card a {
                display: inline-block;
                margin-top: 10px;
                padding: 5px 10px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }

            .card a:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <a href="/">Home</a>
            <a href="/animals">View all Animals</a>
        </div>
        <div id="filterPanel" style="display:none;">
            <h3>Filter Animals</h3>
            <label for="filterAge">Age:</label>
            <input type="number" id="filterAge" name="age" placeholder="Age"><br>
            <label for="filterSpecies">Species:</label>
            <input type="text" id="filterSpecies" name="species" placeholder="Species"><br>
            <label for="filterName">Name:</label>
            <input type="text" id="filterName" name="name" placeholder="Search by name"><br><br>
            <button onclick="applyFilter()">Apply Filter</button>
            <button onclick="resetFilter()">Reset Filter</button>
        </div>
        <div class="container">
            <div class="header-container">
                <h1>All Animals</h1>
                <button onclick="toggleFilterPanel()"><i>&#x1F50D;</i> Filter</button>
            </div>
            <div class="animal-cards">
    """
    
    for animal in animals:
        animal_list_html += f"""
        <div class="card">
            <h3>{animal['name']}</h3>
            <p><strong>Species:</strong> {animal['species']}</p>
            <p><strong>Age:</strong> {animal['age']}</p>
            <p>{animal.get('description', 'No description available')}</p>
        </div>
        """
    animal_list_html += """
                </div>
            </div>
        </body>
    </html>
    """
    return animal_list_html