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
    msg = EmailMessage()
    msg['Subject'] = '🚀 Your Travel Agent Verification Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    # HTML Template
    html_content = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <div style="background: #2c3e50; padding: 20px; text-align: center; color: white;">
                    <h1>Global AI Travel Agent</h1>
                </div>
                <div style="padding: 30px; text-align: center;">
                    <p style="font-size: 18px; color: #333;">Welcome aboard!</p>
                    <p style="color: #666;">Use the secure 8-digit code below to verify your account and start planning your next adventure.</p>
                    <div style="margin: 30px 0; padding: 15px; background: #ecf0f1; border-radius: 5px; font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #2980b9;">
                        {otp}
                    </div>
                    <p style="font-size: 12px; color: #999;">This code will expire in 10 minutes. If you didn't request this, please ignore this email.</p>
                </div>
                <div style="background: #f9f9f9; padding: 15px; text-align: center; font-size: 12px; color: #bdc3c7;">
                    &copy; 2026 AI Travel Agent Inc. | Powered by LangGraph
                </div>
            </div>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
   
   