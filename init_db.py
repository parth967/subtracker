#!/usr/bin/env python3
"""
Database initialization script for SubTracker Pro on PythonAnywhere
Run this script to set up your MySQL database using same credentials as Budget Tracker
"""

import os
import sys
from dotenv import load_dotenv
from urllib.parse import quote_plus

def setup_environment():
    """Set up environment variables for database connection"""
    # Load production environment
    load_dotenv('.env.production')
    
    # Check if MYSQL_PASSWORD is set
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    if not mysql_password:
        print("❌ MYSQL_PASSWORD environment variable not set")
        print("This should be the same password you use for Budget Tracker")
        print("\nSet it with:")
        print("export MYSQL_PASSWORD='your-mysql-password'")
        return False
    
    # Construct the DATABASE_URL with the password
    database_url = f"mysql+pymysql://Parth967:{quote_plus(mysql_password)}@Parth967.mysql.pythonanywhere-services.com/Parth967$subtracker?charset=utf8mb4"
    os.environ['DATABASE_URL'] = database_url
    
    print("✅ Environment configured successfully")
    print(f"Database: Parth967$subtracker")
    print(f"Host: Parth967.mysql.pythonanywhere-services.com")
    
    return True

def initialize_database():
    """Initialize the database with tables and default data"""
    from app import app, db, init_default_data
    
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
            print(f"Error details: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Initializing SubTracker Pro Database...")
    print("Using same MySQL credentials as Budget Tracker")
    print("=" * 60)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Initialize database
    success = initialize_database()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Create the database 'Parth967$subtracker' in PythonAnywhere Databases tab")
        print("2. Make sure your web app is configured to use wsgi.py")
        print("3. Reload your web app in PythonAnywhere")
        print("4. Visit your site to start using SubTracker Pro!")
    else:
        print("\n❌ Database initialization failed")
        print("Make sure:")
        print("- MYSQL_PASSWORD environment variable is set")
        print("- Database 'Parth967$subtracker' exists in PythonAnywhere")
        print("- MySQL credentials are correct")