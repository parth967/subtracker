# PythonAnywhere Deployment Guide

This guide will help you deploy the Email Analyzer application on PythonAnywhere.

## Prerequisites

- A PythonAnywhere account (free or paid)
- Your email account credentials and app passwords ready

## Step-by-Step Deployment

### 1. Upload Files

1. **Zip your project files** on your local machine
2. **Upload to PythonAnywhere**:
   - Go to the "Files" tab in your PythonAnywhere dashboard
   - Navigate to `/home/yourusername/`
   - Upload and extract your zip file
   - Rename the folder to `mysite` (or your preferred name)

### 2. Install Dependencies

1. **Open a Bash console** in PythonAnywhere
2. **Navigate to your project**:
   ```bash
   cd ~/mysite
   ```
3. **Install requirements**:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

### 3. Configure Environment

1. **Create .env file**:
   ```bash
   cp .env.example .env
   nano .env
   ```

2. **Update .env with your settings**:
   ```
   SECRET_KEY=your-very-secure-secret-key-here
   FLASK_ENV=production
   DATABASE_URL=sqlite:///email_analyzer.db
   ```

3. **Generate a secure secret key** (optional):
   ```bash
   python3.10 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### 4. Set Up Web App

1. **Go to the "Web" tab** in your PythonAnywhere dashboard
2. **Create a new web app**:
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select "Python 3.10"

3. **Configure paths**:
   - **Source code**: `/home/yourusername/mysite`
   - **Working directory**: `/home/yourusername/mysite`

### 5. Configure WSGI

1. **Edit the WSGI configuration file**:
   - Click on the WSGI configuration file link
   - Replace the contents with:

   ```python
   import sys
   import os
   from dotenv import load_dotenv

   # Add your project directory to Python path
   project_home = '/home/yourusername/mysite'  # Update with your username
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   # Load environment variables
   load_dotenv(os.path.join(project_home, '.env'))

   from app import app, db, email_monitor

   # Initialize database and start email monitoring
   with app.app_context():
       db.create_all()
       email_monitor.start_monitoring()

   # WSGI application
   application = app
   ```

2. **Update the path**: Replace `yourusername` with your actual PythonAnywhere username

### 6. Initialize Database

1. **Open a Python console** in PythonAnywhere
2. **Run the setup**:
   ```python
   import os
   os.chdir('/home/yourusername/mysite')  # Update with your username
   
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

### 7. Configure Static Files (Optional)

1. **In the Web tab**, scroll to "Static files"
2. **Add a new static file mapping**:
   - URL: `/static/`
   - Directory: `/home/yourusername/mysite/static/`

### 8. Reload and Test

1. **Click "Reload" button** in the Web tab
2. **Visit your app**: `https://yourusername.pythonanywhere.com`
3. **Add your email configuration** through the web interface

## Database Options

### SQLite (Default)
- Good for personal use
- No additional setup required
- File-based database

### MySQL (Recommended for Production)
1. **Create a MySQL database** in PythonAnywhere
2. **Update .env**:
   ```
   DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere-services.com/username$dbname
   ```
3. **Install MySQL client**:
   ```bash
   pip3.10 install --user mysqlclient
   ```

## Email Provider Setup

### Gmail
1. **Enable 2-Factor Authentication**
2. **Generate App Password**:
   - Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
3. **Use in application**: Your email + generated app password

### Outlook/Hotmail
1. **Enable 2FA** (if not already enabled)
2. **Generate App Password**:
   - Microsoft Account → Security → Advanced security options → App passwords
3. **IMAP Server**: `outlook.office365.com`

### Yahoo
1. **Generate App Password**:
   - Yahoo Account → Account Security → Generate app password
2. **IMAP Server**: `imap.mail.yahoo.com`

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Check if all packages are installed
   pip3.10 list --user
   ```

2. **Database Errors**:
   ```bash
   # Check file permissions
   ls -la ~/mysite/
   ```

3. **Email Connection Issues**:
   - Verify app passwords are correct
   - Check if IMAP is enabled
   - Test with a simple IMAP connection

4. **Application Not Loading**:
   - Check error logs in PythonAnywhere
   - Verify WSGI configuration
   - Check Python path in WSGI file

### Debugging

1. **Check error logs**:
   - Web tab → Error log
   - Server log

2. **Test in console**:
   ```python
   from app import app
   with app.app_context():
       # Test your code here
   ```

## Security Considerations

1. **Use strong secret keys**
2. **Keep app passwords secure**
3. **Enable HTTPS** (automatic on PythonAnywhere)
4. **Regular backups** of your database
5. **Monitor application logs**

## Maintenance

### Regular Tasks
1. **Monitor email processing**
2. **Check application logs**
3. **Backup database** regularly
4. **Update dependencies** periodically

### Updates
1. **Upload new files**
2. **Install new requirements**
3. **Run database migrations** if needed
4. **Reload web app**

## Support

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Email Provider IMAP Guides**: Check your provider's documentation