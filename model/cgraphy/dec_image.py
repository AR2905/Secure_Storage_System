import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class ImageDecryptor:
    def __init__(self, input_file_combined):
        self.input_file_combined = input_file_combined
        self.decrypted_image_file = "decrypted_image.png"  # Update the file extension to match your image format (e.g., .jpg, .png, .bmp)

    def decrypt_image_with_3des(self, password_3des):
        salt_3des_length = 16  # Assuming salt is 16 bytes
        iv_3des_length = 8  # Change the IV size if it's different in your setup

        # Split the combined file into salt, IV, and encrypted image data
        self.salt_3des = self.input_file_combined[:salt_3des_length]
        self.iv_3des = self.input_file_combined[salt_3des_length:salt_3des_length + iv_3des_length]
        self.encrypted_image_data_3des = self.input_file_combined[salt_3des_length + iv_3des_length:]

        kdf_3des = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=24,  # 3DES uses a 192-bit key (24 bytes)
            salt=self.salt_3des,
            iterations=100000,
            backend=default_backend()
        )

        key_3des = kdf_3des.derive(password_3des.encode())

        cipher = Cipher(algorithms.TripleDES(key_3des), modes.CFB(self.iv_3des), backend=default_backend())
        decryptor = cipher.decryptor()
        self.decrypted_image_data_3des = decryptor.update(self.encrypted_image_data_3des) + decryptor.finalize()

    def decrypt_image_with_aes(self, password_aes):
        self.salt_aes = self.decrypted_image_data_3des[:16]
        self.iv_aes = self.decrypted_image_data_3des[16:16 + 16]
        self.encrypted_image_data_aes = self.decrypted_image_data_3des[16 + 16:]

        kdf_aes = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 uses a 256-bit key (32 bytes)
            salt=self.salt_aes,
            iterations=100000,
            backend=default_backend()
        )

        key_aes = kdf_aes.derive(password_aes.encode())

        cipher = Cipher(algorithms.AES(key_aes), modes.CFB(self.iv_aes), backend=default_backend())
        decryptor = cipher.decryptor()
        self.decrypted_image_data_aes = decryptor.update(self.encrypted_image_data_aes) + decryptor.finalize()

    def run(self, password_3des, password_aes):
        self.decrypt_image_with_3des(password_3des)
        self.decrypt_image_with_aes(password_aes)

    def save_decrypted_image(self):
        with open(self.decrypted_image_file, 'wb') as file:
            file.write(self.decrypted_image_data_aes)

if __name__ == "__main__":
    input_file_combined = "your_encrypted_image.png"  # Provide the path to your encrypted image file
    image_decryptor = ImageDecryptor(input_file_combined)

    password_3des = input("Enter your 3DES Key: ")
    password_aes = input("Enter your AES Key: ")

    image_decryptor.run(password_3des, password_aes)
    image_decryptor.save_decrypted_image()
