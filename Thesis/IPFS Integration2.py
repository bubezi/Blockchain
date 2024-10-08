import ipfshttpclient
from cryptography.fernet import Fernet
import time

class IPFSManager:
    def __init__(self, max_retries=3, retry_delay=1):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connect_to_ipfs()
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def connect_to_ipfs(self):
        for attempt in range(self.max_retries):
            try:
                self.client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
                return
            except ipfshttpclient.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    def encrypt_and_upload(self, model_update):
        encrypted_update = self.fernet.encrypt(model_update.encode())
        for attempt in range(self.max_retries):
            try:
                res = self.client.add_bytes(encrypted_update)
                return res['Hash']
            except ipfshttpclient.exceptions.TimeoutError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

    def download_and_decrypt(self, ipfs_hash):
        for attempt in range(self.max_retries):
            try:
                encrypted_update = self.client.cat(ipfs_hash)
                return self.fernet.decrypt(encrypted_update).decode()
            except ipfshttpclient.exceptions.TimeoutError:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise

# Usage
ipfs_manager = IPFSManager()
ipfs_hash = ipfs_manager.encrypt_and_upload("Model update data")
retrieved_update = ipfs_manager.download_and_decrypt(ipfs_hash)
