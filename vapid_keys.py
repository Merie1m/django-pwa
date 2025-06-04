from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

def get_vapid_private_key():
    # Passphrase que tu as reçu après le chiffrement
    passphrase = b'KpVXO6WkFvAYmsQS323dEw6gfP1mpbkcKNDOMXBQRPY='

    with open('vapid_private_encrypted.pem', 'rb') as f:
        encrypted_key = f.read()

    fernet = Fernet(passphrase)
    decrypted_key = fernet.decrypt(encrypted_key)

    return decrypted_key.decode()
def get_vapid_private_key_base64():
    decrypted_key_pem = get_vapid_private_key().encode()

    private_key = serialization.load_pem_private_key(
        decrypted_key_pem,
        password=None,
        backend=default_backend()
    )

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    private_b64 = base64.urlsafe_b64encode(private_bytes).rstrip(b'=').decode('utf-8')

    return private_b64

def get_vapid_public_key():
    with open('vapid_public.pem', 'r') as f:
        return f.read()
    
def get_vapid_public_key_base64():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend

    pem = get_vapid_public_key().encode()

    public_key = serialization.load_pem_public_key(pem, backend=default_backend())

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    public_b64 = base64.urlsafe_b64encode(public_bytes).rstrip(b'=').decode('utf-8')

    return public_b64
