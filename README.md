# Microblog

This is a microblogging web application built with Flask. Users can register, log in, create posts, and edit their profiles.

## Features

- User registration and authentication
- Create, edit, and delete posts
- Edit user profile
- Request password reset

## Usage

- Open your web browser and go to `http://127.0.0.1:5000/`
- Register a new account or log in with an existing account
- Create, edit, and delete posts
- Edit your profile

## Project Structure

- [app](http://_vscodecontentref_/0) - Contains the application code
  - `forms.py` - Contains the form classes used in the application
  - `models.py` - Contains the database models
  - `routes.py` - Contains the route handlers
  - `templates/` - Contains the HTML templates
  - `static/` - Contains static files like CSS and JavaScript
- [migrations](http://_vscodecontentref_/1) - Contains the database migration files
- `tests/` - Contains the unit tests
- [venv](http://_vscodecontentref_/2) - Contains the virtual environment files
- [config.py](http://_vscodecontentref_/3) - Contains the configuration settings

## Forms

### LoginForm

- `username` - StringField, required
- `password` - PasswordField, required
- `remember_me` - BooleanField
- `submit` - SubmitField

### RegistrationForm

- `username` - StringField, required
- `email` - StringField, required, email validation
- `password` - PasswordField, required
- `password2` - PasswordField, required, must match `password`
- `submit` - SubmitField

### EditProfileForm

- `username` - StringField, required
- `about_me` - TextAreaField, optional, max length 140
- `submit` - SubmitField

### EmptyForm

- `submit` - SubmitField

### PostForm

- `post` - TextAreaField, required, min length 1, max length 140
- `submit` - SubmitField

### ResetPasswordRequestForm

- `email` - StringField, required, email validation
- `submit` - SubmitField

### ResetPasswordForm

- `password` - PasswordField, required
- `password2` - PasswordField, required, must match `password`
- `submit` - SubmitField

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
