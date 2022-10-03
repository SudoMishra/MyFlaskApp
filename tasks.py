# from flask_app import celery_app
from tensorflow import keras
from celery import Celery
import os
import cv2
import numpy as np
import json

celery_app = Celery('tasks', broker='pyamqp://',backend='rpc://')

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@celery_app.task()
def cel_load_model():
    model = keras.models.load_model('./static/models/mnist_model_1.hdf5')
    # json_dump = json.dumps(mo)
    return model

@celery_app.task()
def cel_load_image(fname):
    img_path = os.path.join('.','static','uploads',fname)
    # print(img_path)
    i = cv2.imread(img_path)
    # print(i.shape)
    i = np.array(cv2.cvtColor(i,cv2.COLOR_BGR2GRAY))
    i = cv2.resize(i,(28,28))
    i = i.reshape((1,28,28,1))
    i = i/255.0
    page_img_path = os.path.join('uploads',fname)
    i = json.dumps({"img":i},cls=NumpyEncoder)
    return i,page_img_path

@celery_app.task()
def cel_get_predictions(model,img):
    # img_path = os.path.join('uploads',fname)
    # img = load_image(os.path.join('.','static',img_path))
    pred = model.predict(img)
    pred, probs = np.argmax(pred,axis=1)[0], np.max(pred,axis=1)[0]
    outs = json.dumps({"pred":pred,"probs":probs})
    return outs
