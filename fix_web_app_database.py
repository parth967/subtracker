#!/usr/bin/env python3.10
"""
Fix Web App Database Configuration

This script ensures the web application uses the correct MySQL database
by updating the app.py configuration and creating a proper .env file.
"""

import os
import shutil

def fix_web_app_database():
    """Fix the web app database configuration"""
    print("🔧 Fixing Web App Database Configuration")
    print("=" * 50)
    
    # Step 1: Create a proper .env file (not just .env.production)
    print("📁 Creating .env file...")
    
    env_content = """# InviteMe Environment Configuration
SECRET_KEY=your-super-secure-secret-key-here-change-this-to-something-random
FLASK_ENV=production
FLASK_DEBUG=False

# MySQL Database Configuration for InviteMe
DATABASE_URL=mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4

# Application Settings
APP_NAME=InviteMe
APP_URL=https://parth967.pythonanywhere.com
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    # Step 2: Update .env.production to match
    try:
        with open('.env.production', 'w') as f:
            f.write(env_content)
        print("✅ Updated .env.production file")
    except Exception as e:
        print(f"❌ Error updating .env.production file: {e}")
    
    # Step 3: Create a backup of current app.py
    print("\n💾 Creating backup of app.py...")
    try:
        shutil.copy2('app.py', 'app.py.backup')
        print("✅ Backup created: app.py.backup")
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
    
    # Step 4: Read current app.py
    print("\n📖 Reading current app.py...")
    try:
        with open('app.py', 'r') as f:
            app_content = f.read()
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False
    
    # Step 5: Fix the database configuration in app.py
    print("🔧 Fixing database configuration in app.py...")
    
    # Replace the problematic line
    old_line = "app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inviteme.db')"
    new_line = """# Force MySQL database - no SQLite fallback
mysql_url = 'mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', mysql_url)"""
    
    if old_line in app_content:
        app_content = app_content.replace(old_line, new_line)
        print("✅ Fixed database configuration")
    else:
        print("⚠️  Could not find exact line to replace, adding configuration...")
        # Add the configuration after the SECRET_KEY line
        secret_line = "app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')"
        if secret_line in app_content:
            app_content = app_content.replace(
                secret_line,
                secret_line + "\n\n" + new_line
            )
    
    # Step 6: Write the updated app.py
    try:
        with open('app.py', 'w') as f:
            f.write(app_content)
        print("✅ Updated app.py with fixed database configuration")
    except Exception as e:
        print(f"❌ Error writing app.py: {e}")
        return False
    
    # Step 7: Test the configuration
    print("\n🧪 Testing the fixed configuration...")
    try:
        # Import the updated app
        import importlib
        import sys
        
        # Remove old module from cache
        if 'app' in sys.modules:
            del sys.modules['app']
        
        # Import fresh app
        from app import app, db
        
        with app.app_context():
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            print(f"✅ Database URI: {db_uri}")
            
            if 'mysql' in db_uri and 'Parth967$inviteme' in db_uri:
                print("✅ Configuration points to correct MySQL database")
            else:
                print(f"❌ Configuration still wrong: {db_uri}")
                return False
        
        print("✅ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 InviteMe Web App Database Fix")
    print("=" * 50)
    
    success = fix_web_app_database()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ WEB APP DATABASE FIXED!")
        print("=" * 50)
        
        print("\n🎯 What was fixed:")
        print("✅ Created proper .env file")
        print("✅ Updated .env.production file")
        print("✅ Fixed app.py database configuration")
        print("✅ Removed SQLite fallback")
        print("✅ Forced MySQL database usage")
        
        print("\n🚀 Final steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit: https://parth967.pythonanywhere.com")
        print("4. The app should now use the correct MySQL database")
        
        print("\n🎊 Your InviteMe platform should now work!")
        
    else:
        print("\n❌ Fix failed!")
        print("Check the error messages above.")
        print("You can restore the backup with: cp app.py.backup app.py")
    
    return success

if __name__ == "__main__":
    main()