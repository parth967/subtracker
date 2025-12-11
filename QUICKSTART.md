# Quick Start Guide

## Local Development (5 minutes)

1. **Install dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Initialize the application**:
   ```bash
   python setup.py
   ```

3. **Start the application**:
   ```bash
   python app.py
   ```

4. **Open your browser**: Go to `http://localhost:5000`

5. **Add your email**: Click "Add Email" and configure your email account

## PythonAnywhere Deployment (10 minutes)

1. **Upload files** to `/home/yourusername/mysite/`

2. **Install dependencies**:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

3. **Create web app**:
   - Web tab → Add new web app → Manual configuration → Python 3.10
   - Source code: `/home/yourusername/mysite`
   - WSGI file: Use the provided `wsgi.py` (update the path)

4. **Initialize database**:
   ```bash
   cd ~/mysite
   python3.10 setup.py
   ```

5. **Reload web app** and visit your site!

## Email Setup

### Gmail (Recommended)
1. Enable 2-factor authentication
2. Generate app password: Google Account → Security → App passwords
3. Use your email + app password in the application

### Other Providers
- **Outlook**: `outlook.office365.com`
- **Yahoo**: `imap.mail.yahoo.com`
- **Custom**: Enter your IMAP server details

## Features

- ✅ **Multi-email monitoring**
- ✅ **Automatic job application detection**
- ✅ **Status tracking** (Pending, Interview, Accepted, Rejected)
- ✅ **Real-time dashboard**
- ✅ **Manual status updates**
- ✅ **Responsive design**

## Next Steps

1. **Configure your emails** through the web interface
2. **Let it run** - the system monitors automatically
3. **Check the dashboard** for statistics and recent emails
4. **Update statuses** manually as needed

## Need Help?

- Check `README.md` for detailed documentation
- See `DEPLOYMENT.md` for deployment troubleshooting
- Review error logs if something goes wrong