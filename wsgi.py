#!/usr/bin/env python3
"""
WSGI entry point for SubTracker Pro on PythonAnywhere
"""

import sys
import os
from dotenv import load_dotenv

# Add your project directory to Python path
project_home = '/home/Parth967/mysite/subtracker'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load production environment variables
load_dotenv(os.path.join(project_home, '.env.production'))

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


echo 'export MYSQL_PASSWORD="your-actual-mysql-password"' >> ~/.bashrc