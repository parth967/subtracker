#!/usr/bin/env python3
"""
Test MySQL connection for SubTracker Pro
"""

import os
from dotenv import load_dotenv
import pymysql

# Load environment
load_dotenv('.env.production')

def test_connection():
    """Test MySQL connection"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    print(f"🔗 Testing connection...")
    print(f"Database URL: {database_url.replace(':YOUR_MYSQL_PASSWORD', ':***PASSWORD***')}")
    
    # Parse the URL
    if 'YOUR_MYSQL_PASSWORD' in database_url:
        print("❌ You need to replace 'YOUR_MYSQL_PASSWORD' with your actual password in .env.production")
        return False
    
    try:
        # Extract connection details from URL
        # mysql+pymysql://Parth967:password@host/database
        url_parts = database_url.replace('mysql+pymysql://', '').split('@')
        user_pass = url_parts[0].split(':')
        host_db = url_parts[1].split('/')
        
        user = user_pass[0]
        password = user_pass[1]
        host = host_db[0]
        database = host_db[1].split('?')[0]
        
        print(f"User: {user}")
        print(f"Host: {host}")
        print(f"Database: {database}")
        print(f"Password: {'*' * len(password)}")
        
        # Test connection
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ MySQL connection successful!")
            
            # Check if tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Existing tables: {[table[0] for table in tables]}")
            
            cursor.close()
            connection.close()
            return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing SubTracker Pro MySQL Connection")
    print("=" * 50)
    
    if test_connection():
        print("\n✅ Connection test passed!")
        print("You can now run: python3.10 migrate_database.py")
    else:
        print("\n❌ Connection test failed!")
        print("Fix the issues above before proceeding.")