from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
# Database configuration - supports both SQLite (local) and PostgreSQL (production)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'


# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.name}>'


# Newsletter Model
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Newsletter {self.email}>'


# Database tables will be created when app starts (see if __name__ == '__main__')


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username', '').strip()
        password = request.form.get('password', '')

        if not email_or_username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')

        # Check if input is email or username
        user = User.query.filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email/username or password', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = []
        if not all([first_name, last_name, username, email, password, confirm_password]):
            errors.append('Please fill in all fields')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('signup.html')

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('signup.html')

        # Create new user
        try:
            password_hash = generate_password_hash(password)
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password_hash=password_hash
            )
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


# Template routes for other pages
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/mentors')
def mentors():
    return render_template('mentors.html')


@app.route('/events')
def events():
    return render_template('events.html')




# Serve static files from assets and photos directories
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)


@app.route('/photos/<path:filename>')
def photos(filename):
    return send_from_directory('photos', filename)


# Admin/Database viewing routes
@app.route('/admin')
def admin():
    """Admin dashboard to view database records"""
    users = User.query.order_by(User.created_at.desc()).all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    newsletters = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    
    return render_template('admin.html', 
                         users=users, 
                         contacts=contacts, 
                         newsletters=newsletters)


# Form handling routes
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission (works for both AJAX and regular)
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # Validation
        if not all([name, email, subject, message]):
            if is_ajax:
                return 'Please fill in all fields', 400
            flash('Please fill in all fields', 'error')
            return redirect(url_for('contact'))

        # Validate email format
        if '@' not in email or '.' not in email:
            if is_ajax:
                return 'Invalid email address', 400
            flash('Invalid email address', 'error')
            return redirect(url_for('contact'))

        # Save to database
        try:
            new_contact = Contact(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(new_contact)
            db.session.commit()

            if is_ajax:
                return 'OK', 200
            flash('Your message has been sent. Thank you!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            if is_ajax:
                return 'An error occurred. Please try again.', 500
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('contact'))

    return render_template('contact.html')


# Newsletter subscription route
@app.route('/newsletter', methods=['POST'])
def newsletter_subscribe():
    email = request.form.get('email', '').strip()
    
    # Check if this is an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Validation
    if not email:
        if is_ajax:
            return 'Please enter your email address', 400
        flash('Please enter your email address', 'error')
        return redirect(request.referrer or url_for('index'))

    # Validate email format
    if '@' not in email or '.' not in email:
        if is_ajax:
            return 'Invalid email address', 400
        flash('Invalid email address', 'error')
        return redirect(request.referrer or url_for('index'))

    # Check if email already subscribed
    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        if is_ajax:
            return 'OK', 200  # Already subscribed but return OK
        flash('This email is already subscribed to our newsletter!', 'info')
        return redirect(request.referrer or url_for('index'))

    # Save to database
    try:
        new_subscriber = Newsletter(email=email)
        db.session.add(new_subscriber)
        db.session.commit()

        if is_ajax:
            return 'OK', 200
        flash('Thank you for subscribing to our newsletter!', 'success')
        return redirect(request.referrer or url_for('index'))
    except Exception as e:
        db.session.rollback()
        if is_ajax:
            return 'An error occurred. Please try again.', 500
        flash('An error occurred. Please try again.', 'error')
        return redirect(request.referrer or url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # For production: use environment variable for port, disable debug
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
