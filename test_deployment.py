#!/usr/bin/env python3.10
"""
Test InviteMe Deployment

This script tests if all components of InviteMe are working correctly
on PythonAnywhere.
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    tests = [
        ("Flask", "import flask"),
        ("Flask-SQLAlchemy", "import flask_sqlalchemy"),
        ("Flask-Login", "import flask_login"),
        ("QRCode", "import qrcode"),
        ("Pillow", "import PIL"),
        ("Werkzeug", "import werkzeug"),
        ("Python-dotenv", "import dotenv"),
        ("PyMySQL", "import pymysql"),
        ("Cryptography", "import cryptography")
    ]
    
    passed = 0
    failed = 0
    
    for name, import_cmd in tests:
        try:
            exec(import_cmd)
            print(f"  ✅ {name}")
            passed += 1
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    print(f"\n📊 Import Results: {passed} passed, {failed} failed")
    return failed == 0

def test_app_import():
    """Test application import"""
    print("\n🔍 Testing application import...")
    
    try:
        from app import app, db, User, Invitation, RSVP
        print("  ✅ Application imports successfully")
        
        # Test app configuration
        with app.app_context():
            print(f"  ✅ App name: {app.name}")
            print(f"  ✅ Database URI configured: {bool(app.config.get('SQLALCHEMY_DATABASE_URI'))}")
            
        return True
    except Exception as e:
        print(f"  ❌ Application import failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from app import app, db
        with app.app_context():
            # Test connection
            result = db.engine.execute("SELECT 1 as test").fetchone()
            if result and result[0] == 1:
                print("  ✅ Database connection successful")
                
                # Test tables
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"  ✅ Tables found: {', '.join(tables)}")
                
                return True
            else:
                print("  ❌ Database query failed")
                return False
                
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False

def test_qr_generation():
    """Test QR code generation"""
    print("\n📱 Testing QR code generation...")
    
    try:
        import qrcode
        import io
        import base64
        
        # Create a test QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data("https://test.com")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qr_code = base64.b64encode(buffer.getvalue()).decode()
        
        if qr_code and len(qr_code) > 100:
            print("  ✅ QR code generation successful")
            return True
        else:
            print("  ❌ QR code generation failed")
            return False
            
    except Exception as e:
        print(f"  ❌ QR code generation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 InviteMe Deployment Test")
    print("=" * 40)
    
    # Run tests
    import_ok = test_imports()
    app_ok = test_app_import()
    db_ok = test_database_connection()
    qr_ok = test_qr_generation()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary")
    print("=" * 40)
    
    tests_passed = sum([import_ok, app_ok, db_ok, qr_ok])
    total_tests = 4
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your deployment is ready.")
        print("\n🎯 Next steps:")
        print("1. Reload your web app in PythonAnywhere")
        print("2. Visit https://parth967.pythonanywhere.com")
        print("3. Create your first user account")
        print("4. Start creating beautiful invitations!")
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed.")
        print("\n🔧 Recommended fixes:")
        
        if not import_ok:
            print("- Install missing packages: pip3.10 install --user -r requirements.txt")
        if not app_ok:
            print("- Check app.py file and fix any syntax errors")
        if not db_ok:
            print("- Verify database credentials in .env.production")
            print("- Run: python3.10 migrate_db.py init")
        if not qr_ok:
            print("- Install QR code package: pip3.10 install --user qrcode[pil]")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)