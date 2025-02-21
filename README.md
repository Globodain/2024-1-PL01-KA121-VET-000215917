# Microblog Project

Microblog Project, a full-featured microblog application built with Flask. This project is a dynamic web application with user authentication, profile management, posting, following, and RESTful API endpoints. It is inspired by the Flask Mega-Tutorial by Miguel Grinberg. 

## Features

- **User Authentication & Registration:** Secure sign-up, login, and logout with password hashing.
- **User Profiles:** View and edit profiles, including avatar generation via Gravatar.
- **Posting:** Create and view posts with pagination.
- **Followers System:** Follow and unfollow users; view posts from followed users.
- **Password Reset:** Request a password reset via email.
- **RESTful API:** JSON endpoints for user and token management.
- **Error Handling:** Custom 404 and 500 error pages.
- **Unit Testing:** Comprehensive tests to ensure proper functionality.

## Installation

### Prerequisites

- Python 3.7 or later
- Virtual environment (recommended)
- A mail server configuration for sending emails (for password resets)
- SQLite (default) or another database supported by SQLAlchemy

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd microblog
