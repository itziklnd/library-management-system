from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from db import init_db, execute_query
from models import User, Book
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Initialize database
init_db()

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if User.get_by_username(username):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        User.create(username, password, email)
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Book routes
@app.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        # Search for books
        sql_query = """
            SELECT * FROM books 
            WHERE BookName LIKE %s OR Author LIKE %s
        """
        search_term = f"%{query}%"
        books = execute_query(sql_query, (search_term, search_term), fetch=True)
    else:
        # List all books
        books = execute_query("SELECT * FROM books", fetch=True)
    
    return render_template('index.html', books=books, query=query)

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        book_name = request.form['book_name']
        rating = request.form['rating']
        comment = request.form['comment']
        
        query = """
            INSERT INTO reviews (BookName, Rating, Comment)
            VALUES (%s, %s, %s)
        """
        execute_query(query, (book_name, rating, comment))
        flash('Review submitted successfully!')
        return redirect(url_for('index'))
    
    return render_template('review.html')

@app.route('/admin')
def admin():
    code = request.args.get('code')
    if code != 'LIB2025':
        return render_template('denied.html')
    return render_template('admin.html')

@app.route('/admin/borrow', methods=['GET', 'POST'])
def admin_borrow():
    code = request.args.get('code')
    if code != 'LIB2025':
        return render_template('denied.html')
    
    if request.method == 'POST':
        book_id = request.form['book_id']
        borrower_name = request.form['borrower_name']
        
        # Update book availability
        execute_query(
            "UPDATE books SET IsAvailable = FALSE WHERE BookID = %s",
            (book_id,)
        )
        
        # Log the borrowing
        execute_query(
            "INSERT INTO borrowed_books (BookID, BorrowerName) VALUES (%s, %s)",
            (book_id, borrower_name)
        )
        
        flash('Book borrowed successfully!')
        return redirect(url_for('admin_borrow', code='LIB2025'))
    
    # Get available books
    books = execute_query(
        "SELECT * FROM books WHERE IsAvailable = TRUE",
        fetch=True
    )
    
    return render_template('admin_borrow.html', books=books)

@app.route('/admin/add-book', methods=['GET', 'POST'])
def admin_add_book():
    code = request.args.get('code')
    if code != 'LIB2025':
        return render_template('denied.html')
    
    if request.method == 'POST':
        book_name = request.form['book_name']
        author = request.form['author']
        
        execute_query(
            "INSERT INTO books (BookName, Author) VALUES (%s, %s)",
            (book_name, author)
        )
        
        flash('Book added successfully!')
        return redirect(url_for('admin_add_book', code='LIB2025'))
    
    return render_template('admin_add_book.html')

# Librarian routes
@app.route('/librarian/books', methods=['GET', 'POST'])
@login_required
def manage_books():
    if not current_user.is_librarian:
        flash('Access denied')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        Book.create(title, author, isbn)
        flash('Book added successfully')
        return redirect(url_for('manage_books'))
    
    books = Book.get_all()
    return render_template('manage_books.html', books=books)

@app.route('/librarian/books/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_librarian:
        flash('Access denied')
        return redirect(url_for('index'))
    
    Book.delete(book_id)
    flash('Book deleted successfully')
    return redirect(url_for('manage_books'))

@app.route('/librarian/borrow', methods=['GET', 'POST'])
@login_required
def manage_borrows():
    if not current_user.is_librarian:
        flash('Access denied')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_id = request.form['user_id']
        
        query = """
            INSERT INTO borrowings (book_id, user_id)
            VALUES (%s, %s)
        """
        execute_query(query, (book_id, user_id))
        
        # Update book availability
        book = Book.get_by_id(book_id)
        book.update_availability(False)
        
        flash('Book borrowed successfully')
        return redirect(url_for('manage_borrows'))
    
    # Get all borrowings
    query = """
        SELECT b.*, bk.title, u.username
        FROM borrowings b
        JOIN books bk ON b.book_id = bk.id
        JOIN users u ON b.user_id = u.id
        WHERE b.returned_at IS NULL
    """
    borrowings = execute_query(query, fetch=True)
    
    # Get available books
    books = Book.get_all()
    available_books = [b for b in books if b.available]
    
    # Get all users
    users = execute_query("SELECT id, username FROM users", fetch=True)
    
    return render_template('manage_borrows.html', 
                         borrowings=borrowings,
                         available_books=available_books,
                         users=users)

@app.route('/librarian/return/<int:borrowing_id>', methods=['POST'])
@login_required
def return_book(borrowing_id):
    if not current_user.is_librarian:
        flash('Access denied')
        return redirect(url_for('index'))
    
    # Update borrowing record
    query = """
        UPDATE borrowings 
        SET returned_at = CURRENT_TIMESTAMP 
        WHERE id = %s
    """
    execute_query(query, (borrowing_id,))
    
    # Get book_id from borrowing
    query = "SELECT book_id FROM borrowings WHERE id = %s"
    result = execute_query(query, (borrowing_id,), fetch=True)
    if result:
        book = Book.get_by_id(result[0]['book_id'])
        book.update_availability(True)
    
    flash('Book returned successfully')
    return redirect(url_for('manage_borrows'))

if __name__ == '__main__':
    app.run(debug=True) 