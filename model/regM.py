from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore, storage, initialize_app
from google.cloud import storage as sss
from datetime import timedelta
from firebase_admin import credentials, firestore, storage
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
class regM:
    def __init__(self):
        try:
            # Gather all credentials from environment variables
            cred_info = {
                "type": os.getenv("GOOGLE_TYPE"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL"),
                "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN")
            }

            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                initialize_app(credentials.Certificate(cred_info), {
                    'apiKey': os.getenv("FIREBASE_API_KEY"),
                    'authDomain': os.getenv("FIREBASE_AUTH_DOMAIN"),
                    'projectId': os.getenv("FIREBASE_PROJECT_ID"),
                    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET"),
                    'messagingSenderId': os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
                    'appId': os.getenv("FIREBASE_APP_ID"),
                    'measurementId': os.getenv("FIREBASE_MEASUREMENT_ID")
                })

            self.db = firestore.client()
            self.bucket = storage.bucket()

            print("OK_reg")
        except Exception as e:
            print(f"Error initializing regM: {e}")
        
    def add_data_model(self, data):
        try:
            if request.method == 'POST':
                
                self.username = data['username']
                password = data['password']
                first_name = data['first_name']
                last_name = data['last_name']
                email = data['email']
                color1 = data['color1']
                color2 = data['color2']
                color3 = data['color3']
                reenter_password = request.form['reenter_password']
                
                if reenter_password != password:
                    return render_template('reenter_error.html')
                
                # Check if the username is already taken
                existing_user = self.db.collection('users').where('username', '==', self.username).get()
                if not existing_user:
                    # Create a new user profile in Firestore
                    user_ref = self.db.collection('users').add({
                        'username': self.username, 
                        'password': password,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'color1': color1,
                        'color2': color2,
                        'color3': color3,
                        'files': []  
                        
                        
                        
                    })
                    self.user_id_code = self.get_user_id(self.username)
                    self.create_user_folders(self.user_id_code)
                    # print(f'in reg __________ {self.user_id_code}')
                    
                    return render_template("login.html")
                else:
                    return render_template("username_error.html")
        except:
            return ("bad fun")
    
    def create_user_folders(self, user_id):
        folder_names = ['document', 'audio', 'video', 'image']
        for folder_name in folder_names:
            folder = self.bucket.blob(f'uploads/{user_id}/{folder_name}/')
            folder.upload_from_string('') 
            
    def get_user_id(self, username):
            user_ref = self.db.collection('users').where('username', '==', username).get()
            for user_doc in user_ref:
                return user_doc.id  # Return user_id if user is found
            return None  # User not found