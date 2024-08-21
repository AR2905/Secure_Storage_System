from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud import storage as gcs
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class regM:
    def __init__(self):
        try:
            # Define credentials directly as a dictionary
            cred_dict = {
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

            # Initialize Firebase app with credentials directly
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'practice-17d52.appspot.com'
            })

            # Initialize Firestore and Storage clients
            self.db = firestore.client()
            self.bucket = storage.bucket()
            print("Firebase initialized successfully")
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
                    if self.user_id_code:
                        self.create_user_folders(self.user_id_code)
                    return render_template("login.html")
                else:
                    return render_template("username_error.html")
        except Exception as e:
            print(f"Error in add_data_model: {e}")
            return "An error occurred during data processing."

    def create_user_folders(self, user_id):
        folder_names = ['document', 'audio', 'video', 'image']
        try:
            for folder_name in folder_names:
                folder = self.bucket.blob(f'uploads/{user_id}/{folder_name}/')
                folder.upload_from_string('') 
        except Exception as e:
            print(f"Error creating user folders: {e}")

    def get_user_id(self, username):
        try:
            user_ref = self.db.collection('users').where('username', '==', username).get()
            for user_doc in user_ref:
                return user_doc.id  # Return user_id if user is found
            return None  # User not found
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None
