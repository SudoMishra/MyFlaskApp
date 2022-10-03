from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from tensorflow import keras

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import requests
import base64
import json

main = Blueprint('main', __name__)

# from tasks import tasks.cel_get_predictions, tasks.cel_load_image, tasks.cel_load_model
import tasks

url = 'http://localhost:8501/v1/models/mnist:predict'

def make_prediction(instances):
   data = json.dumps({"signature_name": "serving_default", "instances": instances.tolist()})
   headers = {"content-type": "application/json"}
   json_response = requests.post(url, data=data, headers=headers)
   print("In make predictions")
   predictions = json.loads(json_response.text)['predictions']
   return predictions


def load_model():
    model = keras.models.load_model('./static/models/mnist_model_1.hdf5')
    # print(model.summary())
    return model

def load_image(fname):
    print(fname)
    i = cv2.imread(fname)
    print(i.shape)
    # plt.imshow(i)
    # print(i.shape)
    i = np.array(cv2.cvtColor(i,cv2.COLOR_BGR2GRAY))
    i = cv2.resize(i,(28,28))
    i = i.reshape((1,28,28,1))
    i = i/255.0
    
    return i

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict')
@login_required
def predict(name="Hello",img="a.png"):
    # TODO Allow image Upload and in html and then run mnist model and return the output
    # model = load_model()
    # print(os.getcwd())
    # print("Model Loaded")
    # print(name,img)
    # img_path = os.path.join(current_app.config["UPLOAD_FOLDER"],img)
    return render_template('predict.html', name=current_user.name)

@main.route('/predict/<user_name>/<fname>', methods=['GET'])
@login_required
def show_img(user_name="Bob",fname="a.png"):
    # model = load_model()
    # print(os.getcwd())
    print("Model Loaded in SHow")
    # print(user_name,fname)
    # img_path = os.path.join('uploads',fname)
    # img = load_image(os.path.join('.','static',img_path))
    print(f"file : {fname}")
    img,img_path = tasks.cel_load_image.delay(fname=fname)#.get()
    json_load = json.loads(img)
    img = np.asarray(json_load["img"])
    # preds = model.predict(img)
    # preds = np.argmax(preds,axis=1)
    # print(preds)
    # print(img_path)
    return render_template('predict.html', name=current_user.name, user_image=img_path,pred=True)

@main.route('/predict/<user_name>/<fname>', methods=['POST'])
@login_required
def pred_img(user_name="Bob",fname="a.png"):
    if request.form.get('reupload') == 'yes':
        return redirect(url_for('main.predict'))
    # model = load_model()
    # model = load_model()
    # print(os.getcwd())
    print("Model Loaded in Pred Img")
    # print(user_name,fname)
    # img,img_path = tasks.cel_load_image.delay(fname=fname).get()
    # json_load = json.loads(img)
    # img = np.asarray(json_load["img"])
    img_path = os.path.join('uploads',fname)
    img = load_image(os.path.join('.','static',img_path))
    print("Image Loaded in pred img")
    img = img.reshape(1,28,28,1)
    probs = make_prediction(img)
    print("GOt Predictions")

    # print(type(probs))
    pred,probs = np.argmax(probs[0]), np.max(probs[0])
    # pred,probs = tasks.cel_get_predictions.delay(model=model,img=img).get()

    
    # pred = model.predict(img)
    # pred, probs = np.argmax(pred,axis=1)[0], np.max(pred,axis=1)[0]

    # print(preds)
    # print(img_path)
    return render_template('predict.html', name=current_user.name, user_image=img_path, pred=True, preds=pred, probs=probs)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/predict', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            # print("Heree",filename)
            return redirect(url_for('main.show_img', user_name=current_user.name, fname=filename))
    return render_template('predict.html')

@main.route('/display/<file>')
def display_img(file):
    return redirect(url_for('main.display_img',filename=file))