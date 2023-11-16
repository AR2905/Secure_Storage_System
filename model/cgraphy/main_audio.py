# main.py

import os
from enc_audio import AudioEncryptor  # Import the AudioEncryptor class from enc.py

def main():
    input_file = 'THIS.mp3'  # Change this to the file you want to encrypt

    # Create an instance of AudioEncryptor
    audio_encryptor = AudioEncryptor(input_file)

    # Run the encryption process
    audio_encryptor.run()

    # Get the size of the encrypted file
    encrypted_file = audio_encryptor.encrypted_file_combined
    encrypted_file_size = os.path.getsize(encrypted_file)


    # print(f"The size of the encrypted file is {encrypted_file_size} bytes.")

if __name__ == "__main__":
    main()
