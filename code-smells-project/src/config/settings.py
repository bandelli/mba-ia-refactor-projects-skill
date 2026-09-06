import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
DB_PATH = os.environ.get("DB_PATH", "loja.db")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "dev-admin-token-change-me")
PORT = int(os.environ.get("PORT", "5000"))
