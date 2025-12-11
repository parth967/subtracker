#!/usr/bin/env python3
"""
WSGI entry point for PythonAnywhere deployment
"""

import sys
import os
from dotenv import load_dotenv

# Add your project directory to Python path
project_home = '/home/yourusername/mysite'  # Update this path
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

from app import app, db, email_monitor

# Initialize database and start email monitoring
with app.app_context():
    db.create_all()
    email_monitor.start_monitoring()

# This is what PythonAnywhere will use
application = app

if __name__ == "__main__":
    app.run()