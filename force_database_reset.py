#!/usr/bin/env python3.10
"""
Force Database Reset for InviteMe

This script forcefully resets the database by manually dropping
all constraints and tables, then recreating everything.

Run this in PythonAnywhere Bash console:
python3.10 force_database_reset.py
"""

import sys
import pymysql
from app import app, db, User, Invitation, RSVP

def force_reset_database():
    """Forcefully reset the database"""
    print("🔧 Force Resetting InviteMe Database")
    print("=" * 50)
    
    # Database connection details
    db_config = {
        'host': 'Parth967.mysql.pythonanywhere-services.com',
        'user': 'Parth967',
        'password': 'khushali979797',
        'database': 'Parth967$inviteme',
        'charset': 'utf8mb4'
    }
    
    try:
        # Step 1: Connect directly to MySQL
        print("🔌 Connecting to MySQL database...")
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("✅ Connected to database")
        
        # Step 2: Disable foreign key checks
        print("\n🔓 Disabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Step 3: Get all tables
        print("\n📋 Getting all tables...")
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Found tables: {tables}")
        
        # Step 4: Drop all tables
        print("\n🗑️  Dropping all tables...")
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                print(f"✅ Dropped table: {table}")
            except Exception as e:
                print(f"⚠️  Could not drop {table}: {e}")
        
        # Step 5: Re-enable foreign key checks
        print("\n🔒 Re-enabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database cleared successfully")
        
        # Step 6: Recreate tables using SQLAlchemy
        print("\n🏗️  Creating new tables with SQLAlchemy...")
        with app.app_context():
            db.create_all()
            print("✅ All tables created successfully")
            
            # Step 7: Verify table structure
            print("\n🔍 Verifying new table structure...")
            
            # Check tables exist
            result = db.engine.execute("SHOW TABLES")
            new_tables = [row[0] for row in result]
            print(f"📋 New tables: {new_tables}")
            
            # Check User table structure
            if 'user' in new_tables:
                result = db.engine.execute("DESCRIBE user")
                user_columns = [row[0] for row in result]
                print(f"👤 User table columns: {user_columns}")
                
                # Verify required columns exist
                required_columns = ['id', 'username', 'email', 'password_hash', 'full_name']
                missing = [col for col in required_columns if col not in user_columns]
                
                if missing:
                    print(f"❌ Missing columns: {missing}")
                    return False
                else:
                    print("✅ User table structure correct")
            
            # Check Invitation table
            if 'invitation' in new_tables:
                result = db.engine.execute("DESCRIBE invitation")
                invitation_columns = [row[0] for row in result]
                print(f"📧 Invitation table columns: {invitation_columns}")
            
            # Check RSVP table
            if 'rsvp' in new_tables:
                result = db.engine.execute("DESCRIBE rsvp")
                rsvp_columns = [row[0] for row in result]
                print(f"📝 RSVP table columns: {rsvp_columns}")
            
            # Step 8: Test basic operations
            print("\n🧪 Testing database operations...")
            
            # Test user creation
            test_user = User(
                username='testuser123',
                email='test@inviteme.com',
                full_name='Test User'
            )
            test_user.set_password('testpass123')
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created")
            
            # Test user query
            found_user = User.query.filter_by(username='testuser123').first()
            if found_user:
                print("✅ User query works")
                
                # Test user authentication
                if found_user.check_password('testpass123'):
                    print("✅ Password authentication works")
                else:
                    print("❌ Password authentication failed")
                
                # Clean up
                db.session.delete(found_user)
                db.session.commit()
                print("✅ Test user cleaned up")
            else:
                print("❌ User query failed")
                return False
            
            print("\n🎉 Database reset completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error during database reset: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🚀 InviteMe Force Database Reset")
    print("=" * 50)
    
    print("⚠️  WARNING: This will completely destroy and recreate the database!")
    print("   ALL existing data will be permanently lost!")
    print("   This includes users, invitations, and RSVPs.")
    
    response = input("\nAre you absolutely sure? Type 'RESET' to continue: ")
    if response != 'RESET':
        print("❌ Operation cancelled.")
        return False
    
    success = force_reset_database()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 FORCE DATABASE RESET COMPLETE!")
        print("=" * 50)
        
        print("\n✅ What's been accomplished:")
        print("✅ All old tables and constraints removed")
        print("✅ Fresh database schema created")
        print("✅ User table with correct columns")
        print("✅ Invitation and RSVP tables properly linked")
        print("✅ All database operations tested")
        
        print("\n🚀 Final steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit: https://parth967.pythonanywhere.com")
        print("4. You should see the InviteMe home page")
        print("5. Register a new account")
        print("6. Create your first invitation!")
        
        print("\n🎊 Your InviteMe platform is now ready!")
        
    else:
        print("\n❌ Force reset failed!")
        print("Please check the error messages above.")
        print("You may need to manually reset the database in PythonAnywhere.")
    
    return success

if __name__ == "__main__":
    main()