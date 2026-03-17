"""
Email service for sending verification emails and notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from jinja2 import Template
from typing import Optional
import os

# Email templates
VERIFICATION_EMAIL_TEMPLATE = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background-color: #0070f3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .button { display: inline-block; background-color: #0070f3; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; font-size: 12px; color: #666; padding: 20px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Control Center</h1>
        </div>
        <div class="content">
            <p>Hello {{ first_name }} {{ last_name }},</p>
            <p>Thank you for registering with Control Center. To complete your registration and activate your account, please verify your email address by clicking the button below:</p>
            <a href="{{ verification_link }}" class="button">Verify Email Address</a>
            <p>Or copy this link into your browser:</p>
            <p><code>{{ verification_link }}</code></p>
            <p style="color: #666; font-size: 12px;">This link will expire in 24 hours.</p>
        </div>
        <div class="footer">
            <p>&copy; 2026 Control Center. All rights reserved.</p>
            <p>If you didn't create this account, please ignore this email.</p>
        </div>
    </div>
</body>
</html>
"""

COMPANY_VERIFICATION_PENDING_TEMPLATE = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background-color: #0070f3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .status-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; font-size: 12px; color: #666; padding: 20px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Company Account Verification</h1>
        </div>
        <div class="content">
            <p>Hello {{ contact_person }},</p>
            <p>Thank you for registering {{ company_name }} with Control Center.</p>
            <div class="status-box">
                <strong>Your account status:</strong> Pending Company Verification
            </div>
            <p>Your company account has been created and is awaiting verification by our team. This typically takes 1-2 business days.</p>
            <p><strong>Company Information:</strong></p>
            <ul>
                <li>Company: {{ company_name }}</li>
                <li>NIP: {{ nip }}</li>
                <li>Contact: {{ contact_person }}</li>
            </ul>
            <p>We will review your submission and send you a confirmation email once the verification is complete.</p>
        </div>
        <div class="footer">
            <p>&copy; 2026 Control Center. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

COMPANY_VERIFIED_TEMPLATE = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background-color: #0070f3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .status-box { background-color: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; }
        .button { display: inline-block; background-color: #0070f3; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; font-size: 12px; color: #666; padding: 20px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Company Verified</h1>
        </div>
        <div class="content">
            <p>Hello {{ contact_person }},</p>
            <div class="status-box">
                <strong>✓ Your company has been verified!</strong>
            </div>
            <p>Congratulations! {{ company_name }} has been successfully verified and your account is now active.</p>
            <p>You can now access all features including:</p>
            <ul>
                <li>Project Management</li>
                <li>Billing & Invoicing</li>
                <li>Team Management</li>
                <li>Analytics Dashboard</li>
                <li>API Access</li>
            </ul>
            <a href="{{ login_link }}" class="button">Login to Your Account</a>
        </div>
        <div class="footer">
            <p>&copy; 2026 Control Center. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

COMPANY_REJECTED_TEMPLATE = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background-color: #0070f3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .status-box { background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 20px 0; }
        .footer { text-align: center; font-size: 12px; color: #666; padding: 20px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Company Verification Update</h1>
        </div>
        <div class="content">
            <p>Hello {{ contact_person }},</p>
            <div class="status-box">
                <strong>Your company verification was not approved.</strong>
            </div>
            <p>Unfortunately, we were unable to verify {{ company_name }} at this time.</p>
            <p><strong>Reason:</strong></p>
            <p>{{ reason }}</p>
            <p>Please contact our support team for more information or to resubmit your application with corrected information.</p>
            <p><strong>Support Contact:</strong><br>Email: support@control-center.pl<br>Hours: Monday-Friday 9:00 AM - 5:00 PM CET</p>
        </div>
        <div class="footer">
            <p>&copy; 2026 Control Center. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_server = getattr(settings, 'SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_user = getattr(settings, 'SMTP_USER', '')
        self.smtp_password = getattr(settings, 'SMTP_PASSWORD', '')
        self.email_from = getattr(settings, 'EMAIL_FROM', 'noreply@control-center.pl')
        self.frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    
    def send_verification_email(self, email: str, first_name: str, last_name: str, token: str) -> bool:
        """Send email verification link"""
        try:
            verification_link = f"{self.frontend_url}/#/verify-email?token={token}"
            
            template = Template(VERIFICATION_EMAIL_TEMPLATE)
            html_content = template.render(
                first_name=first_name,
                last_name=last_name,
                verification_link=verification_link
            )
            
            return self._send_email(
                to_email=email,
                subject="Verify Your Email - Control Center",
                html_content=html_content
            )
        except Exception as e:
            print(f"Error sending verification email: {str(e)}")
            return False
    
    def send_company_pending_email(self, email: str, contact_person: str, 
                                  company_name: str, nip: str) -> bool:
        """Send company pending verification email"""
        try:
            template = Template(COMPANY_VERIFICATION_PENDING_TEMPLATE)
            html_content = template.render(
                contact_person=contact_person,
                company_name=company_name,
                nip=nip
            )
            
            return self._send_email(
                to_email=email,
                subject="Company Verification Pending - Control Center",
                html_content=html_content
            )
        except Exception as e:
            print(f"Error sending company pending email: {str(e)}")
            return False
    
    def send_company_verified_email(self, email: str, contact_person: str, 
                                   company_name: str) -> bool:
        """Send company verified email"""
        try:
            template = Template(COMPANY_VERIFIED_TEMPLATE)
            html_content = template.render(
                contact_person=contact_person,
                company_name=company_name,
                login_link=f"{self.frontend_url}/login"
            )
            
            return self._send_email(
                to_email=email,
                subject="Company Verified - Control Center",
                html_content=html_content
            )
        except Exception as e:
            print(f"Error sending company verified email: {str(e)}")
            return False
    
    def send_company_rejected_email(self, email: str, contact_person: str, 
                                   company_name: str, reason: str) -> bool:
        """Send company rejected email"""
        try:
            template = Template(COMPANY_REJECTED_TEMPLATE)
            html_content = template.render(
                contact_person=contact_person,
                company_name=company_name,
                reason=reason
            )
            
            return self._send_email(
                to_email=email,
                subject="Company Verification Update - Control Center",
                html_content=html_content
            )
        except Exception as e:
            print(f"Error sending company rejected email: {str(e)}")
            return False
    
    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Internal method to send email via SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_from
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            if self.smtp_user and self.smtp_password:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
            else:
                # For testing/development without SMTP configured
                print(f"[EMAIL] To: {to_email}, Subject: {subject}")
                return True
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False


# Global email service instance
email_service = EmailService()
