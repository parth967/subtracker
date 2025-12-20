"""
Quick script to add email notification columns to User table
Run this once to add the columns safely
"""

from app import app, db, User
from sqlalchemy import text

def add_email_columns():
    """Add email notification columns to user table"""
    with app.app_context():
        try:
            # Check if columns exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            print("📧 Adding email notification columns...")
            
            # Add columns one by one if they don't exist
            if 'email_notifications_enabled' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN email_notifications_enabled BOOLEAN DEFAULT TRUE"))
                print("✅ Added email_notifications_enabled")
            
            if 'email_new_rsvp' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN email_new_rsvp BOOLEAN DEFAULT TRUE"))
                print("✅ Added email_new_rsvp")
            
            if 'email_reminders' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN email_reminders BOOLEAN DEFAULT TRUE"))
                print("✅ Added email_reminders")
            
            if 'email_weekly_summary' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN email_weekly_summary BOOLEAN DEFAULT FALSE"))
                print("✅ Added email_weekly_summary")
            
            if 'email_milestones' not in columns:
                db.session.execute(text("ALTER TABLE user ADD COLUMN email_milestones BOOLEAN DEFAULT TRUE"))
                print("✅ Added email_milestones")
            
            db.session.commit()
            print("🎉 Email columns added successfully!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            print("💡 If columns already exist, that's okay - the app will work fine!")
            return False

if __name__ == '__main__':
    add_email_columns()

