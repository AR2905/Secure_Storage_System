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

import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class loginM:
    def __init__(self):
        try:
            self.db = firestore.client()
            self.bucket = storage.bucket()
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
            if any(results):
                return render_template('login2.html', username=username)
            else:
                return render_template('no_user.html')
      
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            return render_template('error.html', message="Something went wrong.")
    
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
        # Initialize the storage client with credentials from environment variable
        service_account_info = {
            "type": "service_account",
            "project_id": "practice-17d52",
            "private_key_id": "a2ddd2b73712b7893d3d0482d9dce7a3d3823040",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCkOs7jFNkvZlsB\nvJnsERGE84xxEw0mBKJ3n1fCg0gL+Osk10cqC538bC7Q7bo+0nOtJfbELXHW3pYR\n+4uPN/oGU0DkpiIxZ3+a9eo53z0eykc5simb+SXky7UuH5xVGpLXbAs9oT4HqAUL\njh9Xg4OT/qwpCWHwZnhpdvIqZpd/NZX4re57q/9rfU/5c2rXVXXOkp6Ci9FnmjaU\nS3e7xd6X9MppzmN6Q9P/qDSIlf7wzavFmsR9bpY/8C0EbtOneH5AwvVwDPGceAJY\n+tid9I1y1OmotUGzgcAhC/Q6PrTFnfRN9kqEH0ne8Tq0v0E1kO1m6YF4mNKywBYy\nTvEo0wKBAgMBAAECggEACBEgCL0rrOPrD1/UMxykhTWqxDW46ESDT+Gd35iJiuMB\n3XtAmN/D6Lpn2bKvrdz/BxyHOkKQ/32xlk9wxVegNAk8KQin3QOvm8akDnTF4KcN\ndOSCN2t3av1ky4+/ovOG9OA7zh3UBiLAurBTH34x62yJSHIlFpHZLM8Fqd0EgiBL\nhCvIjUOBkH1cak1TqQcEE/R4SiDgjGSxdRnbk7erKua7DK7sHykyJ9DOWnEg73qg\nXqRA+7pQwJly7yAx/FBjzPwOx7jGIfyL7DeLi8HelkIdY2GJ+8N7AgpQ4c6xnonD\n7nYYWgHQz3RcUBJY/OwGarPcMBt25ZsFgEbgJ0NoBQKBgQDh+d5DoLeFDrOjzT3B\nDTsDIoHIZqm1kfaEIKkN7iuUqZaQqPYK1uebIAcHD4aExO/YAbkJpKoj9AMB5QzQ\n/xFg/TsEbOXadcGhjxh13LwvOJo2RPfs+59wQdTgiHQe2YismYdo2mCLk3/GH/fW\nh3QPJIdUWr1GPDLFXLgJkBkcNQKBgQC6DMJ/E9eIb0BSdeSv1T0ThyCC0MV6WOgU\nbQROI4BA+J1pUczFZ5GS1ZKmqvOKzqO0AXqwQnN18QvTiGRgFP2tFczN3kbsbxvb\nqQP92rnv6M/4w0YQQoBaPX88PfJQUfZxbM28n+H6pNizPVdl934aa8slE0rq+dQ0\n/TXRunSenQKBgACsIKgs2z7vG0O6gZuIcYuB18cD3y9mHsin3DjpY4HOu1700b6Y\ngxnoD31K44iTmW8YGjfYIJV4zWV9C/u3NpMGTd2mgUyUGx5i8ZywKnMthO/yZpZy\n7TeFSp/caBQLa6ev0UJTnAPuTWwGflNKFeNRpYFvv65s0W3a58VHg3udAoGAJClK\nvGxc3hXRiLWFZ2+o2VzQQtzVJTyWjzHJPm7EBNzNq6TMiinhL4r3YBGmGHqlct0+\nvXeM/YWGaOz/pXUvAS9ViUYEvvuxjHZDYlna/fhgQ9egjJSAYgnF6y2XJWlo3w7o\nxhrFT3Qu8lef3x/FkNkWuPQRAa7hQhNdHJCDDjkCgYEA2haAhfqoD+Ri8YMVs7fP\nogaFjb0zawRpZiWQk73K0DnJapjdg5lcXG4T3va1bocivioqbIhkYirMdwu6eVgh\nJPvkwm5W9ghmVyRms5G6wg0iuX1nQRDp2t0KF2ZiYN7/EUIe5onCr0a1irWin5ZT\nbeOIghPVXoRkaXJRdaxuheM=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-71old@practice-17d52.iam.gserviceaccount.com",
            "client_id": "107184044495231452010",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-71old%40practice-17d52.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        storage_client = sss.Client.from_service_account_info(service_account_info)
        bucket = storage_client.bucket("practice-17d52.appspot.com")
        
        # Proceed with listing blobs in the specified folder
        existing_files = list(bucket.list_blobs(prefix=f'uploads/{self.user_id_code}/{folder_name}/'))
        
        uploaded_files = []
        for blob in existing_files:
            filename = os.path.basename(blob.name)
            uploaded_files.append(filename)
            
        uploaded_files = [file for file in uploaded_files if file.strip()]
        return uploaded_files
            
    def download_image(self, file_name, key1, key2):
        return self.download_file('image', file_name, key1, key2)

    def download_doc(self, file_name, key1, key2):
        return self.download_file('document', file_name, key1, key2)

    def download_video(self, file_name, key1, key2):
        return self.download_file('video', file_name, key1, key2)

    def download_audio(self, file_name, key1, key2):
        return self.download_file('audio', file_name , key1, key2)
