import os
import MySQLdb
import smtplib
import random
import string
from datetime import datetime
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash, send_file
from database import db_connect,inc_reg,ins_loginact,viewadata,getmail,vm1,vc1
from database import db_connect,owner_reg,owner_reg1
# from cloud import uploadFile,downloadFile,close
import os
import cv2
import numpy as np
from sklearn import svm
from sendmail import sendmail
import joblib
loaded_model = joblib.load('model.joblib')
# def db_connect():
#     _conn = MySQLdb.connect(host="localhost", user="root",
#                             passwd="root", db="assigndb")
#     c = _conn.cursor()

#     return c, _conn


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")
    
@app.route("/upload.html")
def admin():
    return render_template("upload.html")



@app.route("/uhome.html")
def uhome():
    return render_template("uhome.html")

@app.route("/vm.html")
def vm():
    uid = session['uid']
    data = vm1(uid)
    print(data)
    return render_template("vm.html",data = data)


@app.route("/vc.html")
def vc():
    uid = session['uid']
    data = vc1(uid)
    print(data)
    return render_template("vc.html",data = data)


@app.route("/pubg.html")
def pubg():
    return render_template("pubg.html")





@app.route("/auth.html")
def ins():
    return render_template("auth.html")


@app.route("/increg.html")
def increg():
    return render_template("increg.html")








@app.route("/index.html")
def index():
    return render_template("index.html") 







@app.route("/inceregact", methods = ['GET','POST'])
def inceregact():
   if request.method == 'POST':    
      
      status = inc_reg(request.form['oname'],request.form['uid'],request.form['password'],request.form['email'],request.form['mobile'])
      
      if status == 1:
       return render_template("auth.html",m1="sucess")
      else:
       return render_template("increg.html",m1="failed")



@app.route("/oregact", methods = ['GET','POST'])
def oregact():
   if request.method == 'POST': 
      
      uid = session['uid']


      
      status = owner_reg(request.form['cname'],request.form['city'],request.form['landmarks'],request.form['remarks'],request.form['mobile'],request.form['image'],uid)
      
      if status == 1:
       return render_template("upload.html",m1="sucess")
      else:
       return render_template("upload.html",m1="failed")
      
def load_images_from_folder(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Read image in grayscale
        if img is not None:
            img = cv2.resize(img, (64, 64))  # Resize image to a fixed size
            images.append(img.flatten())  # Flatten image into a 1D array
            labels.append(folder.split('/')[-1])  # Assign label based on folder name
    return images, labels     

def load_data_from_folders(folder_paths):
    images = []
    labels = []
    for folder_path in folder_paths:
        folder_images, folder_labels = load_images_from_folder(folder_path)
        images.extend(folder_images)
        labels.extend(folder_labels)
    return images, labels


@app.route("/oregact2", methods = ['GET','POST'])
def oregact2():
   if request.method == 'POST':  
      cname =  request.form['cname']
      city =   request.form['city']
      landmarks = request.form['landmarks']
      remarks = request.form['remarks']
      mobile = request.form['mobile']
      image = request.form['image']
      images = []
      data = viewadata()
     
      aimage = data[0][0]  
      print(aimage)
      uid = data[0][1]
      print(uid)
      img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)  # Read image in grayscale
      if img is not None:
        img = cv2.resize(img, (64, 64))  # Resize image to a fixed size
        faltimg= img.flatten()  # Flatten image into a 1D array
        y_pred = loaded_model.predict([faltimg])
        print ("dddddddddddddddddddddddddddddddddddddddddddddddddddd")
        print(y_pred[0] )
       
      if y_pred[0]  == cname:
      
        owner_reg1(cname,city,landmarks,remarks,mobile,image,uid)

        data1 = getmail(uid)
        email = data1[0][0]
        skey = cname + "Details Match Found"
        sendmail(skey,email)
        return render_template("pubg.html",m1="sucess")
      else:
       return render_template("pubg.html",m1="failed")





      
# #-------------------------------ADD_END---------------------------------------------------------------------------
# # -------------------------------Loginact-----------------------------------------------------------------








@app.route("/inslogin", methods=['GET', 'POST'])       
def inslogin():
    if request.method == 'POST':
        status = ins_loginact(request.form['uid'], request.form['password'])
        print(status)
        if status == 1:
            session['uid'] = request.form['uid']
            return render_template("uhome.html", m1="sucess")
        else:
            return render_template("auth.html", m1="Login Failed")
        



# # -------------------------------Loginact End-----------------------------------------------------------------


   
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
