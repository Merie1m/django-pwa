from cryptography.fernet import Fernet

# Génère une clé symétrique (mot de passe pour chiffrer)
key = Fernet.generate_key()
cipher = Fernet(key)

# Lis ta clé privée
with open("vapid_private.pem", "rb") as f:
    private_key_data = f.read()

# Chiffre la clé privée
encrypted_private_key = cipher.encrypt(private_key_data)

# Sauvegarde la clé chiffrée
with open("vapid_private_encrypted.pem", "wb") as f:
    f.write(encrypted_private_key)

# Affiche la clé symétrique (à garder secrète pour déchiffrer)
print("Garde cette clé pour déchiffrer ta clé privée :", key.decode())
