import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        # Create books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                BookID INT AUTO_INCREMENT PRIMARY KEY,
                BookName VARCHAR(255) NOT NULL,
                Author VARCHAR(255) NOT NULL,
                IsAvailable BOOLEAN DEFAULT TRUE
            )
        ''')

        # Create borrowed_books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowed_books (
                BorrowID INT AUTO_INCREMENT PRIMARY KEY,
                BookID INT,
                BorrowerName VARCHAR(255) NOT NULL,
                BorrowDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (BookID) REFERENCES books(BookID)
            )
        ''')

        # Create reviews table (optional)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                ReviewID INT AUTO_INCREMENT PRIMARY KEY,
                BookName VARCHAR(255) NOT NULL,
                Rating INT CHECK (rating >= 1 AND rating <= 5),
                Comment TEXT,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        connection.commit()
        cursor.close()
        connection.close()

def execute_query(query, params=None, fetch=False):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
            else:
                connection.commit()
                result = None
                
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None 