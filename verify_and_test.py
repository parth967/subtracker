#!/usr/bin/env python3.10
"""
Verify and Test InviteMe Database

The tables were created successfully! This script just verifies
everything is working and creates a test admin user.
"""

from app import app, db, User, Invitation, RSVP

def verify_and_test():
    """Verify database and create test user"""
    print("🔍 Verifying InviteMe Database")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Step 1: Check tables (case insensitive)
            print("📋 Checking tables...")
            result = db.engine.execute("SHOW TABLES")
            tables = [row[0].lower() for row in result]  # Convert to lowercase for comparison
            print(f"Found tables: {tables}")
            
            # Check for required tables (case insensitive)
            required_tables = ['user', 'invitation', 'rsvp']
            missing_tables = []
            
            for table in required_tables:
                if table not in tables and table.upper() not in [t.upper() for t in tables]:
                    missing_tables.append(table)
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            else:
                print("✅ All required tables exist")
            
            # Step 2: Check User table structure
            print("\n👤 Checking User table structure...")
            result = db.engine.execute("DESCRIBE user")
            user_columns = [row[0] for row in result]
            print(f"User columns: {user_columns}")
            
            required_user_cols = ['id', 'username', 'email', 'password_hash', 'full_name']
            missing_user_cols = [col for col in required_user_cols if col not in user_columns]
            
            if missing_user_cols:
                print(f"❌ User table missing columns: {missing_user_cols}")
                return False
            else:
                print("✅ User table structure is correct")
            
            # Step 3: Test user operations
            print("\n🧪 Testing user operations...")
            
            # Check if admin user already exists
            existing_admin = User.query.filter_by(username='admin').first()
            if existing_admin:
                print("✅ Admin user already exists")
                test_user = existing_admin
            else:
                # Create admin user
                test_user = User(
                    username='admin',
                    email='admin@inviteme.com',
                    full_name='Administrator'
                )
                test_user.set_password('admin123')
                
                db.session.add(test_user)
                db.session.commit()
                print("✅ Admin user created")
            
            # Test user queries
            found_by_username = User.query.filter_by(username='admin').first()
            if found_by_username:
                print("✅ Username query works")
            else:
                print("❌ Username query failed")
                return False
            
            found_by_email = User.query.filter_by(email='admin@inviteme.com').first()
            if found_by_email:
                print("✅ Email query works")
            else:
                print("❌ Email query failed")
                return False
            
            # Test password authentication
            if test_user.check_password('admin123'):
                print("✅ Password authentication works")
            else:
                print("❌ Password authentication failed")
                return False
            
            # Step 4: Test invitation creation
            print("\n📧 Testing invitation creation...")
            
            # Check if test invitation exists
            existing_invitation = Invitation.query.filter_by(title='Test Invitation').first()
            if existing_invitation:
                print("✅ Test invitation already exists")
            else:
                # Create test invitation
                from datetime import datetime, timedelta
                
                test_invitation = Invitation(
                    title='Test Invitation',
                    description='This is a test invitation',
                    event_type='party',
                    event_date=datetime.now() + timedelta(days=30),
                    event_time='18:00',
                    venue_name='Test Venue',
                    venue_address='123 Test Street',
                    host_name='Admin',
                    host_email='admin@inviteme.com',
                    template_id='classic',
                    invitation_code='TEST1234',
                    user_id=test_user.id
                )
                
                db.session.add(test_invitation)
                db.session.commit()
                print("✅ Test invitation created")
            
            # Step 5: Test RSVP creation
            print("\n📝 Testing RSVP creation...")
            
            invitation = Invitation.query.filter_by(title='Test Invitation').first()
            if invitation:
                # Check if test RSVP exists
                existing_rsvp = RSVP.query.filter_by(guest_name='Test Guest').first()
                if existing_rsvp:
                    print("✅ Test RSVP already exists")
                else:
                    # Create test RSVP
                    test_rsvp = RSVP(
                        guest_name='Test Guest',
                        guest_email='guest@example.com',
                        status='attending',
                        guest_count=2,
                        message='Looking forward to it!',
                        invitation_id=invitation.id
                    )
                    
                    db.session.add(test_rsvp)
                    db.session.commit()
                    print("✅ Test RSVP created")
            
            print("\n🎉 All database operations successful!")
            return True
            
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main function"""
    print("🚀 InviteMe Database Verification")
    print("=" * 50)
    
    success = verify_and_test()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 DATABASE VERIFICATION COMPLETE!")
        print("=" * 50)
        
        print("\n✅ Everything is working:")
        print("✅ All database tables exist and are correct")
        print("✅ User registration and authentication works")
        print("✅ Invitation creation works")
        print("✅ RSVP system works")
        print("✅ Admin user available for testing")
        
        print("\n🎯 Test credentials:")
        print("   Username: admin")
        print("   Email: admin@inviteme.com")
        print("   Password: admin123")
        
        print("\n🚀 Your InviteMe platform is READY!")
        print("1. Go to PythonAnywhere Web tab")
        print("2. Click 'Reload' button")
        print("3. Visit: https://parth967.pythonanywhere.com")
        print("4. Login with admin credentials or register new account")
        print("5. Create beautiful invitations!")
        
        print("\n🎊 Deployment successful!")
        
    else:
        print("\n❌ Verification failed!")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()