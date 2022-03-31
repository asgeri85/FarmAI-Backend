# Kütüphanelerin import edilmesi

from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import warnings
import optparse as opt
import json
import googletrans
from googletrans import Translator


warnings.filterwarnings('ignore')
def userInput():
    parser=opt.OptionParser()
    parser.add_option("-N",dest="N",help="N.")
    parser.add_option("-P",dest="P",help="N.")
    parser.add_option("-K",dest="K",help="N.")
    parser.add_option("-p",dest="p",help="N.")
    options = parser.parse_args()[0]
    return options
    
options=userInput()
N=int(options.N)
P=int(options.P)
K=int(options.K)
t=22
h=80
p=int(options.p)
r=100
"""
N - ratio of Nitrogen content in soil
P - ratio of Phosphorous content in soil
K - ratio of Potassium content in soil
temperature - temperature in degree Celsius
humidity - relative humidity in %
ph - ph value of the soil
rainfall - rainfall in mm
"""

PATH = 'Mahsul_Analizi/Dataset/crop_recommendation.csv'
df = pd.read_csv(PATH)

df['label'].unique()
#print(df.dtypes)

df['label'].value_counts()

sns.heatmap(df.corr(),annot=True)

features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']
labels = df['label']

# Tüm modelin adını ve karşılık gelen adı eklemek için boş listeler başlatılıyor.
acc = []
model = []

# Train ve test verilerine ayırma

from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB

NaiveBayes = GaussianNB()

NaiveBayes.fit(Xtrain,Ytrain)

predicted_values = NaiveBayes.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Naive Bayes')
#print("Naive Bayes's Accuracy is: ", x)

from sklearn.svm import SVC

SVM = SVC(gamma='auto')

SVM.fit(Xtrain,Ytrain)

predicted_values = SVM.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('SVM')
#print("SVM's Accuracy is: ", x)

from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)

predicted_values = RF.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('RF')

translator = Translator()

#data = np.array([[104,18, 30, 23.603016, 60.3, 6.7, 140.91]])
data = np.array([[N, P, K, t, h, p,r]])
prediction1 = RF.predict(data)
prediction1 = str(prediction1)
prediction1=prediction1.strip("[]'")
prediction1 = translator.translate(prediction1, src='en',dest="tr").text

data = np.array([[N+30, P-40, K+40, t+8, h+20, p+1,r+50]])
prediction2 = RF.predict(data)
prediction2 = str(prediction2)
prediction2=prediction1.strip("[]'")
prediction2 = translator.translate(prediction2,src='en', dest="tr").text

data = np.array([[N-30, P+40, K-40, t-8, h-20, p-1,r-50]])
prediction3 = RF.predict(data)
prediction3 = str(prediction3)
prediction3=prediction3.strip("[]'")
prediction3 = translator.translate(prediction3,src='en', dest="tr").text

data = np.array([[N+50, P-30, K+60, t+15, h+40, p+2,r+80]])
prediction4 = RF.predict(data)
prediction4 = str(prediction4)
prediction4=prediction4.strip("[]'")
prediction4 = translator.translate(prediction4,src='en', dest="tr").text


data = np.array([[N-50, P+30, K-60, t-15, h-40, p-2,r-80]])
prediction5 = RF.predict(data)
prediction5 = str(prediction5)
prediction5=prediction5.strip("[]'")
prediction5 = translator.translate(prediction5,src='en', dest="tr").text


Mahsul = {
    "Mahsul": [prediction1.capitalize() ,prediction2.capitalize(), prediction3.capitalize(),prediction4.capitalize(),prediction5.capitalize()]
    }



with open("Mahsul_Analizi/mahsul.json", "w",encoding='utf8') as outfile:
        json.dump(Mahsul, outfile,ensure_ascii=False)


