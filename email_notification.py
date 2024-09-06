import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class EmailNotifier:
    def __init__(self):
        self.sender = 'your_email@example.com'
        self.recipient = 'recipient@example.com'
        self.smtp_server = 'smtp.example.com'
        self.password = 'your_password'

    def send(self, report_file):
        subject = "Daily Political Analysis Report"
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = subject

        with open(report_file, 'r') as f:
            report_content = f.read()

        msg.attach(MIMEText(report_content, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.starttls()
           
