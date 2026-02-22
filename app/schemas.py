from pydantic import BaseModel, EmailStr

class UserEmail(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str