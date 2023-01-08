from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import librosa

dic = {
    "happy": 0,
    "sad": 0,
    "fear": 0,
    "disgust": 0,
    "neutral": 0,
    "angry": 0,
    "Surprise": 0,
}
model1 = keras.models.load_model("speechmodel")
hello = list(dic.keys())
hello1 = list()
for i in hello:
    hello1.append([i])
enc = OneHotEncoder()
enc.fit(hello1)


def extract_mfcc1(filename):
    y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return np.expand_dims(np.array(list(mfcc)), -1)


def speech_input(filename):
    dic["happy"] = 0
    dic["sad"] = 0
    dic["neutral"] = 0
    dic["disgust"] = 0
    dic["fear"] = 0
    dic["angry"] = 0
    dic["Surprise"] = 0
    input_mfcc = extract_mfcc1(filename)
    result = model1.predict(input_mfcc)
    result1 = enc.inverse_transform(result)
    # print(result1)
    for i in result1:
        dic[i[0]] += 1
    return dic


def return_percentage_list(dictionary):
    resultList = list(dictionary.values())
    total = sum(resultList)
    percentageList = [(x / total) * 100 for x in resultList]
    return percentageList


# input your file path in this function
# path demo "archive//input//OAF_angry//1001_DFA_ANG_XX.wav"
def input_main(filename):
    dictionary = speech_input(filename)
    percentages = return_percentage_list(dictionary)
    return percentages


# this function returns list of emotions
def return_emoion_list():
    return list(dic.keys())


def plot_graph():
    from matplotlib.ticker import PercentFormatter

    total = sum(dic.values())
    plt.bar(dic.keys(), [v / total for v in dic.values()], color="salmon")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    plt.grid(axis="y")
    plt.show()


l = input_main("12//surprise.wav")
plot_graph()
