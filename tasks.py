# from .flask_app import celery_app
from tensorflow import keras
from flask import current_app

import os
import cv2
import numpy as np

from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = make_celery(current_app)


@celery_app.task()
def load_model():
    model = keras.models.load_model('./static/models/mnist_model_1.hdf5')
    return model

@celery_app.task()
def load_image(fname):
    print(fname)
    i = cv2.imread(fname)
    print(i.shape)
    i = np.array(cv2.cvtColor(i,cv2.COLOR_BGR2GRAY))
    i = cv2.resize(i,(28,28))
    i = i.reshape((1,28,28,1))
    i = i/255.0
    img_path = os.path.join('uploads',fname)
    return i,img_path

@celery_app.task()
def get_predictions(model,img):
    # img_path = os.path.join('uploads',fname)
    # img = load_image(os.path.join('.','static',img_path))
    pred = model.predict(img)
    pred, probs = np.argmax(pred,axis=1)[0], np.max(pred,axis=1)[0]
    return pred,probs
