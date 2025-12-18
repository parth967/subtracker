# 🚀 InviteMe PythonAnywhere Deployment Guide

This guide will help you deploy InviteMe to PythonAnywhere with MySQL database and user authentication.

## 📋 Prerequisites

- PythonAnywhere account
- MySQL database access (Parth967$inviteme)
- Basic knowledge of PythonAnywhere interface

## 🗄️ Database Setup

### 1. Create MySQL Database

1. Go to PythonAnywhere **Databases** tab
2. Create a new database: `Parth967$inviteme`
3. Note your database credentials:
   - **Host**: `Parth967.mysql.pythonanywhere-services.com`
   - **Username**: `Parth967`
   - **Password**: `khushali979797`
   - **Database**: `Parth967$inviteme`

### 2. Update Environment Configuration

The `.env.production` file is already configured with your MySQL credentials:

```env
# Production Configuration for PythonAnywhere
SECRET_KEY=your-super-secure-secret-key-here-change-this
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://Parth967:khushali979797@Parth967.mysql.pythonanywhere-services.com/Parth967$inviteme?charset=utf8mb4
APP_NAME=InviteMe
APP_URL=https://parth967.pythonanywhere.com
```

## 📁 File Upload

### 1. Upload Project Files

Upload all project files to `/home/Parth967/inviteme/`:

```
inviteme/
├── app.py
├── wsgi.py
├── migrate_db.py
├── requirements.txt
├── .env.production
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── create_invitation.html
│   ├── view_invitation.html
│   ├── manage_invitation.html
│   ├── template_gallery.html
│   └── auth/
│       ├── login.html
│       └── register.html
└── static/ (if any)
```

### 2. Install Dependencies

In a **Bash console** on PythonAnywhere:

```bash
cd /home/Parth967/inviteme
pip3.10 install --user -r requirements.txt
```

## 🔧 Web App Configuration

### 1. Create Web App

1. Go to **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**

### 2. Configure WSGI File

1. Click on **WSGI configuration file** link
2. Replace the contents with:

```python
#!/usr/bin/python3.10

import sys
import os
from dotenv import load_dotenv

# Add your project directory to sys.path
project_home = '/home/Parth967/inviteme'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
load_dotenv(os.path.join(project_home, '.env.production'))

# Import your Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
```

### 3. Set Working Directory

In the **Web** tab, set:
- **Source code**: `/home/Parth967/inviteme`
- **Working directory**: `/home/Parth967/inviteme`

## 🗃️ Database Initialization

### 1. Initialize Database

In a **Bash console**:

```bash
cd /home/Parth967/inviteme
python3.10 migrate_db.py init
```

### 2. Create Admin User (Optional)

You can create an admin user by running Python in the console:

```bash
cd /home/Parth967/inviteme
python3.10
```

Then in Python:

```python
from app import app, db, User
with app.app_context():
    admin = User(
        username='admin',
        email='admin@inviteme.com',
        full_name='Administrator'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

## 🌐 Domain Configuration

### 1. Set Custom Domain (Optional)

If you have a custom domain:
1. Go to **Web** tab
2. Add your domain in **Domain** section
3. Update `APP_URL` in `.env.production`

### 2. HTTPS Configuration

PythonAnywhere provides free HTTPS for `.pythonanywhere.com` domains automatically.

## 🔐 Security Configuration

### 1. Update Secret Key

**Important**: Change the `SECRET_KEY` in `.env.production`:

```bash
# Generate a new secret key
python3.10 -c "import secrets; print(secrets.token_hex(32))"
```

Update `.env.production` with the new key.

### 2. Environment Variables

For additional security, you can set environment variables in PythonAnywhere:
1. Go to **Files** tab
2. Edit `.bashrc` file
3. Add: `export SECRET_KEY="your-new-secret-key"`

## 🚀 Launch Application

### 1. Reload Web App

1. Go to **Web** tab
2. Click **Reload** button
3. Wait for the green checkmark

### 2. Test Application

Visit your application at:
- **Free domain**: `https://parth967.pythonanywhere.com`
- **Custom domain**: Your configured domain

### 3. Create First Account

1. Go to your website
2. Click **Sign Up**
3. Create your account
4. Start creating invitations!

## 📊 Features Available

### ✅ **User Authentication**
- Secure user registration and login
- Password hashing with Werkzeug
- User isolation (users only see their own invitations)

### ✅ **11 Beautiful Templates**
- Classic Elegance
- Modern Minimalist
- Floral Garden
- Vintage Charm
- Festive Celebration
- Corporate Professional
- Luxury Gold
- Ocean Breeze
- Sunset Romance
- Neon Party
- Forest Green

### ✅ **Full RSVP Management**
- Real-time RSVP tracking
- Guest information collection
- Analytics and charts
- QR code generation
- Social media sharing

### ✅ **Mobile Responsive**
- Perfect on all devices
- Touch-friendly interface
- Fast loading times

## 🔧 Maintenance

### Database Backup

```bash
cd /home/Parth967/inviteme
python3.10 migrate_db.py backup
```

### Database Status

```bash
python3.10 migrate_db.py status
```

### View Logs

Check error logs in PythonAnywhere **Web** tab under **Log files**.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `--user` flag
2. **Database Connection**: Verify MySQL credentials in `.env.production`
3. **Template Not Found**: Check file paths and permissions
4. **Static Files**: Configure static files in **Web** tab if needed

### Getting Help

- Check PythonAnywhere **Error log**
- Use **Bash console** for debugging
- Test database connection manually

## 🎉 Success!

Your InviteMe platform is now live! Users can:

1. **Register** for free accounts
2. **Create** beautiful invitations
3. **Share** via links and QR codes
4. **Track** RSVPs in real-time
5. **Manage** multiple events

**Live URL**: `https://parth967.pythonanywhere.com`

---

**🎊 Congratulations! Your invitation platform is ready for users!**