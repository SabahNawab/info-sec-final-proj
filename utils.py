
import base64
import hashlib
from cryptography.fernet import Fernet
from pqc.kem import mceliece6960119 as kemalg


private_key, shared_key, ct, secret_s = None, None, None, None

def key_create_fer(bytes_recv):
    return base64.urlsafe_b64encode(hashlib.sha256(bytes_recv).digest())

def key_creation():
    global private_key, shared_key
    private_key, shared_key = kemalg.keypair()
    return base64.b64encode(private_key).decode(), base64.b64encode(shared_key).decode()

def mes_enc(message):
    global private_key, ct, secret_s
    if not private_key:
        raise ValueError("Keys not generated.")
    secret_s, ct = kemalg.encap(private_key)
    fernet = Fernet(key_create_fer(secret_s))
    encrypted_msg = fernet.encrypt(message.encode()).decode()
    ct_encoded = base64.b64encode(ct).decode()
    return encrypted_msg, ct_encoded

def mes_dry(encrypted_msg):
    global shared_key, ct
    if not shared_key or not ct:
        raise ValueError("Missing keys or ciphertext.")
    recovered_secret = kemalg.decap(ct, shared_key)
    fernet = Fernet(key_create_fer(recovered_secret))
    decrypted_msg = fernet.decrypt(encrypted_msg.encode()).decode()
    return decrypted_msg
