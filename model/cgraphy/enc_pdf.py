import os
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class PDFEncryptor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.encrypted_file_combined_name = f"Encrypted_{input_file.filename}"
        self.aes_key = secrets.token_bytes(16)
        self.aes_key_hex = self.aes_key.hex()
        self.des3_key = secrets.token_bytes(24)
        self.des3_key_hex = self.des3_key.hex()
        
        # print("AES KEY: " + self.aes_key_hex)
        # print("3DES KEY: " + self.des3_key_hex)

    def pad_pdf(self, data):
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    def encrypt_pdf_with_aes(self, password):
        pdf_data = self.input_file.read()
        salt_aes = os.urandom(16)
        kdf_aes = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_aes,
            iterations=100000,
            backend=default_backend()
        )
        key_aes = kdf_aes.derive(password.encode())

        iv_aes = os.urandom(16)
        cipher = Cipher(algorithms.AES(key_aes), modes.CFB(iv_aes), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_pdf_data_aes = encryptor.update(self.pad_pdf(pdf_data)) + encryptor.finalize()
        self.encrypted_file_combined = salt_aes + iv_aes + encrypted_pdf_data_aes
        
        return self.encrypted_file_combined

    def encrypt_pdf_with_3des(self, password):
        salt_3des = os.urandom(16)
        kdf_3des = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=24,
            salt=salt_3des,
            iterations=100000,
            backend=default_backend()
        )
        key_3des = kdf_3des.derive(password.encode())

        iv_3des = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(key_3des), modes.CFB(iv_3des), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_pdf_data_3des = encryptor.update(self.pad_pdf(self.encrypted_file_combined)) + encryptor.finalize()
        
        self.encrypted_file_combined =  salt_3des + iv_3des + encrypted_pdf_data_3des
        return self.encrypted_file_combined

    def run(self):
        self.encrypt_pdf_with_aes(self.aes_key_hex)
        self.enced_Data = self.encrypt_pdf_with_3des(self.des3_key_hex)

    def w_file(self):
        with open(self.encrypted_file_combined_name, 'wb') as f:
            f.write(self.encrypted_file_combined)

if __name__ == "__main":
    input_file = 'YOUR_PDF.pdf'  # Provide the path to your PDF file
    pdf_encryptor = PDFEncryptor(input_file)
    pdf_encryptor.run()
    pdf_encryptor.w_file()
    
    aes_key = pdf_encryptor.aes_key_hex
    des3_key = pdf_encryptor.des3_key_hex
