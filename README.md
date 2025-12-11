# Email Analyzer - Job Application Tracker

A Python Flask web application that monitors your email accounts and automatically tracks job applications, replies, and their status. Perfect for job seekers who want to stay organized and track their application progress.

## Features

- **Multi-Email Support**: Configure multiple email accounts to monitor
- **Automatic Email Classification**: Automatically detects job applications, replies, and other emails
- **Status Tracking**: Track application status (Pending, Interview, Accepted, Rejected)
- **Real-time Monitoring**: Continuously monitors your email accounts for new messages
- **Interactive Dashboard**: View statistics and manage your email configurations
- **Manual Status Updates**: Update email status manually through the web interface
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### 1. Local Development

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:5000`

### 2. PythonAnywhere Deployment

1. **Upload files to PythonAnywhere**:
   - Upload all project files to your PythonAnywhere account
   - Place them in `/home/yourusername/mysite/`

2. **Install dependencies**:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

3. **Configure the web app**:
   - Go to the "Web" tab in your PythonAnywhere dashboard
   - Create a new web app (Flask, Python 3.10)
   - Set the source code directory to `/home/yourusername/mysite`
   - Set the WSGI configuration file to `/home/yourusername/mysite/wsgi.py`

4. **Update wsgi.py**:
   - Edit `wsgi.py` and update the `project_home` path to match your directory

5. **Set up environment variables**:
   - Create a `.env` file with your configuration
   - Update `SECRET_KEY` with a secure random string

6. **Configure database** (optional):
   - For production, consider using MySQL instead of SQLite
   - Update `DATABASE_URL` in `.env` accordingly

7. **Reload the web app** in PythonAnywhere dashboard

## Email Configuration

### Gmail Setup
1. Enable 2-factor authentication on your Google account
2. Generate an app password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use your email and the generated app password in the application

### Other Email Providers
- **Outlook/Hotmail**: Use app password if 2FA is enabled
- **Yahoo**: Generate app password in Account Security settings
- **Custom IMAP**: Enter your provider's IMAP server details

## How It Works

1. **Email Monitoring**: The application connects to your email accounts using IMAP
2. **Classification**: Emails are automatically classified based on keywords:
   - Job applications: Contains keywords like "application", "job", "position"
   - Replies: Contains "re:", "reply", "response"
   - Status detection: Automatically detects rejections, interviews, acceptances

3. **Database Storage**: All emails are stored in a local database with metadata
4. **Web Interface**: Access statistics, manage configurations, and update statuses

## Security Notes

- App passwords are stored encrypted in the database
- Use environment variables for sensitive configuration
- The application only reads emails, it doesn't send or modify them
- Consider using HTTPS in production (PythonAnywhere provides this automatically)

## Customization

The application is designed to be extensible. You can:

- Modify email classification rules in the `_analyze_email` method
- Add new email types and statuses
- Customize the web interface templates
- Add new features like email notifications or export functionality

## Troubleshooting

### Common Issues

1. **Email connection fails**:
   - Verify app password is correct
   - Ensure IMAP is enabled in your email provider
   - Check firewall settings

2. **Database errors**:
   - Ensure write permissions in the application directory
   - For MySQL on PythonAnywhere, verify connection string

3. **Application not starting**:
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Check error logs in PythonAnywhere

### Support

For issues specific to:
- **PythonAnywhere**: Check their help documentation
- **Email providers**: Refer to their IMAP setup guides
- **Application bugs**: Check the code comments and error messages

## Future Enhancements

Planned features for future versions:
- Email content analysis using AI
- Integration with job boards
- Email templates for follow-ups
- Advanced reporting and analytics
- Mobile app companion

## License

This project is open source and available under the MIT License.