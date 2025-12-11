#!/usr/bin/env python3
"""
Setup script for Email Analyzer
Run this script to initialize the application
"""

import os
import secrets
from app import app, db

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        secret_key = generate_secret_key()
        
        env_content = f"""# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///email_analyzer.db

# Optional: Default email configuration
# DEFAULT_EMAIL=your.email@gmail.com
# DEFAULT_APP_PASSWORD=your-app-password
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file with secure secret key")
    else:
        print("ℹ️  .env file already exists")

def initialize_database():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully")

def main():
    print("🚀 Setting up Email Analyzer...")
    print()
    
    # Create .env file
    create_env_file()
    
    # Initialize database
    initialize_database()
    
    print()
    print("✅ Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Review and update the .env file with your configuration")
    print("2. Run 'python app.py' to start the application")
    print("3. Open http://localhost:5000 in your browser")
    print("4. Add your email configuration through the web interface")
    print()
    print("For PythonAnywhere deployment:")
    print("1. Upload all files to your PythonAnywhere account")
    print("2. Update the wsgi.py file with your correct path")
    print("3. Install requirements: pip3.10 install --user -r requirements.txt")
    print("4. Configure your web app to use wsgi.py")

if __name__ == "__main__":
    main()