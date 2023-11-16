from app import app
import requests
from flask import render_template, request
from model.loginM import loginM
from flask import Flask, request, render_template, redirect, url_for, flash
import firebase_admin
import mimetypes
from google.cloud import storage
from firebase_admin import credentials
app.config['SECRET_KEY'] = 'your_secret_key_here'
# from model.regM import regM 
log_obj = loginM()


@app.route("/getuname",  methods=["POST"])
def getuname():
            
    username =  request.form.get('username')
    return log_obj.username_check(username)


@app.route("/getpassword", methods=["POST"])
def getpassword():
    password = request.form.get("password")
    # print(password)
    return log_obj.password_check(password)


@app.route("/getcolor", methods=["POST"])
def getcolor():
    try:
        color1= request.form.get('color1')
        color2= request.form.get('color2')
        color3= request.form.get('color3')
        # print(color1)
        return log_obj.color_check(color1, color2, color3)
    except:
        return "Color error"
    
    
@app.route('/img' , methods = ['get'])
def img():
    return "hello"

@app.route('/upload', methods = ['POST','GET'])
def upload():
    
    uploaded_file = request.files['uploaded-file']  # 'file' is the name of the file input field in your HTML form
    
        # Save the file to a desired location
    if uploaded_file:
        f_name = uploaded_file.filename
        content_type, _ = mimetypes.guess_type(f_name)
      
        return log_obj.upl_logic( uploaded_file , f_name , content_type )
           
            
    else:
        return 'No file selected'
    


@app.route('/imgFolder')
def imgFolder():
    folder_name  = 'image'
    image_files = log_obj.sync_files_with_storage_img(folder_name)
    return render_template('img_folder.html',image_files = image_files)

@app.route('/vidFolder')
def vidFolder():
    folder_name  = 'video'
    video_files = log_obj.sync_files_with_storage_img(folder_name)
    return render_template('vid_folder.html',video_files = video_files)


@app.route('/audFolder')
def audFolder():
    folder_name  = 'audio'
    audio_files = log_obj.sync_files_with_storage_img(folder_name)
    return render_template('aud_folder.html',audio_files = audio_files)


@app.route('/docFolder')
def docFolder():
    
    folder_name  = 'document'
    doc_files = log_obj.sync_files_with_storage_img(folder_name)
    return render_template('doc_folder.html',doc_files = doc_files)


# Define a route for downloading images
@app.route('/downloadIMG/<file_name>', methods=['GET'])
def downloadIMG(file_name):
    key1 = request.args.get('key1')
    key2 = request.args.get('key2')
    # print('you wanna download : ' + file_name)
    # print('Key 1:', key1)
    # print('Key 2:', key2)
    return log_obj.download_image(file_name, key1, key2)



@app.route('/downloadVID/<file_name>', methods=['GET'])
def downloadVID(file_name):
    key1 = request.args.get('key1')
    key2 = request.args.get('key2')
    # print('you wanna download : ' + file_name)
    # print('Key 1:', key1)
    # print('Key 2:', key2)
    return log_obj.download_video(file_name, key1, key2)


@app.route('/downloadAUD/<file_name>', methods=['GET'])
def downloadAUD(file_name):
    key1 = request.args.get('key1')
    key2 = request.args.get('key2')

    # print('You want to download:', file_name)
    # print('Key 1:', key1)
    # print('Key 2:', key2)

    # Pass key1 and key2 to your log_obj or use them as needed

    return log_obj.download_audio(file_name, key1 , key2)




@app.route('/downloadDOC/<file_name>', methods=['GET'])
def downloadDOC(file_name):
    
    key1 = request.args.get('key1')
    key2 = request.args.get('key2')

    # print('you wanna download : ' + file_name)
    # print('Key 1:', key1)
    # print('Key 2:', key2)
    return log_obj.download_doc(file_name, key1, key2)