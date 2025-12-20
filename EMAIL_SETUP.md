# 📧 Free Email Setup Guide

RSVP Hub uses **completely free** email service with Python's built-in `smtplib` - **no API costs!**

## 🎯 Quick Setup (5 minutes)

### Option 1: Gmail (Recommended - 500 emails/day free)

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Create App Password**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Other (Custom name)"
   - Enter "RSVP Hub"
   - Copy the 16-character password

3. **Add to `.env` file:**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   FROM_EMAIL=your-email@gmail.com
   FROM_NAME=RSVP Hub
   ```

### Option 2: Outlook/Hotmail (Also Free)

1. **Enable 2-Factor Authentication**
   - Go to [Microsoft Account Security](https://account.microsoft.com/security)

2. **Create App Password**
   - Go to Security settings
   - Create app password for "Mail"
   - Copy the password

3. **Add to `.env` file:**
   ```env
   SMTP_SERVER=smtp-mail.outlook.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@outlook.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@outlook.com
   FROM_NAME=RSVP Hub
   ```

## ✨ Unique Email Features

### 1. **RSVP Confirmations**
- Guests get beautiful confirmation emails when they RSVP
- Includes event details and invitation link

### 2. **Host Notifications**
- Instant email when someone RSVPs
- Shows guest name, response, and message

### 3. **Event Reminders**
- Automatic reminders 1 day before events
- Sent to all guests who RSVPed "attending"

### 4. **Milestone Celebrations**
- Get notified at 10, 25, 50, 100 RSVPs
- Celebrate your event's success!

### 5. **Weekly Summaries**
- Weekly digest of all RSVP activity
- Track your event planning progress

### 6. **Thank You Emails**
- Sent after events to show appreciation
- Encourages repeat usage

## 🔧 Setup Scheduled Tasks (Optional)

For automatic reminders and summaries, set up cron jobs:

### Daily Reminders (1 day before events)
```bash
# Add to crontab (crontab -e)
0 9 * * * curl https://parth967.pythonanywhere.com/tasks/send-reminders
```

### Weekly Summaries (Every Monday)
```bash
# Add to crontab
0 9 * * 1 curl https://parth967.pythonanywhere.com/tasks/send-weekly-summaries
```

## 📊 Email Limits

- **Gmail**: 500 emails/day (free)
- **Outlook**: 300 emails/day (free)
- **No API costs**: Uses built-in Python smtplib

## 🎨 Email Templates

All emails are beautifully designed with:
- Gradient headers
- Responsive design
- Brand colors
- Clear call-to-action buttons

## 🔒 Security

- Uses TLS encryption
- App passwords (not your main password)
- Secure SMTP connection

## ✅ Testing

Test your email setup:
1. Create an invitation
2. RSVP as a guest
3. Check your email inbox!

## 🆘 Troubleshooting

**Emails not sending?**
- Check SMTP credentials in `.env`
- Verify app password is correct
- Check spam folder
- Ensure 2FA is enabled

**Rate limits?**
- Gmail: 500/day is usually enough
- Consider Outlook for higher limits
- Or use multiple email accounts

## 💡 Pro Tips

1. **Use a dedicated email** for RSVP Hub
2. **Monitor your email count** to stay within limits
3. **Enable all notifications** to maximize engagement
4. **Test with your own email** first

---

**That's it!** Your email system is now ready - completely free, no API costs! 🎉

