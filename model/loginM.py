from flask import render_template

from flask import Flask, render_template, request, redirect, url_for, session,send_file , abort , flash
import firebase_admin
from google.cloud import storage as sss
from firebase_admin import storage
import tempfile
from datetime import timedelta
import hashlib
from firebase_admin import credentials, firestore, storage
import os
import secrets
import mimetypes
import pyrebase
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from model.cgraphy.enc_audio import AudioEncryptor
from model.cgraphy.dec_audio import AudioDecryptor

from model.cgraphy.enc_pdf import PDFEncryptor

from model.cgraphy.enc_word import WordEncryptor
from model.cgraphy.enc_video import VideoEncryptor
from model.cgraphy.enc_image import ImageEncryptor

from model.cgraphy.dec_video import VideoDecryptor
from model.cgraphy.dec_image import ImageDecryptor
from model.cgraphy.dec_pdf import PdfDecryptor
from model.cgraphy.dec_word_SIMPLE import WordFileDecryptor


class loginM:
    
    def __init__(self):
        try:
            self.db = firestore.client()
            self.bucket = storage.bucket()
            # self.client = storage.Client()
            print("OK_log")
        except:
            print("ERROR_log")
            
    @classmethod
    def generate_key(cls):
        return Fernet.generate_key()

    @classmethod
    def encrypt_file(cls, file_bytes, key):
        f = Fernet(key)
        encrypted_bytes = f.encrypt(file_bytes)
        return encrypted_bytes

    @classmethod
    def decrypt_file(cls, encrypted_bytes, key):
        f = Fernet(key)
        decrypted_bytes = f.decrypt(encrypted_bytes)
        return decrypted_bytes
            
    def username_check(self , username):
        try:
            self.uname = username
            # print ("this is the name " +self.uname)
            self.users_ref = self.db.collection('users')
            self.query = self.users_ref.where("username", "==", username)
            results = self.query.stream()
            for result in results:
        # If there's at least one result, the username exists
                return render_template('login2.html', username = username)
            # If no matching documents were found, the username does not exist
            return render_template('no_user.html')

        except:
            return("Something wrong")
        
    def password_check(self , password):
        q = self.users_ref.where('username', '==', self.uname).get()
        for doc in q:
            self.data = doc.to_dict()
            if 'password' in self.data:
                if self.data['password'] == password: 
                    return render_template('login3.html')
                else:
                    return render_template('error.html')
            

    def color_check(self , color1, color2, color3):
        
        try:
        
            cc1 = self.data['color1']
            
            cc2 = self.data['color2']
            
            cc3 = self.data['color3']
            
            if cc1 == color1 and cc2 == color2 and cc3 ==color3:
                self.user_id_code = self.get_user_id(self.uname)
                session['user_id_code'] = self.user_id_code
                print('This is the code : ' + self.user_id_code)
                # session['user_id_code'] = self.user_id_code
                return render_template("dashboard.html")

            else:
                return("Wrong password")
        except:
            return("NOT")
    
        

    def sync_files_with_storage(self, user_id, uploaded_files):
        
        self.storage_client = sss.Client()
        
        self.existing_files = list(self.bucket.list_blobs(prefix=f'uploads/{user_id}/'))
        
        self.synced_files = []
        for filename in uploaded_files:
            if any(filename.decode('utf-8', 'ignore') in blob.name for blob in self.existing_files):

                self.synced_files.append(filename)
        # print(self.synced_files)
        # return self.synced_files
    
    
    from flask import make_response
    
    def get_file_type(self, filename):
        file_extension = filename.rsplit('.', 1)[-1].lower()
        document_extensions = ['pdf', 'docx', 'txt']
        audio_extensions = ['mp3', 'wav', 'ogg']
        video_extensions = ['mp4', 'avi', 'mkv']
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']

        if file_extension in document_extensions:
            return 'document'
        elif file_extension in audio_extensions:
            return 'audio'
        elif file_extension in video_extensions:
            return 'video'
        elif file_extension in image_extensions:
            return 'image'
        else:
            return None  # Unknown file type


    
    def get_user_id(self, username):
        user_ref = self.db.collection('users').where('username', '==', username).get()
        for user_doc in user_ref:
            return user_doc.id  # Return user_id if user is found
        return None  # User not found
    

    def download_file(self, file_type, file_name, ipk1, ipk2):
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file_name)

        file_path = f'uploads/{self.user_id_code}/{file_type}/{file_name}'
        blob = self.bucket.blob(file_path)
        encrypted_file_bytes = blob.download_as_bytes()
        

        # # Retrieve the encryption key
        # key_path = f'keys/{self.user_id_code}/{file_type}/{file_name}.key'
        # key_blob = self.bucket.blob(key_path)
        # encryption_key = key_blob.download_as_text()
        
        if file_type=='audio':
            
            decobj = AudioDecryptor(encrypted_file_bytes)
            # self.ipk1 = input("Enter KEY1-D : ")
            # self.ipk2 = input("Enter KEY2-A : ")
            decobj.run(ipk1 , ipk2)
            
            encrypted_file_bytes = decobj.decrypted_audio_data_aes
        
        if file_type=='video':
            
            decobj = VideoDecryptor(encrypted_file_bytes)
            # self.ipk1 = input("Enter KEY1-D : ")
            # self.ipk2 = input("Enter KEY2-A : ")
            decobj.run(ipk1 , ipk2)
            
            encrypted_file_bytes = decobj.decrypted_video_data_aes
        
        if file_type=='image':
            
            decobj = ImageDecryptor(encrypted_file_bytes)
            # self.ipk1 = input("Enter KEY1-D : ")
            # self.ipk2 = input("Enter KEY2-A : ")
            decobj.run(ipk1 , ipk2)
            
            encrypted_file_bytes = decobj.decrypted_image_data_aes
        
        if file_type=='document':
            
            decobj = PdfDecryptor(encrypted_file_bytes)
            # self.ipk1 = input("Enter KEY1-D : ")
            # self.ipk2 = input("Enter KEY2-A : ")
            decobj.run(ipk1 , ipk2)
            
            encrypted_file_bytes = decobj.decrypted_pdf_data_aes
        
        
        
        

        # decrypted_file_bytes = self.decrypt_file(encrypted_file_bytes, encryption_key)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(encrypted_file_bytes)

        return send_file(temp_file_path, as_attachment=True)

    def upl_logic(self, u_file, f_name, content_type):
        try:
            if f_name == '':
                return "No selected file"

            file_type = self.get_file_type(u_file.filename)

            if file_type is not None:
                
                if file_type == 'audio':
                    obj =  AudioEncryptor(u_file)
                    k1 = obj.aes_key_hex
                    k2 = obj.des3_key_hex                    
                    # print("A : " + k1)
                    # print("D : " + k2)
                    obj.run()
                    file_bytes = obj.enced_Data 
                    # print("DONE---")
                    
                if file_type == 'video':
                    obj =  VideoEncryptor(u_file)
                    k1 = obj.aes_key_hex
                    k2 = obj.des3_key_hex                    
                    # print("A : " + k1)
                    # print("D : " + k2)
                    obj.run()
                    file_bytes = obj.enced_Data 
                    # print("DONE---")
                    
                    
                if file_type == 'image':
                    obj =  ImageEncryptor(u_file)
                    k1 = obj.aes_key_hex
                    k2 = obj.des3_key_hex                    
                    # print("A : " + k1)
                    # print("D : " + k2)
                    obj.run()
                    file_bytes = obj.enced_Data 
                    # print("DONE---")
                    
                    
                if file_type == 'document':
                    obj =  PDFEncryptor(u_file)
                    k1 = obj.aes_key_hex
                    k2 = obj.des3_key_hex                    
                    # print("A : " + k1)
                    # print("D : " + k2)
                    obj.run()
                    file_bytes = obj.enced_Data 
                    # print("DONE---")
                    
                
                    # encrypted_file = obj.encrypted_file_combined
                    # print(encrypted_file)
                    
                    # print(f"The size of the encrypted file is {encrypted_file.filename} bytes.")
                    # file_bytes = encrypted_file
      
                             
                # file_bytes = u_file.read()
                
                # Generate a random encryption key
                # encryption_key = Fernet.generate_key()
                # encrypted_file_bytes = self.encrypt_file(file_bytes, encryption_key)

                storage_path = f'uploads/{self.user_id_code}/{file_type}/{f_name}'
                blob = self.bucket.blob(storage_path)
                blob.upload_from_string(file_bytes, content_type=content_type)
                
                # Store the encryption key in a separate location (e.g., Firestore)
                # key_path = f'keys/{self.user_id_code}/{file_type}/{f_name}.key'
                # key_blob = self.bucket.blob(key_path)
                # key_blob.upload_from_string(encryption_key, content_type='text/plain')
                
             

                return render_template('dashboard.html', keyy1 = k1, keyy2 = k2, file_is = f_name , redirection = 1)
            else:
                return "Unsupported file type"
        except Exception as e:
            return f"Error in upl_logic uploading file: {str(e)}"


    def sync_files_with_storage_img(self, folder_name):
        
        storage_client = sss.Client()
        bucket = storage_client.bucket("practice-17d52.appspot.com")
        
        # Specify the folder name within the user's directory (e.g., 'image')
        # folder_name = 'image'
        
        # List blobs with the specified folder prefix
        existing_files = list(bucket.list_blobs(prefix=f'uploads/{self.user_id_code}/{folder_name}/'))
        
        # Initialize an empty list to store the filenames
        uploaded_files = []
        
        for blob in existing_files:
            # Extract the filename from the blob's name
            filename = os.path.basename(blob.name)
            uploaded_files.append(filename)
            
        uploaded_files = [file for file in uploaded_files if file.strip()]
        # print(uploaded_files)
        return uploaded_files
    
    def download_image(self, file_name, key1, key2):
        return self.download_file('image', file_name, key1, key2)

    def download_doc(self, file_name, key1, key2):
        return self.download_file('document', file_name, key1, key2)

    def download_video(self, file_name, key1, key2):
        return self.download_file('video', file_name, key1, key2)

    def download_audio(self, file_name, key1, key2):
        return self.download_file('audio', file_name , key1, key2)