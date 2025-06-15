# Library Management System

A modern web application for managing a library system, built with Flask and MySQL.

## Features

### User Features
- View list of books and their availability
- Search for books by title or author
- Submit book reviews with ratings
- User authentication system

### Librarian Features
- Manage book borrowing
- Track book borrowing history
- Add or remove books from the system
- Special librarian dashboard

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
- Create a MySQL database named `library_db`
- Update the `.env` file with your database credentials

5. Run the application:
```bash
python app.py
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

## Database Schema

### Users Table
- id (Primary Key)
- username
- password (hashed)
- email
- is_librarian
- created_at

### Books Table
- id (Primary Key)
- title
- author
- isbn
- available
- created_at

### Borrowings Table
- id (Primary Key)
- book_id (Foreign Key)
- user_id (Foreign Key)
- borrowed_at
- returned_at

### Reviews Table
- id (Primary Key)
- book_id (Foreign Key)
- user_id (Foreign Key)
- rating
- review_text
- created_at

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)
Project Link: [https://github.com/yourusername/library-management-system](https://github.com/yourusername/library-management-system) 