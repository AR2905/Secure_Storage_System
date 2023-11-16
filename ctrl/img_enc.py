import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets

# Get the directory of the current script file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the location of the script
os.chdir(current_directory)

def pad(data):
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length] * padding_length)

def encrypt_image_with_aes(input_file, output_file, password):
    with open(input_file, 'rb') as file:
        image_data = file.read()

    salt_aes = os.urandom(16)
    kdf_aes = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 uses a 256-bit key (32 bytes)
        salt=salt_aes,
        iterations=100000,
        backend=default_backend()
    )
    key_aes = kdf_aes.derive(password.encode())

    iv_aes = os.urandom(16)
    cipher = Cipher(algorithms.AES(key_aes), modes.CFB(iv_aes), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_image_data_aes = encryptor.update(pad(image_data)) + encryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(salt_aes)
        file.write(iv_aes)
        file.write(encrypted_image_data_aes)

def encrypt_image_with_3des(input_file, output_file, password):
    with open(input_file, 'rb') as file:
        image_data = file.read()

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
    encrypted_image_data_3des = encryptor.update(pad(image_data)) + encryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(salt_3des)
        file.write(iv_3des)
        file.write(encrypted_image_data_3des)

if __name__ == "__main__":
    input_file = "your_image.jpg"  # Replace with your image file
    encrypted_file_aes = "enc_combined_image.jpg"
    
    # Generate an AES key and print it
    aes_key = secrets.token_bytes(16)
    aes_key_hex = aes_key.hex()
    print(f"AES Key: {aes_key_hex}")

    # Generate a 3DES key and print it
    des3_key = secrets.token_bytes(24)
    des3_key_hex = des3_key.hex()
    print(f"3DES Key: {des3_key_hex}")

    # Encrypt with AES first
    encrypt_image_with_aes(input_file, encrypted_file_aes, aes_key_hex)

    # Encrypt the AES-encrypted image file with 3DES
    input_file_aes = encrypted_file_aes
    encrypted_file_combined = "enc_combined_image.jpg"
    encrypt_image_with_3des(input_file_aes, encrypted_file_combined, des3_key_hex)
