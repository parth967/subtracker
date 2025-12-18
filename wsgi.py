#!/usr/bin/python3.10

"""
WSGI Configuration for InviteMe on PythonAnywhere

This file contains the WSGI configuration required to serve the InviteMe
Flask application on PythonAnywhere hosting platform.
"""

import sys
import os
from dotenv import load_dotenv

# Add your project directory to sys.path
project_home = '/home/Parth967/inviteme'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
load_dotenv(os.path.join(project_home, '.env.production'))

# Import your Flask application
from app import app as application

if __name__ == "__main__":
    application.run()