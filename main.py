import subprocess as sub
import os
import cv2
import pyrebase
import json
import numpy as np
import time
import subprocess

sub.call(["python -m http.server 7777 > /dev/null 2>&1 &"])
sub.call(["python3 pagekite.py 7777 farmai.pagekite.me > /dev/null 2>&1 &"])

config = {
  "apiKey": "AIzaSyCYo_sLWQPOaQ3gNqkud9fW2XKfSHMztxQ",
  "authDomain": "farmai-bd386.firebaseapp.com",
  "databaseURL": "https://farmai-bd386-default-rtdb.firebaseio.com",
  "projectId": "farmai-bd386",
  "storageBucket": "farmai-bd386.appspot.com",
  "serviceAccount": "farmai-bd386-firebase-adminsdk-ed31n-6843c0cd3b.json"
}

def SoilType():

    list = []
    firebase_storage = pyrebase.initialize_app(config)
    storage = firebase_storage.storage()
    allFiles = storage.list_files()

    for file in allFiles:
        list.append(file.name)
    try:
        storage.child(list[0]).download("Toprak_Analizi/Soil_Photo/1.jpg")


        img= cv2.imread("Toprak_Analizi/Soil_Photo/1.jpg")
        w1 , h1 = 1024, 1024
        w2 , h2 = 256 , 256
        size1 = img.shape
        if size1[0]>=1024 and size1[1]>=1024 :
            up_points = (w1, h1)
            imgResize = cv2.resize(img,up_points,interpolation= cv2.INTER_LINEAR)
            cv2.imwrite("Toprak_Analizi/Soil_Photo/1.jpg", imgResize)
        else:
            up_points = (w2, h2)
            imgResize = cv2.resize(img,up_points,interpolation= cv2.INTER_LINEAR)
            cv2.imwrite("Toprak_Analizi/Soil_Photo/1.jpg", imgResize)

        sub.call(["python3","Toprak_Analizi/run1.py"])
        time.sleep(1)
        os.remove("Toprak_Analizi/Soil_Photo/1.jpg")
        storage.delete(list[0])

    except:
        print("[-]İmage Not Found")




def ProposalCrop():
    from firebase import firebase

    try:
        firebase = firebase.FirebaseApplication('https://farmai-bd386-default-rtdb.firebaseio.com', None)
        result = firebase.get('https://farmai-bd386-default-rtdb.firebaseio.com/values/', '')
        list2 = []
        items = result.items()
        for key , value in items:
            list2.append(key)

        url=('https://farmai-bd386-default-rtdb.firebaseio.com/values/'+list2[0])
        result2 = firebase.get(url, '')
        result3 = result2.items()

        values=[]

        for value in result3:
            values.append(value)

        Nitrogen = values[0][1]
        Phosphorus = values[1][1]
        Ph = values[2][1]
        Potasium = values[3][1]

        sub.call(["python3","Mahsul_Analizi/oneri.py","-N",str(Nitrogen),"-p",str(Ph),"-P",str(Phosphorus),"-K",str(Potasium)])
        firebase.delete("/values/"+list2[0],None)
    except:
        print("[-]Value Not Found")

while True:
    try:
        sub.call(["clear"])
        SoilType()
        ProposalCrop()
        time.sleep(0.2)
    except:
        print("Exit")
        break



