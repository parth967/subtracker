#!/usr/bin/env python3.10
"""
Manual Database Reset for InviteMe

This script provides the exact MySQL commands to run manually
to completely reset the database.

Run this to get the commands, then execute them manually.
"""

def print_manual_commands():
    """Print the manual MySQL commands to run"""
    print("🔧 Manual Database Reset Commands")
    print("=" * 50)
    
    print("\n📋 Run these commands in PythonAnywhere MySQL console:")
    print("   (Go to Databases tab > Open MySQL console)")
    
    print("\n-- Step 1: Use the correct database")
    print("USE `Parth967$inviteme`;")
    
    print("\n-- Step 2: Disable foreign key checks")
    print("SET FOREIGN_KEY_CHECKS = 0;")
    
    print("\n-- Step 3: Drop all tables (run each line separately)")
    print("DROP TABLE IF EXISTS `rsvp`;")
    print("DROP TABLE IF EXISTS `invitation`;") 
    print("DROP TABLE IF EXISTS `user`;")
    print("DROP TABLE IF EXISTS `auth_users`;")  # In case old table exists
    print("DROP TABLE IF EXISTS `RSVP`;")        # In case uppercase exists
    print("DROP TABLE IF EXISTS `Invitation`;")  # In case mixed case exists
    print("DROP TABLE IF EXISTS `User`;")        # In case mixed case exists
    
    print("\n-- Step 4: Re-enable foreign key checks")
    print("SET FOREIGN_KEY_CHECKS = 1;")
    
    print("\n-- Step 5: Verify all tables are gone")
    print("SHOW TABLES;")
    
    print("\n" + "=" * 50)
    print("After running the above commands:")
    print("1. Come back to Bash console")
    print("2. Run: python3.10 create_fresh_tables.py")
    print("=" * 50)

def main():
    print_manual_commands()

if __name__ == "__main__":
    main()