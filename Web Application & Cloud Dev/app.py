# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, jsonify, json, redirect, make_response, Response
import key_config as keys
import boto3 
import botocore
import os
import matplotlib.image as mpimg
import numpy as np
import tempfile
import time

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN)


s3 = boto3.resource('s3', aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY, aws_session_token=keys.AWS_SESSION_TOKEN)

KEY = 'aa.png' 
BUCKET_NAME = keys.S3_BUCKET_NAME 

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    return render_template('cp.html')

@app.route("/openexe")
def open_EXE():
  os.system("scan.bat")
  time.sleep(2)
  os.system("extract.bat")

  with open("final.txt", "r") as f:
    content = f.read()

    data = {
        "file": content
    }
    
    return json.dumps(data)
  

@app.route("/mac")
def mac_exe():
  time.sleep(35)
  os.system("macextract.bat")
  
  with open("extractedmacs.txt", "r") as f:
    content = f.read()

    data = {
        "file": content
    }
    
    return json.dumps(data)
  
@app.route("/status")
def status():
  time.sleep(35)
  os.system("status.bat")
  
  with open("status.txt", "r") as f:
    content = f.read()

    data = {
        "file": content
    }
    
    return json.dumps(data)
  
@app.route("/display")
def display():
   
   try:  
        s3.Bucket(keys.S3_BUCKET_NAME).download_file(KEY, 'aa.png')
   except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    return e.response

@app.route('/launchScan')
def st_Scan():
   
   os.system("python3 launch_scan.py")
   time.sleep(55)
   with open("vuln_results.txt", "r") as f:
    content = f.read()

    data = {
        "file": content
    }
    
    return json.dumps(data)
   
   
@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        
        table.put_item(
                Item={
        'name': name,
        'email': email,
        'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('login.html',msg = msg)
    return render_template('index.html')

@app.route('/login')
def login():    
    return render_template('login.html')

@app.route('/exploit')
def exploit():
   
   os.system("python3 launch_exploit.py")
   
   with open("launch_exploit.py", "r") as f:
    content = f.read()

    data = {
        "file": content
    }
    
    return json.dumps(data)   
    
@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            
            return render_template("home.html",name = name)
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template('home.html')