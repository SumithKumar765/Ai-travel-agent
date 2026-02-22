from fastapi import FastAPI, HTTPException
from app.schemas import UserEmail, VerifyOTP
from app.auth import generate_8_digit_otp, send_otp_email, otp_storage

app = FastAPI(title="AI Travel Agent API")

@app.post("/api/auth/request-otp")
async def request_otp(user: UserEmail):
    otp = generate_8_digit_otp()
    
    # Store OTP (in a real app, you would add an expiration timestamp here)
    otp_storage[user.email] = otp 
    
    success = send_otp_email(user.email, otp)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send OTP email. Check your SMTP credentials.")
        
    return {"message": f"8-digit OTP sent successfully to {user.email}"}

@app.post("/api/auth/verify-otp")
async def verify_otp(data: VerifyOTP):
    stored_otp = otp_storage.get(data.email)
    
    if not stored_otp:
        raise HTTPException(status_code=400, detail="No OTP requested for this email.")
        
    if stored_otp == data.otp:
        # Clear the OTP after successful verification
        del otp_storage[data.email]
        return {"message": "Email verified successfully! You are logged in."}
    else:
        raise HTTPException(status_code=401, detail="Invalid 8-digit OTP.")