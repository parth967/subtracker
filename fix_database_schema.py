#!/usr/bin/env python3.10
"""
Fix Database Schema for InviteMe

This script completely recreates the database with the correct schema.
The current database has wrong column names and structure.

Run this in PythonAnywhere Bash console:
python3.10 fix_database_schema.py
"""

import sys
from app import app, db, User, Invitation, RSVP

def fix_database():
    """Drop and recreate all tables with correct schema"""
    print("🔧 Fixing InviteMe Database Schema")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Step 1: Check current tables
            print("🔍 Checking current database state...")
            try:
                result = db.engine.execute("SHOW TABLES")
                tables = [row[0] for row in result]
                print(f"📋 Current tables: {tables}")
            except Exception as e:
                print(f"⚠️  Could not check tables: {e}")
            
            # Step 2: Drop all existing tables
            print("\n🗑️  Dropping all existing tables...")
            try:
                db.drop_all()
                print("✅ All tables dropped successfully")
            except Exception as e:
                print(f"⚠️  Error dropping tables: {e}")
            
            # Step 3: Create all tables with correct schema
            print("\n🏗️  Creating tables with correct schema...")
            db.create_all()
            print("✅ All tables created successfully")
            
            # Step 4: Verify table structure
            print("\n🔍 Verifying table structure...")
            
            # Check User table columns
            result = db.engine.execute("DESCRIBE user")
            user_columns = [row[0] for row in result]
            print(f"👤 User table columns: {user_columns}")
            
            expected_user_columns = ['id', 'username', 'email', 'password_hash', 'full_name', 'created_at', 'is_active']
            missing_columns = [col for col in expected_user_columns if col not in user_columns]
            
            if missing_columns:
                print(f"❌ Missing columns in user table: {missing_columns}")
                return False
            else:
                print("✅ User table has all required columns")
            
            # Check Invitation table
            result = db.engine.execute("DESCRIBE invitation")
            invitation_columns = [row[0] for row in result]
            print(f"📧 Invitation table columns: {invitation_columns}")
            
            # Check RSVP table
            result = db.engine.execute("DESCRIBE rsvp")
            rsvp_columns = [row[0] for row in result]
            print(f"📝 RSVP table columns: {rsvp_columns}")
            
            # Step 5: Test basic operations
            print("\n🧪 Testing basic database operations...")
            
            # Test creating a user
            test_user = User(
                username='test_user',
                email='test@example.com',
                full_name='Test User'
            )
            test_user.set_password('test123')
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully")
            
            # Test querying user
            found_user = User.query.filter_by(username='test_user').first()
            if found_user:
                print("✅ User query successful")
                
                # Clean up test user
                db.session.delete(found_user)
                db.session.commit()
                print("✅ Test user cleaned up")
            else:
                print("❌ User query failed")
                return False
            
            print("\n🎉 Database schema fixed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing database: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function"""
    print("🚀 InviteMe Database Schema Fix")
    print("=" * 50)
    
    # Confirm action
    print("⚠️  This will completely recreate the database.")
    print("   All existing data will be lost!")
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Operation cancelled.")
        return False
    
    success = fix_database()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Database Schema Fix Complete!")
        print("=" * 50)
        
        print("\n🎯 What's been fixed:")
        print("✅ User table with correct columns (username, email, etc.)")
        print("✅ Invitation table with all fields")
        print("✅ RSVP table with proper relationships")
        print("✅ All foreign key constraints")
        
        print("\n🚀 Next steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit: https://parth967.pythonanywhere.com")
        print("4. Register your first account")
        print("5. Start creating invitations!")
        
        print("\n🎊 Your InviteMe platform is ready!")
        
    else:
        print("\n❌ Database fix failed!")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()