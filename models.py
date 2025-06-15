from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from db import execute_query

class User(UserMixin):
    def __init__(self, id, username, email, is_librarian):
        self.id = id
        self.username = username
        self.email = email
        self.is_librarian = is_librarian

    @staticmethod
    def get(user_id):
        query = "SELECT * FROM users WHERE id = %s"
        result = execute_query(query, (user_id,), fetch=True)
        if result:
            user_data = result[0]
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                is_librarian=user_data['is_librarian']
            )
        return None

    @staticmethod
    def get_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        if result:
            user_data = result[0]
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                is_librarian=user_data['is_librarian']
            )
        return None

    @staticmethod
    def create(username, password, email, is_librarian=False):
        hashed_password = generate_password_hash(password)
        query = """
            INSERT INTO users (username, password, email, is_librarian)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (username, hashed_password, email, is_librarian))

    def check_password(self, password):
        query = "SELECT password FROM users WHERE id = %s"
        result = execute_query(query, (self.id,), fetch=True)
        if result:
            return check_password_hash(result[0]['password'], password)
        return False

class Book:
    def __init__(self, id, title, author, isbn, available):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    @staticmethod
    def get_all():
        query = "SELECT * FROM books"
        result = execute_query(query, fetch=True)
        return [Book(**book) for book in result] if result else []

    @staticmethod
    def get_by_id(book_id):
        query = "SELECT * FROM books WHERE id = %s"
        result = execute_query(query, (book_id,), fetch=True)
        if result:
            return Book(**result[0])
        return None

    @staticmethod
    def search(query_term):
        query = """
            SELECT * FROM books 
            WHERE title LIKE %s OR author LIKE %s
        """
        search_term = f"%{query_term}%"
        result = execute_query(query, (search_term, search_term), fetch=True)
        return [Book(**book) for book in result] if result else []

    @staticmethod
    def create(title, author, isbn):
        query = """
            INSERT INTO books (title, author, isbn)
            VALUES (%s, %s, %s)
        """
        execute_query(query, (title, author, isbn))

    @staticmethod
    def delete(book_id):
        query = "DELETE FROM books WHERE id = %s"
        execute_query(query, (book_id,))

    def update_availability(self, available):
        query = "UPDATE books SET available = %s WHERE id = %s"
        execute_query(query, (available, self.id)) 