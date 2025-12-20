"""
Quick script to add custom image and design data columns to Invitation table
Run this once to add the columns safely
"""

from app import app, db, Invitation
from sqlalchemy import text

def add_custom_image_columns():
    """Add custom image and design data columns to invitation table"""
    with app.app_context():
        try:
            # Check if columns exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('invitation')]
            
            print("🖼️ Adding custom image columns...")
            
            # Add columns one by one if they don't exist
            if 'custom_image' not in columns:
                db.session.execute(text("ALTER TABLE invitation ADD COLUMN custom_image VARCHAR(255) NULL"))
                print("✅ Added custom_image")
            
            if 'design_data' not in columns:
                db.session.execute(text("ALTER TABLE invitation ADD COLUMN design_data TEXT NULL"))
                print("✅ Added design_data")
            
            db.session.commit()
            print("🎉 Custom image columns added successfully!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            print("💡 If columns already exist, that's okay - the app will work fine!")
            return False

if __name__ == '__main__':
    add_custom_image_columns()

