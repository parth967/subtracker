#!/usr/bin/env python3.10
"""
Debug Database Connection

This script shows exactly which database the web app is connecting to
and compares it with what we expect.
"""

import os
from app import app, db
from dotenv import load_dotenv

def debug_database_connection():
    """Debug the database connection"""
    print("🔍 Debugging Database Connection")
    print("=" * 50)
    
    # Check environment files
    print("📁 Checking environment files...")
    
    env_files = ['.env', '.env.production']
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ Found: {env_file}")
            with open(env_file, 'r') as f:
                content = f.read()
                if 'DATABASE_URL' in content:
                    for line in content.split('\n'):
                        if 'DATABASE_URL' in line and not line.startswith('#'):
                            print(f"   {line}")
        else:
            print(f"❌ Missing: {env_file}")
    
    # Check environment variables
    print(f"\n🌍 Environment variables:")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}")
    print(f"   DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    
    # Check Flask app configuration
    print(f"\n⚙️  Flask app configuration:")
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"   SQLALCHEMY_DATABASE_URI: {db_uri}")
        
        # Parse the database name from URI
        if 'mysql' in db_uri:
            # Extract database name
            if '/' in db_uri:
                db_name = db_uri.split('/')[-1].split('?')[0]
                print(f"   Database name: {db_name}")
            
            # Test connection
            try:
                result = db.engine.execute("SELECT DATABASE() as current_db")
                current_db = result.fetchone()[0]
                print(f"   Actually connected to: {current_db}")
                
                if current_db != 'Parth967$inviteme':
                    print(f"   ❌ WRONG DATABASE! Should be: Parth967$inviteme")
                    print(f"   ❌ Currently using: {current_db}")
                else:
                    print(f"   ✅ Connected to correct database")
                
            except Exception as e:
                print(f"   ❌ Connection test failed: {e}")
    
    # Check what tables exist in the connected database
    print(f"\n📋 Tables in connected database:")
    try:
        with app.app_context():
            result = db.engine.execute("SHOW TABLES")
            tables = [row[0] for row in result]
            print(f"   Tables: {tables}")
            
            # Check user table structure if it exists
            if 'user' in tables:
                result = db.engine.execute("DESCRIBE user")
                columns = [row[0] for row in result]
                print(f"   User table columns: {columns}")
                
                if 'username' not in columns:
                    print(f"   ❌ User table missing 'username' column!")
                    print(f"   ❌ This confirms we're connected to wrong database")
                else:
                    print(f"   ✅ User table has 'username' column")
            
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")

def main():
    debug_database_connection()

if __name__ == "__main__":
    main()