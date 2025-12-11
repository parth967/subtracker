#!/usr/bin/env python3
"""
Database initialization script for SubTracker Pro on PythonAnywhere
Run this script to set up your MySQL database
"""

import os
import sys
from dotenv import load_dotenv

# Load production environment
load_dotenv('.env.production')

from app import app, db, init_default_data

def initialize_database():
    """Initialize the database with tables and default data"""
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            print("Adding default categories...")
            init_default_data()
            print("✅ Default categories added!")
            
            print("🎉 Database initialization complete!")
            print("Your SubTracker Pro is ready to use!")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Initializing SubTracker Pro Database...")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    if not os.environ.get('DATABASE_URL'):
        print("❌ DATABASE_URL not found in environment variables")
        print("Make sure you've created .env.production with your MySQL details")
        sys.exit(1)
    
    success = initialize_database()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Make sure your web app is configured to use wsgi.py")
        print("2. Reload your web app in PythonAnywhere")
        print("3. Visit your site to start using SubTracker Pro!")
    else:
        print("\n❌ Database initialization failed")
        print("Check your MySQL credentials in .env.production")