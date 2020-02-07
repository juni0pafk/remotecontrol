import tensorflow as tf
import cv2
import pickle
import numpy as np

img_file = open('data/dados_2020_02_03_18_42_29_424927_328_imagens','rb')
imgs = pickle.load(img_file)
img_file.close()

model = tf.keras.models.load_model('models/model_esquerda.h5')
model.summary()

input_img = cv2.cvtColor(imgs[0][0], cv2.COLOR_BGR2GRAY)
input_img = input_img[tf.newaxis,..., tf.newaxis] / 255.0

print(np.argmax(model.predict(input_img)))

