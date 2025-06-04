from vapid_keys import get_vapid_private_key_base64, get_vapid_public_key_base64

def test_keys():
    private_key = get_vapid_private_key_base64()
    public_key = get_vapid_public_key_base64()

    print("Clé privée VAPID (base64 urlsafe) :")
    print(private_key)
    print("\nClé publique VAPID (base64 urlsafe) :")
    print(public_key)

if __name__ == "__main__":
    test_keys()
