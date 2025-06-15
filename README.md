# Library Management System

A Flask-based web application for managing a library system with user and librarian roles.

## Features

### User Features
- View list of books and their availability
- Search for books by title or author
- Submit book reviews with ratings

### Librarian Features
- Manage book borrowing
- Track book borrowing history
- Add or remove books from the system

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up MySQL database and update the configuration in `.env`
5. Run the application:
   ```bash
   python app.py
   ```

## Database Setup

1. Create a MySQL database named `library_db`
2. The application will automatically create the necessary tables on first run

## Environment Variables

Create a `.env` file with the following variables:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=library_db
SECRET_KEY=your_secret_key
```

## Project Structure

```
library_system/
├── app.py              # Main application file
├── db.py              # Database connection and queries
├── models.py          # Database models
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
└── requirements.txt   # Project dependencies
``` 