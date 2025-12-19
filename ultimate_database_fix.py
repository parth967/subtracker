#!/usr/bin/env python3.10
"""
Ultimate Database Fix

The web app is connecting to the wrong database. This script will:
1. Check which database the web app is actually using
2. Force it to use the correct database
3. Verify the fix works
"""

import pymysql
import os

def check_all_databases():
    """Check all possible databases to find where the wrong schema is"""
    print("🔍 Checking All Possible Databases")
    print("=" * 50)
    
    # Possible databases
    databases_to_check = [
        'Parth967$inviteme',
        'Parth967$subtracker', 
        'Parth967$default'
    ]
    
    for db_name in databases_to_check:
        print(f"\n📋 Checking database: {db_name}")
        try:
            conn = pymysql.connect(
                host='Parth967.mysql.pythonanywhere-services.com',
                user='Parth967',
                password='khushali979797',
                database=db_name,
                charset='utf8mb4'
            )
            cursor = conn.cursor()
            
            # Check if user table exists
            cursor.execute("SHOW TABLES LIKE 'user'")
            if cursor.fetchone():
                print(f"   ✅ Has 'user' table")
                
                # Check user table structure
                cursor.execute("DESCRIBE user")
                columns = [row[0] for row in cursor.fetchall()]
                print(f"   Columns: {columns}")
                
                if 'username' in columns:
                    print(f"   ✅ Has 'username' column - THIS IS THE CORRECT DATABASE")
                else:
                    print(f"   ❌ Missing 'username' column - THIS IS THE WRONG DATABASE")
                    print(f"   ⚠️  WEB APP MIGHT BE USING THIS ONE!")
            else:
                print(f"   ❌ No 'user' table")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Cannot connect to {db_name}: {e}")

def fix_database_routing():
    """Fix the database routing issue"""
    print(f"\n🔧 Fixing Database Routing")
    print("=" * 50)
    
    # Step 1: Create a new app.py that forces the correct database
    print("📝 Creating fixed app.py...")
    
    # Read current app.py
    try:
        with open('app.py', 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Cannot read app.py: {e}")
        return False
    
    # Create backup
    try:
        with open('app.py.backup', 'w') as f:
            f.write(content)
        print("✅ Backup created: app.py.backup")
    except Exception as e:
        print(f"⚠️  Cannot create backup: {e}")
    
    # Find and replace the database configuration
    old_config_patterns = [
        "app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inviteme.db')",
        "app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')",
        "mysql_url = 'mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4'"
    ]
    
    # New hardcoded configuration
    new_config = """# HARDCODED DATABASE CONFIGURATION - DO NOT CHANGE
# This forces the app to use the correct InviteMe database
INVITEME_DATABASE_URL = 'mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = INVITEME_DATABASE_URL
print(f"🔧 FORCED DATABASE: {INVITEME_DATABASE_URL}")"""
    
    # Replace any existing database configuration
    for pattern in old_config_patterns:
        if pattern in content:
            content = content.replace(pattern, new_config)
            print(f"✅ Replaced database configuration")
            break
    else:
        # If no pattern found, add after SECRET_KEY
        secret_line = "app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')"
        if secret_line in content:
            content = content.replace(secret_line, secret_line + "\n\n" + new_config)
            print(f"✅ Added database configuration")
    
    # Write the fixed app.py
    try:
        with open('app.py', 'w') as f:
            f.write(content)
        print("✅ Fixed app.py written")
    except Exception as e:
        print(f"❌ Cannot write app.py: {e}")
        return False
    
    return True

def test_fixed_app():
    """Test the fixed app configuration"""
    print(f"\n🧪 Testing Fixed App")
    print("=" * 50)
    
    try:
        # Remove cached module
        import sys
        if 'app' in sys.modules:
            del sys.modules['app']
        
        # Import the fixed app
        from app import app, db
        
        with app.app_context():
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            print(f"📍 Database URI: {db_uri}")
            
            if 'Parth967$inviteme' in db_uri:
                print("✅ App configured for correct database")
                
                # Test actual connection
                from sqlalchemy import text
                with db.engine.connect() as conn:
                    result = conn.execute(text("SELECT DATABASE() as db"))
                    current_db = result.fetchone()[0]
                    print(f"✅ Actually connected to: {current_db}")
                    
                    if current_db == 'Parth967$inviteme':
                        print("✅ Connection verified - using correct database!")
                        
                        # Test user table
                        result = conn.execute(text("DESCRIBE user"))
                        columns = [row[0] for row in result]
                        print(f"✅ User table columns: {columns}")
                        
                        if 'username' in columns:
                            print("✅ Username column exists - fix successful!")
                            return True
                        else:
                            print("❌ Username column still missing")
                            return False
                    else:
                        print(f"❌ Still connected to wrong database: {current_db}")
                        return False
            else:
                print(f"❌ App still configured for wrong database: {db_uri}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🚀 Ultimate InviteMe Database Fix")
    print("=" * 50)
    
    # Step 1: Check all databases
    check_all_databases()
    
    # Step 2: Fix the routing
    if fix_database_routing():
        print("✅ Database routing fixed")
    else:
        print("❌ Failed to fix database routing")
        return False
    
    # Step 3: Test the fix
    if test_fixed_app():
        print("\n" + "=" * 50)
        print("🎉 ULTIMATE FIX SUCCESSFUL!")
        print("=" * 50)
        
        print("\n✅ What was fixed:")
        print("✅ Identified wrong database connection")
        print("✅ Hardcoded correct database URL")
        print("✅ Verified connection to Parth967$inviteme")
        print("✅ Confirmed username column exists")
        
        print("\n🚀 FINAL STEP:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit: https://parth967.pythonanywhere.com")
        print("4. Your InviteMe platform should now work!")
        
        print("\n🎊 Database routing issue RESOLVED!")
        
    else:
        print("\n❌ Ultimate fix failed!")
        print("Restore backup with: cp app.py.backup app.py")
    
    return True

if __name__ == "__main__":
    main()