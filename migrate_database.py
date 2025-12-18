#!/usr/bin/env python3
"""
Database migration script for SubTracker Pro
Adds authentication support to existing database
"""

import os
import sys
from dotenv import load_dotenv

# Load production environment
load_dotenv('.env.production')

from app import app, db, AuthUser, User, Category, Subscription
from sqlalchemy import text

def migrate_database():
    """Migrate existing database to support authentication"""
    with app.app_context():
        try:
            print("🔄 Starting database migration...")
            
            # Drop and recreate all tables with new schema
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            print("📋 Creating new tables with authentication...")
            db.create_all()
            
            # Initialize default categories
            print("🏷️  Adding default categories...")
            from app import init_default_data
            init_default_data()
            
            # Create a default auth user
            print("👤 Creating default admin user...")
            default_auth_user = AuthUser(
                name="Admin User",
                email="admin@subtracker.local"
            )
            default_auth_user.set_password("admin123")
            
            db.session.add(default_auth_user)
            db.session.commit()
            
            # Create a default personal user for the admin
            print("👥 Creating default personal user...")
            personal_user = User(
                name="Admin User",
                email="admin@subtracker.local",
                user_type="personal",
                auth_user_id=default_auth_user.id
            )
            db.session.add(personal_user)
            db.session.commit()
            
            print("🎉 Database migration completed successfully!")
            print("\n🔑 Default login credentials:")
            print("Email: admin@subtracker.local")
            print("Password: admin123")
            print("\n⚠️  IMPORTANT: Change these credentials after first login!")
            
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def check_database_status():
    """Check current database status"""
    with app.app_context():
        try:
            # Check if we can connect and query
            result = db.session.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("✅ Database connection successful")
            
            # Check tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("📊 Current Database Status:")
            print(f"Tables: {tables}")
            
            if 'auth_users' in tables:
                auth_user_count = db.session.execute(text('SELECT COUNT(*) FROM auth_users')).scalar()
                print(f"Auth Users: {auth_user_count}")
            
            if 'user' in tables:
                user_count = db.session.execute(text('SELECT COUNT(*) FROM user')).scalar()
                print(f"Users: {user_count}")
            
            if 'category' in tables:
                cat_count = db.session.execute(text('SELECT COUNT(*) FROM category')).scalar()
                print(f"Categories: {cat_count}")
            
            if 'subscription' in tables:
                sub_count = db.session.execute(text('SELECT COUNT(*) FROM subscription')).scalar()
                print(f"Subscriptions: {sub_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking database: {e}")
            return False

if __name__ == "__main__":
    print("🚀 SubTracker Pro Database Migration")
    print("=" * 50)
    
    # Check current status
    print("\n1️⃣ Checking current database status...")
    if not check_database_status():
        sys.exit(1)
    
    # Run migration
    print("\n2️⃣ Running migration...")
    if migrate_database():
        print("\n3️⃣ Verifying migration...")
        check_database_status()
        
        print("\n✅ Migration completed successfully!")
        print("\n🎯 Next steps:")
        print("1. Reload your web app in PythonAnywhere")
        print("2. Visit your site and login with: admin@subtracker.local / password123")
        print("3. IMPORTANT: Change the default password immediately!")
        print("4. Create your own account through the signup page")
    else:
        print("\n❌ Migration failed!")
        print("Check the error messages above and try again.")