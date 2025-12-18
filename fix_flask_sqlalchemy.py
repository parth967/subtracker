#!/usr/bin/env python3.10
"""
Quick Fix for Flask-SQLAlchemy Compatibility Issue

This script fixes the Flask-SQLAlchemy version compatibility issue
that causes the '_QueryProperty' import error on PythonAnywhere.

Run this in your PythonAnywhere Bash console:
cd /home/Parth967/inviteme
python3.10 fix_flask_sqlalchemy.py
"""

import subprocess
import sys

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Fix Flask-SQLAlchemy compatibility"""
    print("🔧 Fixing Flask-SQLAlchemy Compatibility Issue")
    print("=" * 50)
    
    # Uninstall incompatible versions
    print("\n🗑️  Removing incompatible packages...")
    uninstall_commands = [
        "pip3.10 uninstall -y Flask-SQLAlchemy",
        "pip3.10 uninstall -y Flask", 
        "pip3.10 uninstall -y Werkzeug"
    ]
    
    for cmd in uninstall_commands:
        run_command(cmd, f"Uninstalling {cmd.split()[-1]}")
    
    # Install compatible versions
    print("\n📦 Installing compatible versions...")
    install_commands = [
        "pip3.10 install --user Flask==2.2.5",
        "pip3.10 install --user Flask-SQLAlchemy==2.5.1",
        "pip3.10 install --user Werkzeug==2.2.3",
        "pip3.10 install --user Flask-Login==0.6.3",
        "pip3.10 install --user qrcode[pil]==7.4.2",
        "pip3.10 install --user Pillow==10.0.1",
        "pip3.10 install --user python-dotenv==1.0.0",
        "pip3.10 install --user PyMySQL==1.1.0"
    ]
    
    success_count = 0
    for cmd in install_commands:
        if run_command(cmd, f"Installing {cmd.split('==')[0].split()[-1]}"):
            success_count += 1
    
    # Test imports
    print("\n🧪 Testing imports...")
    try:
        import flask
        print("✅ Flask import - OK")
        
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy import - OK")
        
        import flask_login
        print("✅ Flask-Login import - OK")
        
        import qrcode
        print("✅ QRCode import - OK")
        
        # Test app import
        sys.path.insert(0, '.')
        from app import app
        print("✅ App import - OK")
        
        print("\n🎉 All imports successful!")
        print("\n🚀 Next steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit https://parth967.pythonanywhere.com")
        print("4. Your InviteMe app should now work!")
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("- Check if all packages installed correctly")
        print("- Verify you're in the correct directory")
        print("- Try running: pip3.10 list --user | grep Flask")
    
    except Exception as e:
        print(f"❌ App import failed: {e}")
        print("- This might be normal if database isn't initialized yet")
        print("- Run: python3.10 migrate_db.py init")

if __name__ == "__main__":
    main()