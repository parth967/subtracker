#!/usr/bin/env python3.10
"""
Debug Database Connection - Fixed for SQLAlchemy 2.5.1

This script uses the correct SQLAlchemy syntax to check the database connection.
"""

import os
from app import app, db
from sqlalchemy import text
from dotenv import load_dotenv

def debug_database_connection():
    """Debug the database connection with correct SQLAlchemy syntax"""
    print("🔍 Debugging Database Connection (Fixed)")
    print("=" * 50)
    
    # Check environment files
    print("📁 Environment configuration:")
    print(f"   DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    
    # Check Flask app configuration
    print(f"\n⚙️  Flask app configuration:")
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"   SQLALCHEMY_DATABASE_URI: {db_uri}")
        
        # Parse the database name from URI
        if 'mysql' in db_uri:
            if '/' in db_uri:
                db_name = db_uri.split('/')[-1].split('?')[0]
                print(f"   Expected database: {db_name}")
        
        # Test connection with correct SQLAlchemy 2.x syntax
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT DATABASE() as current_db"))
                current_db = result.fetchone()[0]
                print(f"   Actually connected to: {current_db}")
                
                if current_db != 'Parth967$inviteme':
                    print(f"   ❌ WRONG DATABASE! Should be: Parth967$inviteme")
                    print(f"   ❌ Currently using: {current_db}")
                    return False
                else:
                    print(f"   ✅ Connected to correct database")
                
                # Check tables in connected database
                print(f"\n📋 Tables in connected database:")
                result = conn.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result]
                print(f"   Tables: {tables}")
                
                # Check user table structure if it exists
                if 'user' in tables:
                    result = conn.execute(text("DESCRIBE user"))
                    columns = [row[0] for row in result]
                    print(f"   User table columns: {columns}")
                    
                    if 'username' not in columns:
                        print(f"   ❌ User table missing 'username' column!")
                        return False
                    else:
                        print(f"   ✅ User table has 'username' column")
                        
                        # Test a simple query
                        try:
                            result = conn.execute(text("SELECT COUNT(*) FROM user"))
                            count = result.fetchone()[0]
                            print(f"   ✅ User table accessible, {count} users exist")
                        except Exception as e:
                            print(f"   ❌ Cannot query user table: {e}")
                            return False
                else:
                    print(f"   ❌ User table not found!")
                    return False
                
                return True
                
        except Exception as e:
            print(f"   ❌ Connection test failed: {e}")
            return False

def main():
    success = debug_database_connection()
    
    if success:
        print(f"\n✅ Database connection is correct!")
        print(f"The issue must be elsewhere. Let me check the web app configuration.")
    else:
        print(f"\n❌ Database connection issue found!")
        print(f"Need to fix the database configuration.")

if __name__ == "__main__":
    main()