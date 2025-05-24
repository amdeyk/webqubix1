# Section 1: Email service for sending notifications and confirmations
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import logging

from app.config import settings

class EmailService:
    """Service for handling email notifications"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        self.contact_email = settings.CONTACT_EMAIL
    
    # Section 2: Send inquiry notification to admin
    async def send_inquiry_notification(self, inquiry_id: int, form_data: Dict):
        """Send new inquiry notification to admin"""
        try:
            subject = f"New Inquiry #{inquiry_id} - Qubix Events"
            
            html_content = f"""
            <html>
            <body>
                <h2>New Inquiry Received</h2>
                <p><strong>Inquiry ID:</strong> {inquiry_id}</p>
                <p><strong>Name:</strong> {form_data.get('name')}</p>
                <p><strong>Email:</strong> {form_data.get('email')}</p>
                <p><strong>Phone:</strong> {form_data.get('phone', 'Not provided')}</p>
                <p><strong>Company:</strong> {form_data.get('company', 'Not provided')}</p>
                <p><strong>Event Type:</strong> {form_data.get('event_type', 'Not specified')}</p>
                <p><strong>Event Date:</strong> {form_data.get('event_date', 'Not specified')}</p>
                <p><strong>Location:</strong> {form_data.get('location', 'Not specified')}</p>
                <p><strong>Expected Attendees:</strong> {form_data.get('expected_attendees', 'Not specified')}</p>
                <p><strong>Budget Range:</strong> {form_data.get('budget_range', 'Not specified')}</p>
                <p><strong>Message:</strong></p>
                <p>{form_data.get('message')}</p>
                <p><strong>Requirements:</strong></p>
                <p>{form_data.get('requirements', 'None specified')}</p>
                <hr>
                <p><small>Received from Qubix Events website on {inquiry_id}</small></p>
            </body>
            </html>
            """
            
            await self._send_email(self.contact_email, subject, html_content)
            logging.info(f"Inquiry notification sent for ID: {inquiry_id}")
            
        except Exception as e:
            logging.error(f"Failed to send inquiry notification: {str(e)}")

    # Section 3: Send confirmation email to customer
    async def send_confirmation_email(self, customer_email: str, customer_name: str):
        """Send confirmation email to customer"""
        try:
            subject = "Thank you for contacting Qubix Events & Conferences"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <img src="{settings.BASE_URL}/static/images/qubix-logo.png" alt="Qubix Events" style="max-width: 200px; margin-bottom: 20px;">
                    
                    <h2 style="color: #2c5aa0;">Thank You for Your Inquiry!</h2>
                    
                    <p>Dear {customer_name},</p>
                    
                    <p>Thank you for reaching out to Qubix Events & Conferences. We have received your inquiry and our team will review your requirements carefully.</p>
                    
                    <p><strong>What happens next?</strong></p>
                    <ul>
                        <li>Our event specialists will review your requirements within 24 hours</li>
                        <li>You'll receive a personalized response with initial recommendations</li>
                        <li>We'll schedule a consultation call to discuss your event in detail</li>
                        <li>A customized proposal will be prepared based on your needs</li>
                    </ul>
                    
                    <p><strong>Need immediate assistance?</strong></p>
                    <p>Call us at: <a href="tel:+919899339005">+91-98993-39005</a></p>
                    <p>Email: <a href="mailto:{settings.CONTACT_EMAIL}">{settings.CONTACT_EMAIL}</a></p>
                    
                    <hr style="margin: 30px 0;">
                    
                    <h3 style="color: #2c5aa0;">Why Choose Qubix Events?</h3>
                    <ul>
                        <li>200+ Medical Conferences Successfully Organized</li>
                        <li>400+ Corporate Events Managed</li>
                        <li>1000+ Virtual Conferences Hosted</li>
                        <li>50+ Exhibitions & Trade Shows</li>
                        <li>Pan-India Presence with offices in Delhi, Kolkata & Bangalore</li>
                    </ul>
                    
                    <p style="margin-top: 30px;">Best regards,<br>
                    <strong>Qubix Events & Conferences Team</strong></p>
                    
                    <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
                        <p style="margin: 0; font-size: 12px; color: #666;">
                            This email was sent from Qubix Events & Conferences Pvt. Ltd.<br>
                            Visit our website: <a href="{settings.BASE_URL}">{settings.BASE_URL}</a>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            await self._send_email(customer_email, subject, html_content)
            logging.info(f"Confirmation email sent to: {customer_email}")
            
        except Exception as e:
            logging.error(f"Failed to send confirmation email: {str(e)}")

    # Section 4: Send quote request notification
    async def send_quote_request_notification(self, inquiry_id: int, quote_data: Dict):
        """Send priority quote request notification to admin"""
        try:
            subject = f"🚨 PRIORITY QUOTE REQUEST #{inquiry_id} - Qubix Events"
            
            html_content = f"""
            <html>
            <body>
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                    <h2 style="color: #856404; margin: 0;">⚡ PRIORITY QUOTE REQUEST</h2>
                </div>
                
                <p><strong>Quote Request ID:</strong> {inquiry_id}</p>
                <p><strong>Name:</strong> {quote_data.get('name')}</p>
                <p><strong>Email:</strong> {quote_data.get('email')}</p>
                <p><strong>Phone:</strong> {quote_data.get('phone')}</p>
                <p><strong>Company:</strong> {quote_data.get('company')}</p>
                <p><strong>Service:</strong> {quote_data.get('service_id')}</p>
                <p><strong>Event Date:</strong> {quote_data.get('event_date')}</p>
                <p><strong>Location:</strong> {quote_data.get('location')}</p>
                <p><strong>Expected Attendees:</strong> {quote_data.get('expected_attendees')}</p>
                <p><strong>Budget Range:</strong> {quote_data.get('budget_range')}</p>
                <p><strong>Requirements:</strong></p>
                <p>{quote_data.get('requirements')}</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <p style="margin: 0; color: #155724;"><strong>⏰ Response Target: 6 hours</strong></p>
                </div>
            </body>
            </html>
            """
            
            await self._send_email(self.contact_email, subject, html_content)
            logging.info(f"Priority quote notification sent for ID: {inquiry_id}")
            
        except Exception as e:
            logging.error(f"Failed to send quote notification: {str(e)}")

    # Section 5: Private method to send emails
    async def _send_email(self, to_email: str, subject: str, html_content: str):
        """Private method to handle actual email sending"""
        if not all([self.smtp_server, self.username, self.password]):
            logging.warning("Email configuration not complete. Email not sent.")
            return
            
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to_email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
        except Exception as e:
            logging.error(f"Email sending failed: {str(e)}")
            raise