#!/usr/bin/env python3
"""
InviteMe Database Migration Script

This script handles database creation, updates, and migrations for the InviteMe platform.
Run this script whenever you need to set up or update the database schema.

Usage:
    python migrate_db.py [action]

Actions:
    init     - Initialize database (default)
    reset    - Reset database (drop all tables and recreate)
    backup   - Create a backup of current database
    restore  - Restore from backup
    status   - Show database status
"""

import os
import sys
import shutil
from datetime import datetime
from app import app, db, User, Invitation, RSVP

def init_database():
    """Initialize the database with all tables"""
    print("🔄 Initializing InviteMe database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Created tables: {', '.join(tables)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False

def reset_database():
    """Reset the database (drop all tables and recreate)"""
    print("⚠️  Resetting InviteMe database...")
    
    response = input("This will delete ALL data. Are you sure? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Database reset cancelled.")
        return False
    
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            print("🗑️  Dropped all existing tables")
            
            # Recreate all tables
            db.create_all()
            print("✅ Database reset successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            return False

def backup_database():
    """Create a backup of the current database"""
    print("💾 Creating database backup...")
    
    db_path = 'inviteme.db'
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'inviteme_backup_{timestamp}.db'
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def restore_database(backup_file=None):
    """Restore database from backup"""
    if not backup_file:
        # Find the most recent backup
        backups = [f for f in os.listdir('.') if f.startswith('inviteme_backup_') and f.endswith('.db')]
        if not backups:
            print("❌ No backup files found!")
            return False
        
        backup_file = sorted(backups)[-1]
        print(f"📁 Using most recent backup: {backup_file}")
    
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return False
    
    print(f"🔄 Restoring database from {backup_file}...")
    
    try:
        # Backup current database first
        if os.path.exists('inviteme.db'):
            current_backup = f'inviteme_pre_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            shutil.copy2('inviteme.db', current_backup)
            print(f"💾 Current database backed up to: {current_backup}")
        
        # Restore from backup
        shutil.copy2(backup_file, 'inviteme.db')
        print("✅ Database restored successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error restoring database: {e}")
        return False

def show_database_status():
    """Show current database status and statistics"""
    print("📊 InviteMe Database Status")
    print("=" * 50)
    
    db_path = 'inviteme.db'
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    # File info
    file_size = os.path.getsize(db_path)
    file_size_mb = file_size / (1024 * 1024)
    modified_time = datetime.fromtimestamp(os.path.getmtime(db_path))
    
    print(f"📁 Database file: {db_path}")
    print(f"📏 File size: {file_size_mb:.2f} MB")
    print(f"🕒 Last modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    with app.app_context():
        try:
            # Table info
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tables: {', '.join(tables)}")
            
            # Record counts
            user_count = User.query.count()
            invitation_count = Invitation.query.count()
            rsvp_count = RSVP.query.count()
            
            print(f"\n📈 Statistics:")
            print(f"   Users: {user_count}")
            print(f"   Invitations: {invitation_count}")
            print(f"   RSVPs: {rsvp_count}")
            
            if invitation_count > 0:
                # Recent activity
                recent_invitations = Invitation.query.order_by(Invitation.created_at.desc()).limit(5).all()
                print(f"\n🆕 Recent Invitations:")
                for inv in recent_invitations:
                    print(f"   • {inv.title} ({inv.created_at.strftime('%Y-%m-%d')})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading database: {e}")
            return False

def main():
    """Main function to handle command line arguments"""
    action = sys.argv[1] if len(sys.argv) > 1 else 'init'
    
    print("🚀 InviteMe Database Migration Tool")
    print("=" * 50)
    
    if action == 'init':
        success = init_database()
    elif action == 'reset':
        success = reset_database()
    elif action == 'backup':
        success = backup_database()
    elif action == 'restore':
        backup_file = sys.argv[2] if len(sys.argv) > 2 else None
        success = restore_database(backup_file)
    elif action == 'status':
        success = show_database_status()
    else:
        print(f"❌ Unknown action: {action}")
        print("\nAvailable actions:")
        print("  init     - Initialize database (default)")
        print("  reset    - Reset database (drop all tables and recreate)")
        print("  backup   - Create a backup of current database")
        print("  restore  - Restore from backup")
        print("  status   - Show database status")
        return False
    
    if success:
        print(f"\n✅ Action '{action}' completed successfully!")
        
        if action in ['init', 'reset']:
            print("\n🎯 Next steps:")
            print("1. Start the application: python app.py")
            print("2. Open your browser to: http://localhost:5000")
            print("3. Create your first invitation!")
    else:
        print(f"\n❌ Action '{action}' failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()