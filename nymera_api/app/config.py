from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    def __init__(self):
        # BD
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        
        self.FRONTEND_URL = os.getenv("FRONTEND_URL")
        
        # JWT
        self.JWT_SECRET = os.getenv("JWT_SECRET")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
        self.JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

        # Email
        self.RESEND_API_KEY = os.getenv("RESEND_API_KEY")

        
settings = Settings()
