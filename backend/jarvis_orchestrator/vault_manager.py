import os
import json
from cryptography.fernet import Fernet
from fastapi import HTTPException

# Carpeta segura para el vault
VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../AXYNTRAX_VAULT'))
if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

VAULT_FILE = os.path.join(VAULT_DIR, "secure_vault.enc")
KEY_FILE = os.path.join(VAULT_DIR, "master_key.key")

def _get_or_create_key() -> bytes:
    """Obtiene la clave maestra del Vault o genera una si no existe."""
    master_key = os.getenv("AXYNTRAX_VAULT_MASTER_KEY")
    if master_key:
        return master_key.encode()

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("[VAULT] ALERTA: Nueva Master Key generada en AXYNTRAX_VAULT/master_key.key")
        return key

def _get_fernet() -> Fernet:
    return Fernet(_get_or_create_key())

def _load_vault() -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        with open(VAULT_FILE, "rb") as f:
            encrypted_data = f.read()
        f_obj = _get_fernet()
        decrypted_data = f_obj.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception as e:
        print(f"[VAULT] Error leyendo Vault: {e}")
        return {}

def _save_vault(data: dict):
    try:
        json_data = json.dumps(data).encode()
        f_obj = _get_fernet()
        encrypted_data = f_obj.encrypt(json_data)
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted_data)
    except Exception as e:
        print(f"[VAULT] Error guardando en Vault: {e}")

class VaultManager:
    @staticmethod
    def store_secret(key: str, value: str):
        """Guarda un secreto encriptado en el Vault."""
        data = _load_vault()
        data[key] = value
        _save_vault(data)
        return True

    @staticmethod
    def get_secret(key: str, fallback: str = None) -> str:
        """Obtiene un secreto del Vault, o cae de vuelta a variable de entorno."""
        data = _load_vault()
        if key in data:
            return data[key]
        
        # Fallback a entorno
        env_val = os.getenv(key)
        if env_val:
            return env_val
            
        if fallback:
            return fallback
            
        raise HTTPException(status_code=500, detail=f"Secreto '{key}' no encontrado en el Vault ni en el entorno.")

    @staticmethod
    def delete_secret(key: str):
        data = _load_vault()
        if key in data:
            del data[key]
            _save_vault(data)
            return True
        return False
