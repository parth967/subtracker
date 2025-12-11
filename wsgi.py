#!/usr/bin/env python3
"""
WSGI entry point for SubTracker Pro on PythonAnywhere
Using same MySQL credentials as Budget Tracker
"""

import sys
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Add your project directory to Python path
project_home = '/home/Parth967/mysite'  # Updated with your username
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load production environment variables
load_dotenv(os.path.join(project_home, '.env.production'))

# Set up DATABASE_URL with MYSQL_PASSWORD
mysql_password = os.environ.get('MYSQL_PASSWORD')
if mysql_password:
    database_url = f"mysql+pymysql://Parth967:{quote_plus(mysql_password)}@Parth967.mysql.pythonanywhere-services.com/Parth967$subtracker?charset=utf8mb4"
    os.environ['DATABASE_URL'] = database_url

from app import app, db

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        print("SubTracker Pro database tables created successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

# This is what PythonAnywhere will use
application = app

if __name__ == "__main__":
    app.run()