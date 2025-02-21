# Flask Blog Application

## Overview
This is a simple blog application built using Flask. It allows users to register, log in, create posts, follow other users, and reset their passwords.

## Features
- User authentication (registration, login, logout)
- User profiles with editable information
- Creating, viewing, and deleting posts
- Following and unfollowing other users
- Paginated home and explore feeds
- Password reset via email

## Technologies Used
- **Flask** (Python web framework)
- **Flask-Login** (User authentication)
- **Flask-WTF** (Forms handling)
- **Flask-SQLAlchemy** (ORM for database interactions)
- **SQLite / PostgreSQL** (Database)
- **Bootstrap** (Frontend styling)

## Installation
### Prerequisites
- Python 3.8+
- Virtual environment (optional but recommended)

### Steps to Run the Application
1. **Clone the repository:**
   ```sh
   git clone https://github.com/Globodain/2024-1-PL01-KA121-VET-000215917.git
   cd flask-blog
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Set up the database:**
   ```sh
   flask db upgrade
   ```

4. **Run the Flask application:**
   ```sh
   flask run
   ```

5. **Access the application:**
   Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## API Endpoints & Routes

### Authentication
- `GET /login` – Display login form
- `POST /login` – Log in user
- `GET /logout` – Log out user
- `GET /register` – Display registration form
- `POST /register` – Register a new user

### User Management
- `GET /user/<username>` – View user profile
- `GET /edit_profile` – Edit user profile
- `POST /follow/<username>` – Follow a user
- `POST /unfollow/<username>` – Unfollow a user

### Blog Posts
- `GET /` or `GET /index` – View posts from followed users (home page)
- `GET /explore` – View all posts (explore page)
- `POST /index` – Create a new post

### Password Reset
- `GET /reset_password_request` – Request a password reset email
- `POST /reset_password_request` – Send password reset instructions
- `GET /reset_password/<token>` – Reset password form
- `POST /reset_password/<token>` – Submit new password

## Example Request
### Creating a Post
```sh
curl -X 'POST' 'http://127.0.0.1:5000/index' \
  -H 'Content-Type: application/json' \
  -d '{
    "post": "Hello, this is my first blog post!"
  }'
```

### Response
```json
{
  "message": "Your post is now live!"
}
```
