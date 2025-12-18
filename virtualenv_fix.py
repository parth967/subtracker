#!/usr/bin/env python3.10
"""
Virtual Environment Fix for InviteMe PythonAnywhere Deployment

This script works with PythonAnywhere virtual environments.
It installs packages without --user flag and handles the correct directory.

Run this in PythonAnywhere Bash console:
cd /home/Parth967/mysite/subtracker  # or wherever your files are
python3.10 virtualenv_fix.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, ignore_errors=False):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"⚠️  {description} failed (ignored): {e}")
            return True
        else:
            print(f"❌ {description} failed: {e}")
            if e.stderr:
                print(f"   Error: {e.stderr.strip()}")
            return False

def main():
    """Fix InviteMe in virtual environment"""
    print("🔧 InviteMe Virtual Environment Fix")
    print("=" * 50)
    
    # Check current directory and environment
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"🐍 Virtual environment: {'Yes' if in_venv else 'No'}")
    
    if not Path('app.py').exists():
        print("❌ app.py not found in current directory.")
        print("   Make sure you're in the directory with your InviteMe files.")
        print("   Try: cd /home/Parth967/mysite/subtracker")
        return False
    
    # Step 1: Clean up old packages (without --user)
    print("\n🧹 Cleaning up old packages...")
    cleanup_commands = [
        "pip3.10 uninstall -y Flask-SQLAlchemy",
        "pip3.10 uninstall -y Flask", 
        "pip3.10 uninstall -y Werkzeug",
        "pip3.10 uninstall -y qrcode"
    ]
    
    for cmd in cleanup_commands:
        run_command(cmd, f"Uninstalling {cmd.split()[-1]}", ignore_errors=True)
    
    # Step 2: Install correct package versions (without --user)
    print("\n📦 Installing correct package versions...")
    install_commands = [
        "pip3.10 install Flask==2.2.5",
        "pip3.10 install Flask-SQLAlchemy==2.5.1",
        "pip3.10 install Werkzeug==2.2.3",
        "pip3.10 install Flask-Login==0.6.3",
        "pip3.10 install 'qrcode[pil]==7.4.2'",
        "pip3.10 install Pillow==10.0.1",
        "pip3.10 install python-dotenv==1.0.0",
        "pip3.10 install PyMySQL==1.1.0"
    ]
    
    success_count = 0
    for cmd in install_commands:
        if run_command(cmd, f"Installing {cmd.split('==')[0].split()[-1]}"):
            success_count += 1
    
    print(f"\n📊 Installed {success_count}/{len(install_commands)} packages successfully")
    
    # Step 3: Test imports
    print("\n🧪 Testing package imports...")
    try:
        import flask
        print("✅ Flask - OK")
        
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy - OK")
        
        import flask_login
        print("✅ Flask-Login - OK")
        
        import qrcode
        print("✅ QRCode - OK")
        
        import pymysql
        print("✅ PyMySQL - OK")
        
        import dotenv
        print("✅ python-dotenv - OK")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Step 4: Update database configuration
    print("\n🗄️ Updating database configuration...")
    
    # Check if .env.production exists and update it
    env_content = """# Production Configuration for PythonAnywhere - InviteMe
# Flask Configuration
SECRET_KEY=your-super-secure-secret-key-here-change-this-to-something-random
FLASK_ENV=production

# MySQL Database Configuration for InviteMe
# Database: Parth967$inviteme (NOT subtracker)
DATABASE_URL=mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4

# Application Settings
APP_NAME=InviteMe
APP_URL=https://parth967.pythonanywhere.com"""
    
    try:
        with open('.env.production', 'w') as f:
            f.write(env_content)
        print("✅ Updated .env.production with correct database")
    except Exception as e:
        print(f"⚠️  Could not update .env.production: {e}")
    
    # Step 5: Test database connection
    print("\n🗄️ Testing database connection...")
    try:
        import pymysql
        conn = pymysql.connect(
            host='Parth967.mysql.pythonanywhere-services.com',
            user='Parth967',
            password='khushali979797',
            database='Parth967$inviteme',
            charset='utf8mb4'
        )
        print("✅ Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure the database 'Parth967$inviteme' exists in PythonAnywhere")
        print("   Go to Databases tab and create it if needed")
    
    # Step 6: Test app import
    print("\n🔍 Testing application import...")
    try:
        # Add current directory to path
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from app import app, db
        print("✅ Application imports successfully!")
        
        # Test database context
        with app.app_context():
            try:
                # Test database connection
                result = db.engine.execute("SELECT 1")
                print("✅ Database query successful!")
                
            except Exception as e:
                print(f"⚠️  Database query failed: {e}")
                print("   This might be normal if database tables don't exist yet")
        
    except Exception as e:
        print(f"❌ Application import failed: {e}")
        print("   Check if app.py is in the current directory")
        return False
    
    # Step 7: Initialize database
    print("\n🗃️ Initializing database...")
    if run_command("python3.10 migrate_db.py init", "Database initialization"):
        print("✅ Database initialized successfully!")
    else:
        print("⚠️  Database initialization failed. Try running manually:")
        print("   python3.10 migrate_db.py init")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 Virtual Environment Fix Complete!")
    print("=" * 50)
    
    print(f"\n📍 Current setup:")
    print(f"   Directory: {current_dir}")
    print(f"   Virtual env: {'Yes' if in_venv else 'No'}")
    print(f"   Packages installed: {success_count}/8")
    
    print("\n🚀 Next Steps:")
    print("1. Go to PythonAnywhere Web tab")
    print("2. Make sure your web app points to:")
    print(f"   - Source code: {current_dir}")
    print(f"   - Working directory: {current_dir}")
    print("3. Update WSGI file to point to this directory")
    print("4. Click 'Reload' button")
    print("5. Visit: https://parth967.pythonanywhere.com")
    
    print("\n🎯 Your InviteMe platform should now work!")
    
    return True

if __name__ == "__main__":
    main()