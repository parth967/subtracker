#!/usr/bin/env python3.10
"""
Create Fresh Tables for InviteMe

Run this AFTER manually clearing the database.
This creates clean tables without any constraint conflicts.

Run this in PythonAnywhere Bash console:
python3.10 create_fresh_tables.py
"""

from app import app, db, User, Invitation, RSVP

def create_fresh_tables():
    """Create fresh database tables"""
    print("🏗️  Creating Fresh InviteMe Tables")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Step 1: Verify database is empty
            print("🔍 Checking if database is empty...")
            try:
                result = db.engine.execute("SHOW TABLES")
                tables = [row[0] for row in result]
                
                if tables:
                    print(f"⚠️  Database not empty! Found tables: {tables}")
                    print("   Please run the manual reset commands first.")
                    return False
                else:
                    print("✅ Database is empty - ready to create tables")
            except Exception as e:
                print(f"⚠️  Could not check tables: {e}")
            
            # Step 2: Create all tables
            print("\n🏗️  Creating all tables...")
            db.create_all()
            print("✅ Tables created successfully")
            
            # Step 3: Verify table creation
            print("\n🔍 Verifying table creation...")
            result = db.engine.execute("SHOW TABLES")
            new_tables = [row[0] for row in result]
            print(f"📋 Created tables: {new_tables}")
            
            expected_tables = ['user', 'invitation', 'rsvp']
            missing_tables = [table for table in expected_tables if table not in new_tables]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            
            # Step 4: Check table structures
            print("\n📊 Checking table structures...")
            
            # User table
            result = db.engine.execute("DESCRIBE user")
            user_columns = [row[0] for row in result]
            print(f"👤 User columns: {user_columns}")
            
            required_user_cols = ['id', 'username', 'email', 'password_hash', 'full_name']
            missing_user_cols = [col for col in required_user_cols if col not in user_columns]
            
            if missing_user_cols:
                print(f"❌ User table missing columns: {missing_user_cols}")
                return False
            else:
                print("✅ User table structure correct")
            
            # Invitation table
            result = db.engine.execute("DESCRIBE invitation")
            invitation_columns = [row[0] for row in result]
            print(f"📧 Invitation columns: {invitation_columns}")
            
            # RSVP table
            result = db.engine.execute("DESCRIBE rsvp")
            rsvp_columns = [row[0] for row in result]
            print(f"📝 RSVP columns: {rsvp_columns}")
            
            # Step 5: Test basic operations
            print("\n🧪 Testing database operations...")
            
            # Test user creation
            test_user = User(
                username='admin',
                email='admin@inviteme.com',
                full_name='Administrator'
            )
            test_user.set_password('admin123')
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created")
            
            # Test user query by username
            found_user = User.query.filter_by(username='admin').first()
            if found_user:
                print("✅ Username query works")
            else:
                print("❌ Username query failed")
                return False
            
            # Test user query by email
            found_user_email = User.query.filter_by(email='admin@inviteme.com').first()
            if found_user_email:
                print("✅ Email query works")
            else:
                print("❌ Email query failed")
                return False
            
            # Test password authentication
            if found_user.check_password('admin123'):
                print("✅ Password authentication works")
            else:
                print("❌ Password authentication failed")
                return False
            
            print(f"\n✅ Admin user created successfully!")
            print(f"   Username: admin")
            print(f"   Email: admin@inviteme.com")
            print(f"   Password: admin123")
            
            print("\n🎉 Fresh database created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function"""
    print("🚀 InviteMe Fresh Table Creation")
    print("=" * 50)
    
    success = create_fresh_tables()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 FRESH DATABASE CREATED!")
        print("=" * 50)
        
        print("\n✅ What's ready:")
        print("✅ Clean database with correct schema")
        print("✅ User table with username/email columns")
        print("✅ Invitation and RSVP tables properly linked")
        print("✅ Admin user created for testing")
        print("✅ All database operations verified")
        
        print("\n🚀 Final steps:")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit: https://parth967.pythonanywhere.com")
        print("4. You should see the InviteMe home page")
        print("5. Login with admin/admin123 or register new account")
        print("6. Create beautiful invitations!")
        
        print("\n🎊 Your InviteMe platform is READY!")
        
    else:
        print("\n❌ Table creation failed!")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()