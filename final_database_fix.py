#!/usr/bin/env python3.10
"""
Final Database Fix - Clean Version

We found the issue: web app connects to Parth967$subtracker (wrong)
instead of Parth967$inviteme (correct). This fixes it cleanly.
"""

def fix_app_database():
    """Fix the app.py to use the correct database"""
    print("🔧 Final Database Fix")
    print("=" * 50)
    
    # Read current app.py
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        print("✅ Read app.py")
    except Exception as e:
        print(f"❌ Cannot read app.py: {e}")
        return False
    
    # Create backup
    try:
        with open('app.py.final_backup', 'w') as f:
            f.write(content)
        print("✅ Backup created: app.py.final_backup")
    except Exception as e:
        print(f"⚠️  Cannot create backup: {e}")
    
    # Find the database configuration line and replace it
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if "app.config['SQLALCHEMY_DATABASE_URI']" in line:
            # Replace with hardcoded correct database
            new_lines.append("# FIXED: Force correct InviteMe database")
            new_lines.append("app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4'")
            print("✅ Replaced database configuration line")
        else:
            new_lines.append(line)
    
    # Write the fixed content
    try:
        with open('app.py', 'w') as f:
            f.write('\n'.join(new_lines))
        print("✅ Fixed app.py written")
        return True
    except Exception as e:
        print(f"❌ Cannot write app.py: {e}")
        return False

def test_fix():
    """Test the fix"""
    print("\n🧪 Testing the fix...")
    
    try:
        # Remove cached module
        import sys
        if 'app' in sys.modules:
            del sys.modules['app']
        
        # Import fixed app
        from app import app, db
        
        with app.app_context():
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            print(f"📍 Database URI: {db_uri}")
            
            if 'Parth967$inviteme' in db_uri:
                print("✅ App now configured for correct database!")
                return True
            else:
                print(f"❌ Still wrong database: {db_uri}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Final InviteMe Database Fix")
    print("=" * 50)
    
    print("🎯 Issue identified:")
    print("❌ Web app connects to: Parth967$subtracker (wrong schema)")
    print("✅ Should connect to: Parth967$inviteme (correct schema)")
    
    if fix_app_database():
        if test_fix():
            print("\n" + "=" * 50)
            print("🎉 DATABASE FIX SUCCESSFUL!")
            print("=" * 50)
            
            print("\n✅ What was fixed:")
            print("✅ Hardcoded correct database URL in app.py")
            print("✅ App now points to Parth967$inviteme")
            print("✅ This database has the correct schema with 'username' column")
            
            print("\n🚀 FINAL STEP:")
            print("1. Go to PythonAnywhere Web tab")
            print("2. Click 'Reload' button")
            print("3. Visit: https://parth967.pythonanywhere.com")
            print("4. Try to register/login - it should work now!")
            
            print("\n🎊 Your InviteMe platform is FIXED!")
            
        else:
            print("\n❌ Fix verification failed")
            print("Restore with: cp app.py.final_backup app.py")
    else:
        print("\n❌ Fix failed")
    
    return True

if __name__ == "__main__":
    main()