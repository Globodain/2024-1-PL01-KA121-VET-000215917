### Animal Database Application

This web application, built with FastAPI, allows users to view, manage, and update information in an animal database. It provides both a user interface for animal exploration and admin functionalities to modify the database.

### Features
- View and search animals by family (mammals, birds, reptiles, etc.)
- Display detailed information about each animal
- Add new animals to the database
- Delete animals from the database
- Update animal descriptions

### How to Use
1. Open your browser and go to [http://localhost:8000]
2. Choose an option: 
   - View the list of animals and their details
   - Admin options to add, delete, or update animals
3. Admins can use the `/app2/options/` page to manage animals
4. Select an animal family and view details like description and origin

### Project Organization
- **app1/** – Contains the main application for viewing animal data
- **app2/** – Admin features for managing the animal database
- **database.py** – Handles database interactions and connection to MongoDB
- **main.py** – The FastAPI application setup and routing
- **templates/** – Stores HTML templates for the front-end pages
- **static/** – Stores static assets like images for animals




