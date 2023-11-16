# main.py

import os
from enc_video import VideoEncryptor  # Import the AudioEncryptor class from enc.py

def main():
    input_file = 'THIS.mp3'  # Change this to the file you want to encrypt

    # Create an instance of AudioEncryptor
    video_encryptor = VideoEncryptor(input_file)

    # Run the encryption process
    video_encryptor.run()

    # Get the size of the encrypted file
    encrypted_file = video_encryptor.encrypted_file_combined
    encrypted_file_size = os.path.getsize(encrypted_file)


    # print(f"The size of the encrypted file is {encrypted_file_size} bytes.")

if __name__ == "__main__":
    main()
