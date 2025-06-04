from cryptography.fernet import Fernet
from django.conf import settings

# Clé secrète dans settings.py (en base64)
SECRET_ENCRYPTION_KEY = getattr(settings, 'SECRET_ENCRYPTION_KEY', None)
fernet = Fernet(SECRET_ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
