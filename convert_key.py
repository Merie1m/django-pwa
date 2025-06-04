#!/usr/bin/env python3
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def convert_vapid_key_to_webpush_format(current_base64_key):
    """
    Convertit une clé VAPID du format DER/SubjectPublicKeyInfo 
    vers le format raw requis pour Web Push
    """
    try:
        # Ajouter le padding si nécessaire
        padding = '='.repeat((4 - len(current_base64_key) % 4) % 4)
        padded_key = current_base64_key + padding
        
        # Décoder la clé base64 actuelle
        der_bytes = base64.urlsafe_b64decode(padded_key)
        
        # Charger la clé publique depuis les bytes DER
        public_key = serialization.load_der_public_key(der_bytes, backend=default_backend())
        
        # Extraire les coordonnées brutes (format X9.62 UncompressedPoint)
        raw_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        # Encoder en base64 URL-safe sans padding
        webpush_key = base64.urlsafe_b64encode(raw_bytes).rstrip(b'=').decode('utf-8')
        
        return webpush_key
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion : {e}")
        return None

if __name__ == "__main__":
    # Votre clé actuelle
    current_key = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWkV1v0KJ0ZjCxEvSLdseQhetXRwuLzVEHG-MRprOHHNKFEpz4WYvBg8cetDSTgkor4E_aSG4lvJjDT1UpCpL6A"
    
    print("🔄 Conversion de votre clé VAPID...")
    print(f"📤 Clé actuelle : {current_key}")
    print(f"📏 Longueur actuelle : {len(current_key)} caractères\n")
    
    # Conversion
    webpush_key = convert_vapid_key_to_webpush_format(current_key)
    
    if webpush_key:
        print("✅ Conversion réussie !")
        print(f"📥 Clé convertie : {webpush_key}")
        print(f"📏 Longueur convertie : {len(webpush_key)} caractères")
        print("\n" + "="*60)
        print("🚀 UTILISEZ CETTE CLÉ DANS VOTRE JAVASCRIPT :")
        print("="*60)
        print(f'applicationServerKey: urlBase64ToUint8Array("{webpush_key}")')
        print("="*60)
    else:
        print("❌ Échec de la conversion.")
        print("Votre clé pourrait ne pas être au bon format initial.")