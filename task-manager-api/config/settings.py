import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///tasks.db")
PORT = int(os.environ.get("PORT", "5000"))

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "dev@example.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "dev-smtp-password-change-me")
