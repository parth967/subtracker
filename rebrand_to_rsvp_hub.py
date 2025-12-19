#!/usr/bin/env python3.10
"""
Rebrand InviteMe to RSVP Hub

This script changes all references from "InviteMe" to "RSVP Hub"
and creates a favicon for the browser tab.
"""

import os
import re

def create_favicon():
    """Create a simple favicon for RSVP Hub"""
    print("🎨 Creating RSVP Hub favicon...")
    
    # Create static/images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Create a simple SVG favicon
    favicon_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" fill="#4f46e5" rx="6"/>
  <text x="16" y="22" font-family="Arial, sans-serif" font-size="18" font-weight="bold" 
        text-anchor="middle" fill="white">R</text>
</svg>'''
    
    try:
        with open('static/images/favicon.svg', 'w') as f:
            f.write(favicon_svg)
        print("✅ Created favicon.svg")
    except Exception as e:
        print(f"⚠️  Could not create favicon.svg: {e}")
    
    # Also create a simple ICO version description
    favicon_html = '''<!-- Add this to your HTML head section -->
<link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='images/favicon.svg') }}">
<link rel="shortcut icon" href="{{ url_for('static', filename='images/favicon.svg') }}">'''
    
    try:
        with open('static/images/favicon_instructions.html', 'w') as f:
            f.write(favicon_html)
        print("✅ Created favicon instructions")
    except Exception as e:
        print(f"⚠️  Could not create favicon instructions: {e}")

def update_file_content(filepath, replacements):
    """Update content in a file with multiple replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"⚠️  Error updating {filepath}: {e}")
        return False

def rebrand_files():
    """Rebrand all files from InviteMe to RSVP Hub"""
    print("🔄 Rebranding files from InviteMe to RSVP Hub...")
    
    # Define all replacements
    replacements = {
        # Main branding
        'InviteMe': 'RSVP Hub',
        'inviteme': 'rsvphub',
        'INVITEME': 'RSVPHUB',
        
        # Descriptions and taglines
        'Beautiful Invitation & RSVP Platform': 'Beautiful RSVP & Event Management Platform',
        'Create stunning invitations': 'Create stunning event invitations',
        'invitation platform': 'RSVP platform',
        'Invitation Platform': 'RSVP Platform',
        'invitation system': 'RSVP system',
        'Invitation System': 'RSVP System',
        
        # URLs and domains (keep as examples)
        'inviteme.com': 'rsvphub.com',
        'admin@inviteme.com': 'admin@rsvphub.com',
        
        # File descriptions
        'InviteMe - Beautiful Invitation': 'RSVP Hub - Beautiful Event',
        'InviteMe Team': 'RSVP Hub Team',
        'InviteMe Headquarters': 'RSVP Hub Headquarters',
        
        # Welcome messages
        'Welcome to InviteMe!': 'Welcome to RSVP Hub!',
        'Your InviteMe platform': 'Your RSVP Hub platform',
        'InviteMe Database': 'RSVP Hub Database',
        
        # Technical references
        'InviteMe deployment': 'RSVP Hub deployment',
        'InviteMe application': 'RSVP Hub application',
        'InviteMe web application': 'RSVP Hub web application'
    }
    
    # Files to update
    files_to_update = [
        'app.py',
        'templates/base.html',
        'templates/home.html',
        'templates/dashboard.html',
        'templates/create_invitation.html',
        'templates/view_invitation.html',
        'templates/manage_invitation.html',
        'templates/template_gallery.html',
        'templates/auth/login.html',
        'templates/auth/register.html',
        'README.md',
        'DEPLOYMENT_GUIDE.md',
        '.env.production'
    ]
    
    updated_files = []
    
    for filepath in files_to_update:
        if os.path.exists(filepath):
            if update_file_content(filepath, replacements):
                updated_files.append(filepath)
                print(f"✅ Updated {filepath}")
            else:
                print(f"📄 No changes needed in {filepath}")
        else:
            print(f"⚠️  File not found: {filepath}")
    
    return updated_files

def update_base_template_with_favicon():
    """Add favicon to base template"""
    print("🔗 Adding favicon to base template...")
    
    try:
        with open('templates/base.html', 'r') as f:
            content = f.read()
        
        # Add favicon links in the head section
        favicon_links = '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='images/favicon.svg') }}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='images/favicon.svg') }}">
    <link rel="apple-touch-icon" href="{{ url_for('static', filename='images/favicon.svg') }}">'''
        
        # Find the head section and add favicon
        if '<head>' in content and favicon_links not in content:
            # Add after the opening head tag
            content = content.replace('<head>', '<head>\n' + favicon_links)
            
            with open('templates/base.html', 'w') as f:
                f.write(content)
            print("✅ Added favicon to base template")
            return True
        else:
            print("⚠️  Could not add favicon to base template")
            return False
            
    except Exception as e:
        print(f"❌ Error updating base template: {e}")
        return False

def update_page_titles():
    """Update page titles to use RSVP Hub"""
    print("📝 Updating page titles...")
    
    title_updates = {
        'templates/home.html': 'RSVP Hub - Beautiful Event Invitations',
        'templates/dashboard.html': 'Dashboard - RSVP Hub',
        'templates/create_invitation.html': 'Create Invitation - RSVP Hub',
        'templates/view_invitation.html': 'View Invitation - RSVP Hub',
        'templates/manage_invitation.html': 'Manage Invitation - RSVP Hub',
        'templates/template_gallery.html': 'Template Gallery - RSVP Hub',
        'templates/auth/login.html': 'Login - RSVP Hub',
        'templates/auth/register.html': 'Register - RSVP Hub'
    }
    
    for filepath, new_title in title_updates.items():
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Update title tag
                content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content)
                
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"✅ Updated title in {filepath}")
                
            except Exception as e:
                print(f"⚠️  Error updating title in {filepath}: {e}")

def main():
    """Main rebranding function"""
    print("🚀 RSVP Hub Rebranding")
    print("=" * 50)
    
    # Step 1: Create favicon
    create_favicon()
    
    # Step 2: Rebrand all files
    updated_files = rebrand_files()
    
    # Step 3: Add favicon to base template
    update_base_template_with_favicon()
    
    # Step 4: Update page titles
    update_page_titles()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 REBRANDING COMPLETE!")
    print("=" * 50)
    
    print(f"\n✅ What was changed:")
    print(f"✅ Created RSVP Hub favicon (purple 'R' logo)")
    print(f"✅ Updated {len(updated_files)} files with new branding")
    print(f"✅ Changed all 'InviteMe' references to 'RSVP Hub'")
    print(f"✅ Added favicon to browser tab")
    print(f"✅ Updated all page titles")
    
    print(f"\n📁 Files updated:")
    for filepath in updated_files:
        print(f"   • {filepath}")
    
    print(f"\n🚀 Next steps:")
    print(f"1. Go to PythonAnywhere Web tab")
    print(f"2. Click 'Reload' button")
    print(f"3. Visit: https://parth967.pythonanywhere.com")
    print(f"4. You should see 'RSVP Hub' branding and favicon!")
    
    print(f"\n🎊 Your platform is now RSVP Hub!")

if __name__ == "__main__":
    main()