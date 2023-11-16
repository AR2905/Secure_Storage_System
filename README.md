# Secure_Storage_System

This Git project focuses on developing a robust and secure file storage system with advanced encryption and two-factor authentication. The system ensures the confidentiality and integrity of stored files, supporting a variety of file types including images, videos, audio, and PDF documents.


**Key Features:**

--> Multi-layer Encryption:

Utilizes advanced encryption algorithms such as AES (Advanced Encryption Standard) and 3DES (Triple Data Encryption Standard) to safeguard the stored files.
Implements a multi-layer encryption approach to enhance the security of sensitive data.
File Storage and Key Generation:

Enables users to securely upload files to the storage system.
Generates unique cryptographic keys for each uploaded file, providing users with a secure key for later retrieval.
Secure Download Process:

Implements a secure download mechanism where users are required to enter the correct decryption key.
If the correct key is provided, the system grants access to the unencrypted file; otherwise, it delivers the file in an encrypted form.
Supported File Types:

Accommodates various file formats, including images, videos, audio, and PDF documents, ensuring versatility in file storage.


--> Two-factor Authentication:

Implements a two-layer authentication system:
Layer 1: Users authenticate with a traditional text password.
Layer 2: Introduces an additional layer of security with a color combination code. Users select three colors during the login stage to create a unique authentication code.
User-friendly Interface:

Designs a user-friendly interface for seamless interaction, ensuring that both encryption and authentication processes are intuitive and straightforward.

**Purpose:**
This project aims to provide users with a secure and versatile file storage solution, addressing the need for confidentiality and protection of sensitive information. By combining robust encryption techniques and two-factor authentication, the system ensures a high level of security for stored files.

**Usage:**
Users can clone this Git repository to access the source code and contribute to the development of features, security enhancements, and overall system improvements. The project welcomes collaboration and feedback to continually enhance the security and functionality of the secure file storage system.


## Installation
1. Clone the repository.
2. Make sure you have install python in your system.
3. Activate Virtual Environment to run this project :  Run this command in Terminal --> ".\venv\Scripts\activate"
4. Run --> " flask run "
5. Now Project is activate on your local host "http://127.0.0.1:5000"




   
![Screenshot 2023-11-16 122312](https://github.com/AR2905/Secure_Storage_System/assets/125748114/1b4defd1-812a-44b4-a186-6543843463fa)


![Screenshot 2023-11-16 122654](https://github.com/AR2905/Secure_Storage_System/assets/125748114/464ab612-2546-45d0-af14-b43e9a77b73f)
