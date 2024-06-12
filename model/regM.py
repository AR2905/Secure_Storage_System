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
                "type": 'service_account',
                "project_id": 'practice-17d52',
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": 'firebase-adminsdk-dz44g@practice-17d52.iam.gserviceaccount.com',
                "client_id": '102784792120044523860'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dz44g%40practice-17d52.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }

            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                initialize_app(credentials.Certificate(cred_info), {
                    'apiKey': os.getenv("FIREBASE_API_KEY"),
                    'authDomain': "practice-17d52.firebaseapp.com",
                    'projectId': "practice-17d52",
                    'storageBucket': "practice-17d52.appspot.com",
                    'messagingSenderId': "880102883623",
                    'appId':"1:880102883623:web:c199c29978eb511816a902",
                    'measurementId': "G-PV1J5SXGKJ"
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
