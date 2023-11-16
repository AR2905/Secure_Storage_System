from flask import render_template

from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from google.cloud import storage as sss
from datetime import timedelta
from firebase_admin import credentials, firestore, storage
import os

class regM:
    def __init__(self):
        try:
            
            self.cred = credentials.Certificate("C:\\Users\\ASHISH\\Downloads\\JSON\\sec.json")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\ASHISH\\Downloads\\JSON\\sec.json"

            firebase_admin.initialize_app(self.cred, {

            'apiKey': "AIzaSyC-Fwvy4a2r7x3MqQ5Q_hugdsuKP6c8VBI",
            'authDomain': "practice-17d52.firebaseapp.com",
            'projectId': "practice-17d52",
            'storageBucket': "practice-17d52.appspot.com",
            'messagingSenderId': "880102883623",
            'appId': "1:880102883623:web:c199c29978eb511816a902",
            'measurementId': "G-PV1J5SXGKJ"
            })

            self.db = firestore.client()
            self.bucket = storage.bucket()

            print("OK_reg")
        
        except:
            print("ERROR_reg")

        
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