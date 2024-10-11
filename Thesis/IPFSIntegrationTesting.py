import unittest
from python.ipfs_manager import IPFSManager

class TestIPFSManager(unittest.TestCase):
    def setUp(self):
        self.ipfs_manager = IPFSManager()

    def test_encrypt_upload_download_decrypt(self):
        original_data = "Test model update data"
        ipfs_hash = self.ipfs_manager.encrypt_and_upload(original_data)
        retrieved_data = self.ipfs_manager.download_and_decrypt(ipfs_hash)
        self.assertEqual(original_data, retrieved_data)

if __name__ == '__main__':
    unittest.main()
