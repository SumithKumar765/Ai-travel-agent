import smtplib
import secrets
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# In-memory dictionary to store OTPs temporarily 
# (For a production environment, we would use a Vector DB or Redis)
otp_storage = {}

def generate_8_digit_otp() -> str:
    """Generates a secure 8-digit numeric OTP."""
    return ''.join(str(secrets.randbelow(10)) for _ in range(8))

def send_otp_email(receiver_email: str, otp: str) -> bool:
    """Sends the 8-digit OTP via SMTP."""
    msg = EmailMessage()
    msg.set_content(f"Welcome to your AI Travel Agent! \n\nYour 8-digit verification code is: {otp}\n\nThis code will expire shortly.")
    msg['Subject'] = 'Your Travel Agent Verification Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False