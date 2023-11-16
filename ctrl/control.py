from app import app
from flask import render_template, request
from model.regM import regM

reg_obj = regM()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login1():
    return render_template('login.html')



@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add', methods=["POST", "GET"])
def add():
    result =  reg_obj.add_data_model(request.form)
    return result



    

