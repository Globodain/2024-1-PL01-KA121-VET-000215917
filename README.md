### Microblog

This is a microblogging web application built using Flask, where users can sign up, log in, create posts, and update their profiles.

### Features
- User registration and authentication system
- Ability to create, edit, and delete posts
- Edit user profile details
- Request a password reset

### How to Use
1. Open your browser and go to http://127.0.0.1:5000/
2. Register a new account or log in to an existing one
3. Create, edit, and remove posts
4. Update your profile

### Project Organization
- **app** – Contains the main application code
- **forms.py** – Contains the form classes used within the application
- **models.py** – Defines the database structure and models
- **routes.py** – Includes route definitions and handlers
- **templates/** – Holds the HTML templates
- **static/** – Stores static resources like CSS and JavaScript
- **migrations** – Keeps the database migration files
- **tests/** – Contains unit tests
- **venv** – Includes files related to the virtual environment
- **config.py** – Stores configuration settings for the app

### Forms
- **LoginForm**
  - `username`: StringField (required)
  - `password`: PasswordField (required)
  - `remember_me`: BooleanField
  - `submit`: SubmitField

- **RegistrationForm**
  - `username`: StringField (required)
  - `email`: StringField (required, must pass email validation)
  - `password`: PasswordField (required)
  - `password2`: PasswordField (required, should match the first password)
  - `submit`: SubmitField

- **EditProfileForm**
  - `username`: StringField (required)
  - `about_me`: TextAreaField (optional, max 140 characters)
  - `submit`: SubmitField

- **PostForm**
  - `post`: TextAreaField (required, 1 to 140 characters)
  - `submit`: SubmitField

- **ResetPasswordRequestForm**
  - `email`: StringField (required, must be a valid email)
  - `submit`: SubmitField

- **ResetPasswordForm**
  - `password`: PasswordField (required)
  - `password2`: PasswordField (required, must match the first password)
  - `submit`: SubmitField


