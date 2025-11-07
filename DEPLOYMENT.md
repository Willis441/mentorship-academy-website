# Deployment Guide - Motari Mentorship Academy

This guide shows you how to deploy your Flask application to various platforms.

## Prerequisites

1. **Git** installed on your computer
2. **GitHub account** (free)
3. Your Flask app working locally

---

## Option 1: Render (Recommended - Free Tier Available)

[Render](https://render.com) offers a free tier with automatic deployments from GitHub.

### Step 1: Prepare Your App

Create a `Procfile` (no extension) in your project root:
```
web: gunicorn app:app
```

### Step 2: Create `requirements.txt` (already exists, but verify)
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
gunicorn==21.2.0
```

### Step 3: Update app.py for Production

Add this at the bottom of `app.py`:

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Step 4: Create `.env` file for local development

Create `.env` file (add to `.gitignore`):
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///users.db
```

### Step 5: Initialize Git and Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 6: Deploy on Render

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: mentorship-academy (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes)

### Step 7: Set Environment Variables

In Render dashboard, go to "Environment" tab and add:
- `SECRET_KEY`: Generate a random secret key (use `python -c "import secrets; print(secrets.token_hex(16))"`)
- `FLASK_ENV`: production

Your app will be live at: `https://your-app-name.onrender.com`

---

## Option 2: Railway (Easy & Fast)

[Railway](https://railway.app) is great for quick deployments.

### Steps:

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repository
4. Railway auto-detects Flask, but add:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Add environment variables in Railway dashboard:
   - `SECRET_KEY`: (generate one)
   - `PORT`: (auto-set by Railway)
6. Click "Deploy"

Your app will be live automatically!

---

## Option 3: PythonAnywhere (Good for Beginners)

[PythonAnywhere](https://www.pythonanywhere.com) offers free hosting for Python apps.

### Steps:

1. Sign up at https://www.pythonanywhere.com
2. Upload your files via Files tab
3. Open Bash console and run:
   ```bash
   pip3.10 install --user flask flask-sqlalchemy gunicorn
   ```
4. Create WSGI file: `mysite.wsgi`
   ```python
   import sys
   import os
   
   path = '/home/YOUR_USERNAME/mysite'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from app import app as application
   
   if __name__ == "__main__":
       application.run()
   ```
5. Go to Web tab → Add new web app
6. Configure your app
7. Reload and your site is live!

---

## Option 4: Heroku (Requires Credit Card)

### Steps:

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Create `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Login and deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

---

## Important: Pre-Deployment Checklist

### 1. Update app.py for Production

```python
# At the bottom of app.py
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # For production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### 2. Update Database Configuration

For production, use PostgreSQL (most platforms provide it for free):

```python
# In app.py, update database config
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///users.db'
```

### 3. Create `.gitignore`

Create `.gitignore` file:
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.db
instance/
.DS_Store
.env
*.log
```

### 4. Security Checklist

- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Set `debug=False` in production
- ✅ Use environment variables for sensitive data
- ✅ Never commit `.env` file

---

## Quick Start: Render Deployment

**Easiest method - Follow these steps:**

1. **Create Procfile**:
   ```
   web: gunicorn app:app
   ```

2. **Update requirements.txt** (add gunicorn):
   ```
   Flask==3.0.0
   Flask-SQLAlchemy==3.1.1
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```

3. **Update app.py** (add at bottom):
   ```python
   if __name__ == '__main__':
       with app.app_context():
           db.create_all()
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port, debug=False)
   ```

4. **Push to GitHub**

5. **Deploy on Render** (see steps above)

---

## Troubleshooting

### Database Issues
- Most platforms reset the database on restart (free tier)
- Consider using PostgreSQL addon for persistent data
- Or use external database service (Supabase, PlanetScale)

### Static Files Not Loading
- Make sure paths start with `/` (already done)
- Check `url_for()` is used correctly

### Forms Not Working
- Verify environment variables are set
- Check logs in platform dashboard
- Ensure database tables are created

---

## Recommended: Render.com

**Why Render?**
- ✅ Free tier available
- ✅ Automatic SSL/HTTPS
- ✅ Easy GitHub integration
- ✅ Free PostgreSQL database option
- ✅ Good documentation

**Get started:** https://render.com

---

## Need Help?

Check platform-specific documentation:
- Render: https://render.com/docs
- Railway: https://docs.railway.app
- PythonAnywhere: https://help.pythonanywhere.com


