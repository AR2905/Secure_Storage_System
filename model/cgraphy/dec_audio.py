import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(current_script_directory)
class AudioDecryptor:
    def __init__(self, input_file_combined):
        self.input_file_combined = input_file_combined
        
        self.decrypted_file_final = "dec_combined_final_audio.mp3"

    def decrypt_audio_with_3des(self, password_3des):
        salt_3des_length = 16  # Assuming salt is 8 bytes
        iv_3des_length = 8 
        # with open(self.input_file_combined, 'rb') as file:
        #     salt_3des = file.read(16)
        #     iv_3des = file.read(8)
        #     encrypted_audio_data_3des = file.read()
            # Split the combined file into salt, IV, and encrypted audio data
        self.salt_3des = self.input_file_combined[:salt_3des_length]
        self.iv_3des = self.input_file_combined[salt_3des_length:salt_3des_length + iv_3des_length]
        self.encrypted_audio_data_3des = self.input_file_combined[salt_3des_length + iv_3des_length:]


        kdf_3des = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=24,  # 3DES uses a 192-bit key (24 bytes)
            salt=self.salt_3des,
            iterations=100000,
            backend=default_backend()
        )
        
        # print(f" FUN : {self.salt_3des} \n-----\n {self.iv_3des } \n-----\n {self.encrypted_audio_data_3des}")
        
        key_3des = kdf_3des.derive(password_3des.encode())

        cipher = Cipher(algorithms.TripleDES(key_3des), modes.CFB(self.iv_3des), backend=default_backend())
        decryptor = cipher.decryptor()
        self.decrypted_audio_data_3des = decryptor.update(self.encrypted_audio_data_3des) + decryptor.finalize()
        
        
        # print("THIS  IS decrypted_audio_data_3des : " + self.decrypted_audio_data_3des.hex())
        # with open(self.decrypted_file_final, 'wb') as file:
        #     file.write(decrypted_audio_data_3des)

    def decrypt_audio_with_aes(self, password_aes):
        # with open(self.decrypted_file_final, 'rb') as file:
        
        
        self.salt_aes = self.decrypted_audio_data_3des[:16]
        self.iv_aes = self.decrypted_audio_data_3des[16:16 + 16]
        self.encrypted_audio_data_aes = self.decrypted_audio_data_3des[16 + 16:]

        # salt_aes = self.decrypted_audio_data_3des.read(16)
        # iv_aes = self.decrypted_audio_data_3des.read(16)
        # encrypted_audio_data_aes = self.decrypted_audio_data_3des.read()

        kdf_aes = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256 uses a 256-bit key (32 bytes)
            salt=self.salt_aes,
            iterations=100000,
            backend=default_backend()
        )
        # print(f"Last FUN : {self.salt_aes} \n-----\n {self.iv_aes } \n-----\n {self.encrypted_audio_data_aes}")
        key_aes = kdf_aes.derive(password_aes.encode())

        cipher = Cipher(algorithms.AES(key_aes), modes.CFB(self.iv_aes), backend=default_backend())
        decryptor = cipher.decryptor()
        self.decrypted_audio_data_aes = decryptor.update(self.encrypted_audio_data_aes) + decryptor.finalize()
        
        # print(f"THIS IS decrypted_audio_data_aes : {self.decrypted_audio_data_aes.hex()}")

        # with open(self.decrypted_file_final, 'wb') as file:
        #     file.write(decrypted_audio_data_aes)
        return self.decrypted_audio_data_aes

    def run(self, password_3des, password_aes):
        self.decrypt_audio_with_3des(password_3des)
        self.decrypt_audio_with_aes(password_aes)

if __name__ == "__main__":
    input_file_combined = "xxxx.mp3"
    audio_decryptor = AudioDecryptor(input_file_combined)

    password_3des = input("Enter your 3DES Key: ")
    password_aes = input("Enter your AES Key: ")

    audio_decryptor.run(password_3des, password_aes)
