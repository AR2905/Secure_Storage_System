import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Get the directory of the current script file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the location of the script
os.chdir(current_directory)

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

def decrypt_image_with_aes(input_file, output_file, password):
    with open(input_file, 'rb') as file:
        salt_aes = file.read(16)
        iv_aes = file.read(16)
        encrypted_image_data_aes = file.read()

    kdf_aes = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 uses a 256-bit key (32 bytes)
        salt=salt_aes,
        iterations=100000,
        backend=default_backend()
    )
    key_aes = kdf_aes.derive(password.encode())

    cipher = Cipher(algorithms.AES(key_aes), modes.CFB(iv_aes), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_image_data_aes = decryptor.update(encrypted_image_data_aes) + decryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(decrypted_image_data_aes)

def decrypt_image_with_3des(input_file, output_file, password):
    with open(input_file, 'rb') as file:
        salt_3des = file.read(16)
        iv_3des = file.read(8)
        encrypted_image_data_3des = file.read()

    kdf_3des = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=24,  # 3DES uses a 192-bit key (24 bytes)
        salt=salt_3des,
        iterations=100000,
        backend=default_backend()
    )
    key_3des = kdf_3des.derive(password.encode())

    cipher = Cipher(algorithms.TripleDES(key_3des), modes.CFB(iv_3des), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_image_data_3des = decryptor.update(encrypted_image_data_3des) + decryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(decrypted_image_data_3des)

if __name__ == "__main__":
    input_file_combined = "enc_combined_image.jpg"
    
    decrypted_file_3des = "dec_combined_3des_image.jpg"
    
    # Prompt for 3DES key
    password_3des = input("Enter your 3DES Key: ")

    # Decrypt with 3DES first
    decrypt_image_with_3des(input_file_combined, decrypted_file_3des, password_3des)

    # Prompt for AES key
    password_aes = input("Enter your AES Key: ")

    # Decrypt the 3DES-decrypted image file with AES
    input_file_aes = decrypted_file_3des
    decrypted_file_final = "dec_combined_final_image.jpg"
    decrypt_image_with_aes(input_file_aes, decrypted_file_final, password_aes)

