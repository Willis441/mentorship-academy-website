# Motari Mentorship Academy - Flask Backend

A Flask-based backend for the Motari Mentorship Academy website with user authentication (login and signup).

## Features

- User registration (signup) with validation
- User authentication (login) with email or username
- Password hashing for security
- Session management
- SQLite database for user storage
- Flash messages for user feedback

## Setup Instructions

### 1. Install Python Dependencies

Make sure you have Python 3.7+ installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000` by default.

### 3. Access the Application

- Home page: `http://127.0.0.1:5000/`
- Login page: `http://127.0.0.1:5000/login`
- Signup page: `http://127.0.0.1:5000/signup`
- Logout: `http://127.0.0.1:5000/logout`

## Database

The application uses SQLite and will automatically create a `users.db` file when you first run the application. The database contains a `User` table with the following fields:

- `id` - Primary key
- `first_name` - User's first name
- `last_name` - User's last name
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Hashed password (not plain text)
- `created_at` - Account creation timestamp

## Project Structure

```
mentorship/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── users.db              # SQLite database (created automatically)
├── static/               # Static files (CSS, JS, images)
│   └── login.css
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── about.html
│   ├── contact.html
│   ├── events.html
│   └── mentors.html
└── assets/               # Static assets (existing)
    ├── css/
    ├── img/
    └── js/
```

## Usage

### Sign Up

1. Navigate to `/signup`
2. Fill in all required fields:
   - First Name
   - Last Name
   - Username (must be unique)
   - Email (must be unique)
   - Password (minimum 6 characters)
   - Confirm Password (must match)
3. Click "SIGN UP"
4. You'll be redirected to the login page upon successful registration

### Login

1. Navigate to `/login`
2. Enter your email or username
3. Enter your password
4. Click "LOG IN"
5. Upon successful login, you'll be redirected to the home page

### Logout

Navigate to `/logout` or add a logout link in your navigation menu.

## Security Notes

⚠️ **Important**: Before deploying to production:

1. Change the `SECRET_KEY` in `app.py` to a strong random secret key
2. Consider using environment variables for sensitive configuration
3. Use a production-grade database (PostgreSQL, MySQL) instead of SQLite
4. Implement HTTPS
5. Add rate limiting to prevent brute force attacks
6. Consider adding email verification for new accounts

## Development

To run in development mode with auto-reload:

```bash
python app.py
```

The `debug=True` setting enables:
- Automatic reloading on code changes
- Detailed error messages
- Debug mode (disable in production!)

## Future Enhancements

- Password reset functionality
- Email verification
- Profile management
- Remember me functionality
- Social login (Google/Facebook) integration




