from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import librosa
import os
from moviepy.editor import *

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import cv2
from deepface import DeepFace

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

emotion_dict0 = {
    0: "happy",
    1: "sad",
    2: "fear",
    3: "disgust",
    4: "neutral",
    5: "angry",
    6: "surprise",
}
# emotion_dict0 = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "sad", 5: "surprise", 6: "neutral"}
emotion_dict1 = {
    "happy": 0,
    "sad": 0,
    "fear": 0,
    "disgust": 0,
    "neutral": 0,
    "angry": 0,
    "surprise": 0,
}
# emotion_dict1 = { "angry":0, "disgust":0, "fear":0, "happy":0, "sad":0,  "surprise":0,"neutral":0}
cap = cv2.VideoCapture("12.mp4")
lastemotions = list()
# current_emotion_count=3
emotions = [0, 0, 0, 0, 0, 0, 0]


def extract_mfcc1(file):
    y, sr = librosa.load(file, duration=3, offset=0.5)
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


# plot the grapg from dictionay
def plot_graph():
    total = sum(dic.values())
    plt.bar(dic.keys(), [v / total for v in dic.values()], color="salmon")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    plt.grid(axis="y")
    plt.show()


def return_percentage_listv(li):
    total = sum(li)
    percentageList = [(x / total) * 100 for x in li]
    return percentageList


def audioVideoEmotion(address):
    clip1 = VideoFileClip(address)
    clip1.audio.write_audiofile("Audios//test1.wav")
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        response = DeepFace.analyze(
            frame, actions=("emotion",), enforce_detection=False
        )
        response0 = response[0]
        # print(response0)
        e = response0["emotion"]
        a = list(e.values())
        for j in range(7):
            emotions[j] += a[j]

        temp = 1
        y = False
        while temp < 10:
            temp += 1
            ret, frame = cap.read()
            if ret == False:
                y = True
                break
        if y == True:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()

    percentageList = return_percentage_listv(emotions)
    emotion_dict1["angry"] = percentageList[0]
    emotion_dict1["disgust"] = percentageList[1]
    emotion_dict1["fear"] = percentageList[2]
    emotion_dict1["happy"] = percentageList[3]
    emotion_dict1["sad"] = percentageList[4]
    emotion_dict1["surprise"] = percentageList[5]
    emotion_dict1["neutral"] = percentageList[6]

    # print(sum(emotion_dict1.values()))
    # print(list(emotion_dict1.values()))
    # print(list(emotion_dict1.keys()))
    # print(input_main('Audios//test1.wav'))
    print(return_emoion_list())
    return (
        list(emotion_dict1.keys()),
        list(emotion_dict1.values()),
        input_main("Audios//test1.wav"),
        return_emoion_list(),
    )


print(audioVideoEmotion("12.mp4"))
