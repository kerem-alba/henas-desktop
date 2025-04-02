from datetime import timedelta

class Config:
    JWT_SECRET_KEY = "supersecretkey" 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
