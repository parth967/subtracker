"""
Free Email Notification Service for RSVP Hub
Uses Python's built-in smtplib (completely free, no API costs)

Supports:
- Gmail SMTP (free, 500 emails/day)
- Outlook/Hotmail SMTP (free)
- Any SMTP server

Setup Instructions:
1. For Gmail: Enable 2-factor auth, create App Password
2. Add credentials to .env file
3. Start sending emails!
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv('.env.production' if os.path.exists('.env.production') else '.env')

class EmailService:
    """Free email service using SMTP (no API costs)"""
    
    def __init__(self):
        # Gmail SMTP (free, 500 emails/day)
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        self.from_name = os.environ.get('FROM_NAME', 'RSVP Hub')
        
        # Alternative: Outlook/Hotmail (also free)
        # self.smtp_server = 'smtp-mail.outlook.com'
        # self.smtp_port = 587
        
    def send_email(self, to_email, subject, html_content, text_content=None):
        """
        Send email using free SMTP
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text fallback (optional)
        """
        # Silently skip if not configured - no errors, app works fine without email
        if not self.smtp_username or not self.smtp_password:
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}: {subject}")
            return True
            
        except Exception as e:
            # Silently fail - don't break the app if email fails
            return False
    
    def send_rsvp_confirmation(self, guest_name, guest_email, invitation):
        """Send RSVP confirmation to guest"""
        subject = f"RSVP Confirmed: {invitation.title}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 RSVP Confirmed!</h1>
                </div>
                <div class="content">
                    <p>Hi {guest_name},</p>
                    <p>Your RSVP for <strong>{invitation.title}</strong> has been confirmed!</p>
                    <p><strong>Event Details:</strong></p>
                    <ul>
                        <li>Date: {invitation.event_date.strftime('%A, %B %d, %Y')}</li>
                        <li>Time: {invitation.event_time or 'TBA'}</li>
                        <li>Venue: {invitation.venue_name or 'TBA'}</li>
                    </ul>
                    <p>We're excited to see you there!</p>
                    <a href="{invitation.share_url}" class="button">View Invitation</a>
                    <p class="footer">This is an automated email from RSVP Hub</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(guest_email, subject, html)
    
    def send_new_rsvp_notification(self, host_email, host_name, invitation, rsvp):
        """Notify host when someone RSVPs"""
        subject = f"New RSVP: {rsvp.guest_name} for {invitation.title}"
        
        status_emoji = {
            'attending': '✅',
            'not_attending': '❌',
            'maybe': '❓'
        }
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .rsvp-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-item {{ text-align: center; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{status_emoji.get(rsvp.status, '📧')} New RSVP Received!</h1>
                </div>
                <div class="content">
                    <p>Hi {host_name},</p>
                    <p><strong>{rsvp.guest_name}</strong> has responded to your invitation!</p>
                    <div class="rsvp-box">
                        <p><strong>Response:</strong> {rsvp.status.title()}</p>
                        <p><strong>Guest Count:</strong> {rsvp.guest_count}</p>
                        {f'<p><strong>Message:</strong> {rsvp.message}</p>' if rsvp.message else ''}
                    </div>
                    <a href="{invitation.share_url}" class="button">View All RSVPs</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(host_email, subject, html)
    
    def send_event_reminder(self, guest_email, guest_name, invitation):
        """Send reminder 1 day before event"""
        subject = f"Reminder: {invitation.title} Tomorrow!"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #feca57; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Event Tomorrow!</h1>
                </div>
                <div class="content">
                    <p>Hi {guest_name},</p>
                    <p>Just a friendly reminder that <strong>{invitation.title}</strong> is tomorrow!</p>
                    <p><strong>Event Details:</strong></p>
                    <ul>
                        <li>Date: {invitation.event_date.strftime('%A, %B %d, %Y')}</li>
                        <li>Time: {invitation.event_time or 'TBA'}</li>
                        <li>Venue: {invitation.venue_name or 'TBA'}</li>
                    </ul>
                    <p>We're looking forward to seeing you!</p>
                    <a href="{invitation.share_url}" class="button">View Invitation</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(guest_email, subject, html)
    
    def send_thank_you_email(self, host_email, host_name, invitation):
        """Send thank you email after event"""
        subject = f"Thank You for Using RSVP Hub - {invitation.title}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🙏 Thank You!</h1>
                </div>
                <div class="content">
                    <p>Hi {host_name},</p>
                    <p>We hope <strong>{invitation.title}</strong> was a huge success!</p>
                    <p>Thank you for using RSVP Hub to manage your event. We'd love to hear about your experience!</p>
                    <p>Create your next invitation anytime - it's always free!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(host_email, subject, html)
    
    def send_weekly_summary(self, host_email, host_name, invitations):
        """Send weekly RSVP summary"""
        subject = "Your Weekly RSVP Summary"
        
        total_rsvps = sum(len(inv.rsvps) for inv in invitations)
        total_attending = sum(inv.attending_count for inv in invitations)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-item {{ text-align: center; background: white; padding: 15px; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Weekly Summary</h1>
                </div>
                <div class="content">
                    <p>Hi {host_name},</p>
                    <p>Here's your weekly RSVP summary:</p>
                    <div class="stats">
                        <div class="stat-item">
                            <strong>{len(invitations)}</strong><br>
                            Active Events
                        </div>
                        <div class="stat-item">
                            <strong>{total_rsvps}</strong><br>
                            Total RSVPs
                        </div>
                        <div class="stat-item">
                            <strong>{total_attending}</strong><br>
                            Attending
                        </div>
                    </div>
                    <p>Keep up the great event planning!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(host_email, subject, html)
    
    def send_milestone_notification(self, host_email, host_name, invitation, milestone):
        """Send notification when reaching RSVP milestones (10, 25, 50, 100 guests)"""
        subject = f"🎉 Milestone Reached: {milestone} RSVPs for {invitation.title}!"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 {milestone} RSVPs!</h1>
                </div>
                <div class="content">
                    <p>Hi {host_name},</p>
                    <p>Congratulations! Your event <strong>{invitation.title}</strong> has reached <strong>{milestone} RSVPs</strong>!</p>
                    <p>That's amazing! Your event is going to be fantastic!</p>
                    <a href="{invitation.share_url}" style="display: inline-block; background: #feca57; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">View RSVPs</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(host_email, subject, html)
    
    def send_rsvp_deadline_reminder(self, host_email, host_name, invitation, days_left):
        """Remind host about RSVP deadline"""
        subject = f"RSVP Deadline Reminder: {days_left} days left for {invitation.title}"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ RSVP Deadline Approaching</h1>
                </div>
                <div class="content">
                    <p>Hi {host_name},</p>
                    <p>Your RSVP deadline for <strong>{invitation.title}</strong> is in <strong>{days_left} days</strong>!</p>
                    <p>Consider sending a reminder to guests who haven't responded yet.</p>
                    <a href="{invitation.share_url}" style="display: inline-block; background: #ef4444; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">Manage RSVPs</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(host_email, subject, html)

# Global instance
email_service = EmailService()

