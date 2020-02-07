from flask import Flask, request
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import pickle
import requests

app = Flask(__name__)
CORS(app)

ROBOT_URL = '192.168.1.197:5010'
model = tf.keras.models.load_model('models/model_esquerda.h5')

@app.route('/get_direction', methods=['POST'])
def get_direction():
    data = request.json
    frame = np.array(data['frame'])
    frame = frame[tf.newaxis,...,tf.newaxis] / 255.0
    direction = np.argmax(model.predict(frame))
    if direction == 0:
        requests.get(ROBOT_URL + '/left_side')
    elif direction == 1:
        requests.get(ROBOT_URL + '/up_side')


if __name__ == "__main__":
 print ("Start")
 app.run(host='0.0.0.0',port=5010)