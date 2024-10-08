import ipfshttpclient
from cryptography.fernet import Fernet

class IPFSManager:
    def __init__(self):
        self.client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def encrypt_and_upload(self, model_update):
        encrypted_update = self.fernet.encrypt(model_update.encode())
        res = self.client.add_bytes(encrypted_update)
        return res['Hash']

    def download_and_decrypt(self, ipfs_hash):
        encrypted_update = self.client.cat(ipfs_hash)
        decrypted_update = self.fernet.decrypt(encrypted_update)
        return decrypted_update.decode()

# Usage
ipfs_manager = IPFSManager()
ipfs_hash = ipfs_manager.encrypt_and_upload("Model update data")
retrieved_update = ipfs_manager.download_and_decrypt(ipfs_hash)
