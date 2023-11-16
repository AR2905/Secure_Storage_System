import os
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(current_script_directory)


class AudioEncryptor:
    def __init__(self, input_file):
        self.input_file = input_file
        ext = self.input_file[self.input_file.find('.'):]
        fName= self.input_file[:self.input_file.find('.')]
        self.encrypted_file_combined = f"Encrypted_{fName}{ext}"
        self.aes_key = secrets.token_bytes(16)
        self.aes_key_hex = self.aes_key.hex()
        self.des3_key = secrets.token_bytes(24)
        self.des3_key_hex = self.des3_key.hex()
        
        # print("AES KEY : "+self.aes_key_hex)
        # print("3DES KEY : "+self.des3_key_hex)

    def pad_aud(self,data):
        padding_length = 16 - (len(data) % 16)
        return data + bytes([padding_length] * padding_length)

    def encrypt_audio_with_aes(self, password):
        with open(self.input_file, 'rb') as file:
            audio_data = file.read()

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
        encrypted_audio_data_aes = encryptor.update(self.pad_aud(audio_data)) + encryptor.finalize()

        with open(self.encrypted_file_combined, 'wb') as file:
            file.write(salt_aes)
            file.write(iv_aes)
            file.write(encrypted_audio_data_aes)

    def encrypt_audio_with_3des(self, password):
        with open(self.encrypted_file_combined, 'rb') as file:
            audio_data = file.read()

        salt_3des = os.urandom(16)
        kdf_3des = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=24,  # 3DES uses a 192-bit key (24 bytes)
            salt=salt_3des,
            iterations=100000,
            backend=default_backend()
        )
        key_3des = kdf_3des.derive(password.encode())

        iv_3des = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(key_3des), modes.CFB(iv_3des), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_audio_data_3des = encryptor.update(self.pad_aud(audio_data)) + encryptor.finalize()

        with open(self.encrypted_file_combined, 'wb') as file:
            file.write(salt_3des)
            file.write(iv_3des)
            file.write(encrypted_audio_data_3des)

    def run(self):
        self.encrypt_audio_with_aes(self.aes_key_hex)
        self.encrypt_audio_with_3des(self.des3_key_hex)

if __name__ == "__main__":
    input_file = 'original.mp3'
    audio_encryptor = AudioEncryptor(input_file)
    audio_encryptor.run()
