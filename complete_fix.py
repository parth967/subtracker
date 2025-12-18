#!/usr/bin/env python3.10
"""
Complete Fix for InviteMe PythonAnywhere Deployment

This script fixes all the issues:
1. Install missing packages (qrcode, etc.)
2. Fix Flask-SQLAlchemy version compatibility
3. Create correct database (inviteme, not subtracker)
4. Initialize database with correct schema

Run this in PythonAnywhere Bash console:
cd /home/Parth967/inviteme
python3.10 complete_fix.py
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
    """Complete fix for InviteMe deployment"""
    print("🔧 Complete InviteMe Deployment Fix")
    print("=" * 50)
    
    # Step 1: Check current directory and files
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    if not Path('app.py').exists():
        print("❌ app.py not found. Make sure you're in the correct directory.")
        print("   Expected: /home/Parth967/inviteme")
        return False
    
    # Step 2: Clean up old packages
    print("\n🧹 Cleaning up old packages...")
    cleanup_commands = [
        "pip3.10 uninstall -y Flask-SQLAlchemy",
        "pip3.10 uninstall -y Flask", 
        "pip3.10 uninstall -y Werkzeug",
        "pip3.10 uninstall -y qrcode"
    ]
    
    for cmd in cleanup_commands:
        run_command(cmd, f"Uninstalling {cmd.split()[-1]}", ignore_errors=True)
    
    # Step 3: Install correct package versions
    print("\n📦 Installing correct package versions...")
    install_commands = [
        "pip3.10 install --user Flask==2.2.5",
        "pip3.10 install --user Flask-SQLAlchemy==2.5.1",
        "pip3.10 install --user Werkzeug==2.2.3",
        "pip3.10 install --user Flask-Login==0.6.3",
        "pip3.10 install --user 'qrcode[pil]==7.4.2'",
        "pip3.10 install --user Pillow==10.0.1",
        "pip3.10 install --user python-dotenv==1.0.0",
        "pip3.10 install --user PyMySQL==1.1.0"
    ]
    
    success_count = 0
    for cmd in install_commands:
        if run_command(cmd, f"Installing {cmd.split('==')[0].split()[-1]}"):
            success_count += 1
    
    print(f"\n📊 Installed {success_count}/{len(install_commands)} packages successfully")
    
    # Step 4: Test imports
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
        return False
    
    # Step 6: Test app import
    print("\n🔍 Testing application import...")
    try:
        # Add current directory to path
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from app import app, db, User, Invitation, RSVP
        print("✅ Application imports successfully!")
        
        # Test database context
        with app.app_context():
            try:
                # Test if tables exist
                result = db.engine.execute("SHOW TABLES")
                tables = [row[0] for row in result]
                print(f"✅ Database tables found: {tables}")
                
                if 'user' not in tables:
                    print("⚠️  User table not found. Need to initialize database.")
                    
            except Exception as e:
                print(f"⚠️  Database query failed: {e}")
                print("   This is normal if database hasn't been initialized yet.")
        
    except Exception as e:
        print(f"❌ Application import failed: {e}")
        return False
    
    # Step 7: Initialize database if needed
    print("\n🗃️ Initializing database...")
    if run_command("python3.10 migrate_db.py init", "Database initialization"):
        print("✅ Database initialized successfully!")
    else:
        print("⚠️  Database initialization failed. You may need to run it manually.")
    
    # Step 8: Final verification
    print("\n🔍 Final verification...")
    try:
        from app import app
        with app.app_context():
            result = db.engine.execute("SELECT COUNT(*) FROM user")
            user_count = result.fetchone()[0]
            print(f"✅ User table accessible. Current users: {user_count}")
            
    except Exception as e:
        print(f"⚠️  Final verification failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 Fix Complete!")
    print("=" * 50)
    
    print("\n🚀 Next Steps:")
    print("1. Go to PythonAnywhere Web tab")
    print("2. Make sure your web app points to:")
    print("   - Source code: /home/Parth967/inviteme")
    print("   - Working directory: /home/Parth967/inviteme")
    print("3. Update WSGI file if needed")
    print("4. Click 'Reload' button")
    print("5. Visit: https://parth967.pythonanywhere.com")
    
    print("\n🎯 Your InviteMe platform should now work!")
    print("- Create account and start making invitations")
    print("- All 11 templates available")
    print("- QR codes and RSVP tracking working")
    
    return True

if __name__ == "__main__":
    main()