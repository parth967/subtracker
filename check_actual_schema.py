#!/usr/bin/env python3.10
"""
Check Actual Database Schema

This script checks what columns actually exist in the database
and shows the mismatch with what the code expects.
"""

import pymysql

def check_actual_schema():
    """Check what's actually in the database"""
    print("🔍 Checking Actual Database Schema")
    print("=" * 50)
    
    # Database connection
    try:
        conn = pymysql.connect(
            host='Parth967.mysql.pythonanywhere-services.com',
            user='Parth967',
            password='khushali979797',
            database='Parth967$inviteme',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        print("✅ Connected to database")
        
        # Check all tables
        print("\n📋 All tables in database:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check user table structure
        print("\n👤 User table structure:")
        try:
            cursor.execute("DESCRIBE user")
            columns = cursor.fetchall()
            print("   Columns in 'user' table:")
            for col in columns:
                print(f"   - {col[0]} ({col[1]})")
        except Exception as e:
            print(f"   ❌ Error checking user table: {e}")
        
        # Check invitation table structure
        print("\n📧 Invitation table structure:")
        try:
            cursor.execute("DESCRIBE invitation")
            columns = cursor.fetchall()
            print("   Columns in 'invitation' table:")
            for col in columns:
                print(f"   - {col[0]} ({col[1]})")
        except Exception as e:
            print(f"   ❌ Error checking invitation table: {e}")
        
        # Check RSVP table structure
        print("\n📝 RSVP table structure:")
        try:
            cursor.execute("DESCRIBE RSVP")  # Try uppercase first
            columns = cursor.fetchall()
            print("   Columns in 'RSVP' table:")
            for col in columns:
                print(f"   - {col[0]} ({col[1]})")
        except Exception as e:
            try:
                cursor.execute("DESCRIBE rsvp")  # Try lowercase
                columns = cursor.fetchall()
                print("   Columns in 'rsvp' table:")
                for col in columns:
                    print(f"   - {col[0]} ({col[1]})")
            except Exception as e2:
                print(f"   ❌ Error checking RSVP table: {e2}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎯 What the code expects:")
        print("=" * 50)
        
        print("\n👤 User table should have:")
        expected_user_cols = ['id', 'username', 'email', 'password_hash', 'full_name', 'created_at', 'is_active']
        for col in expected_user_cols:
            print(f"   - {col}")
        
        print("\n📧 Invitation table should have:")
        expected_inv_cols = ['id', 'title', 'description', 'event_type', 'event_date', 'host_name', 'invitation_code', 'user_id']
        for col in expected_inv_cols:
            print(f"   - {col}")
        
        print("\n📝 RSVP table should have:")
        expected_rsvp_cols = ['id', 'guest_name', 'guest_email', 'status', 'invitation_id', 'responded_at']
        for col in expected_rsvp_cols:
            print(f"   - {col}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False

def main():
    check_actual_schema()

if __name__ == "__main__":
    main()