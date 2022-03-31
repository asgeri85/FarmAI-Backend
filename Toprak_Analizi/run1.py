import os
import re
import cv2
import time
import shutil
import zipfile
import urllib.request
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join
from random import randrange
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import subprocess
import tensorflow.keras as k
import json

training_data_directory = 'train'
test_data_directory = 'test'
model = k.models.load_model('/home/devil/Desktop/FarmAI-main/Toprak_Analizi/soil.h5')


def make_prediction(image_fp):
    im = cv2.imread(image_fp) # resmi yüklüyoruz
    plt.imshow(im[:,:,[2,1,0]])
    img = image.load_img(image_fp, target_size = (256,256))
    img = image.img_to_array(img)

    image_array = img / 255. # resmi ölçeklendiriyoruz
    img_batch = np.expand_dims(image_array, axis = 0)

    class_ = ["Gravel", "Sand", "Silt"] # çıkış değerlerini belirliyoruz
    predicted_value = class_[model.predict(img_batch).argmax()]
    #true_value = re.search(r'(Gravel)|(Sand)|(Silt)', image_fp)[0]

    return predicted_value


test_image_filepath ='/home/devil/Desktop/FarmAI-main/Toprak_Analizi/Soil_Photo/1.jpg'
conclusion = make_prediction(test_image_filepath)
print(conclusion)
type1 ={
        "ID":"1",
        "type":"Siltli Toprak",
        "ozellık":"Siltli topraklar tanecikli yapıya sahiptir.Diğer toprak türlerine göre uzun bir süre boyunca nem tutabilirler fakat zaman zaman kompakt hale gelebilirler.İyi bir drenaj özelliğine sahiptirler. Siltli toprak özellikle de nemliyken üzerinde çalışması çok kolay bir toprak türüdür. Orta büyüklükteki partiküllerden ödün veren siltli topraklar çok iyi süzülerek nemi hapsederler. ",
        "Mahsul":['Karpuz', 'Ayva', 'Ahududu', 'Ayçiçeği', 'Kiraz']}

type2 ={
        "ID":"2",
        "type":"Kumlu Toprak",
        "ozellık":"Kumlu topraklar, işlemesi en kolay olan toprak türleri arasındadır.Bünyelerindeki suyu hemen tahliye etmeleri, kumlu toprakların özellikle de ilkbahar mevsiminde bol sulama ihtiyacı duymalarına neden olurlar.Organik madde bakımından zenginddir.Kumlu toprağın aynı zamanda bakımı da kolaydır.",
        "Mahsul":['Havuç', 'Ayçiçeği', 'Bakla', 'Kuru fasulye','Şeftali']
        }

type3 ={
        "ID":"3",
        "type":"Çakıllı Toprak",
        "ozellık":"Kayalık toprağı olarak da bilinir.Kumdan daha büyuk kaydan daha küçük tanecikli yapıya sahiptir.Mahsülden çok ağaç yetiştirmeye daha uygundur.. Su tutma kapasitesi ve besin değeri düşüktür",
        "Mahsul":['Ardıç', 'Alıç', 'Armut', 'Ahlat','İncir']
              }

if conclusion == "Silt":
    with open("/home/devil/Desktop/FarmAI-main/Toprak_Analizi/cikti.json", "w",encoding='utf8') as outfile:
        json.dump(type1, outfile,ensure_ascii=False)
elif conclusion == "Sand":
    with open("/home/devil/Desktop/FarmAI-main/Toprak_Analizi/cikti.json", "w",encoding='utf8') as outfile:
        json.dump(type2, outfile,ensure_ascii=False)
elif conclusion == "Gravel":
    with open("/home/devil/Desktop/FarmAI-main/Toprak_Analizi/cikti.json", "w",encoding='utf8') as outfile:
        json.dump(type3, outfile,ensure_ascii=False)

