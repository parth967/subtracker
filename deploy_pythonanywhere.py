#!/usr/bin/env python3.10
"""
PythonAnywhere Deployment Script for InviteMe

This script handles the complete deployment process for InviteMe on PythonAnywhere.
Run this in a PythonAnywhere Bash console after uploading your files.

Usage:
python3.10 deploy_pythonanywhere.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if Path(filepath).exists():
        print(f"✅ {description} found: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def main():
    """Main deployment function"""
    print("🚀 InviteMe PythonAnywhere Deployment")
    print("=" * 50)
    
    # Check current directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check required files
    print("\n📋 Checking required files...")
    required_files = [
        ('app.py', 'Main application file'),
        ('wsgi.py', 'WSGI configuration'),
        ('requirements.txt', 'Dependencies list'),
        ('.env.production', 'Production environment'),
        ('migrate_db.py', 'Database migration script'),
        ('templates/base.html', 'Base template')
    ]
    
    all_files_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ Some required files are missing. Please upload all files first.")
        return False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    install_success = run_command(
        "python3.10 -m pip install --user -r requirements.txt",
        "Installing Python packages"
    )
    
    if not install_success:
        print("⚠️  Trying alternative installation method...")
        # Try installing packages individually
        packages = [
            "Flask==2.2.5",
            "Flask-SQLAlchemy==2.5.1", 
            "Flask-Login==0.6.3",
            "qrcode[pil]==7.4.2",
            "Pillow==10.0.1",
            "Werkzeug==2.2.3",
            "python-dotenv==1.0.0",
            "PyMySQL==1.1.0"
        ]
        
        for package in packages:
            run_command(
                f"python3.10 -m pip install --user {package}",
                f"Installing {package}"
            )
    
    # Test imports
    print("\n🧪 Testing imports...")
    test_imports = [
        "import flask",
        "import flask_sqlalchemy", 
        "import flask_login",
        "import qrcode",
        "import PIL",
        "import werkzeug",
        "import dotenv",
        "import pymysql"
    ]
    
    for import_test in test_imports:
        try:
            exec(import_test)
            print(f"✅ {import_test} - OK")
        except ImportError as e:
            print(f"❌ {import_test} - Failed: {e}")
    
    # Initialize database
    print("\n🗄️ Initializing database...")
    db_success = run_command(
        "python3.10 migrate_db.py init",
        "Database initialization"
    )
    
    # Test application import
    print("\n🔍 Testing application import...")
    try:
        sys.path.insert(0, current_dir)
        from app import app, db, User, Invitation, RSVP
        print("✅ Application imports successfully")
        
        # Test database connection
        with app.app_context():
            try:
                db.engine.execute("SELECT 1")
                print("✅ Database connection successful")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                
    except Exception as e:
        print(f"❌ Application import failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Deployment Summary")
    print("=" * 50)
    
    if all_files_exist and install_success and db_success:
        print("🎉 Deployment completed successfully!")
        print("\n🎯 Next steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Set source code: /home/Parth967/inviteme")
        print("3. Set working directory: /home/Parth967/inviteme") 
        print("4. Update WSGI file with the provided wsgi.py content")
        print("5. Reload your web app")
        print("6. Visit https://parth967.pythonanywhere.com")
        print("\n🔐 Create your first user account and start creating invitations!")
    else:
        print("⚠️  Deployment completed with some issues.")
        print("Please check the error messages above and resolve them.")
        print("\n🆘 Common fixes:")
        print("- Ensure all files are uploaded to /home/Parth967/inviteme")
        print("- Check MySQL database credentials in .env.production")
        print("- Verify Python 3.10 is being used")
    
    return True

if __name__ == "__main__":
    main()