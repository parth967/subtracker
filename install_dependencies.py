#!/usr/bin/env python3.10
"""
Install Dependencies for InviteMe on PythonAnywhere

This script installs all required Python packages for the InviteMe platform
on PythonAnywhere hosting environment.

Run this in a PythonAnywhere Bash console:
python3.10 install_dependencies.py
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip with --user flag"""
    try:
        print(f"📦 Installing {package}...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--user', package
        ], capture_output=True, text=True, check=True)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Install all required packages"""
    print("🚀 Installing InviteMe Dependencies on PythonAnywhere")
    print("=" * 60)
    
    # List of required packages
    packages = [
        'Flask>=2.3.0',
        'Flask-SQLAlchemy>=3.0.0',
        'Flask-Login>=0.6.0',
        'qrcode[pil]>=7.4.0',  # Include PIL support
        'Pillow>=10.0.0',
        'Werkzeug>=2.3.0',
        'python-dotenv>=1.0.0',
        'PyMySQL>=1.0.0',
        'cryptography>=3.0.0'  # Required for PyMySQL
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
        print()  # Add spacing
    
    print("=" * 60)
    print(f"📊 Installation Summary:")
    print(f"   ✅ Successful: {success_count}/{total_packages}")
    print(f"   ❌ Failed: {total_packages - success_count}/{total_packages}")
    
    if success_count == total_packages:
        print("\n🎉 All dependencies installed successfully!")
        print("\n🎯 Next steps:")
        print("1. Initialize the database: python3.10 migrate_db.py init")
        print("2. Reload your web app in PythonAnywhere")
        print("3. Test your application!")
    else:
        print(f"\n⚠️  {total_packages - success_count} packages failed to install.")
        print("Please check the error messages above and try installing them manually.")
    
    return success_count == total_packages

if __name__ == "__main__":
    main()