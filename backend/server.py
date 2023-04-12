from flask import Flask, Response, request, render_template
import pymongo
from pymongo import MongoClient
import json
import dns
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os


from bson.objectid import ObjectId


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


(
    videoemotionlabels,
    videoemotionpercentages,
    audioemotiopercentages,
    audioemotionlabels,
) = audioVideoEmotion("12.mp4")


app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "i190633@nu.edu.pk"
app.config["MAIL_PASSWORD"] = "Metalmgsv@5"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
# CORS(app)

print(
    "Hello ************************************************************* WORD************************888"
)
try:
    mongo = pymongo.MongoClient(
        "mongodb+srv://admin:1234@fyp.dhi0fxe.mongodb.net/test?authMechanism=DEFAULT"
    )
    db = mongo["fastHire"]
    mongo.server_info()
except:
    print("Couldn't connect to Db")


@app.route("/createjobs", methods=["POST"])
@cross_origin()
def create_job():
    try:
        print("22")
        print(request.json["name"])
        job = {
            "name": request.json["name"],
            "desc": request.json["desc"],
            "skills": request.json["skills"],
            "edu": request.json["edu"],
            "exp": request.json["exp"],
        }
        dbResponse = db.jobs.insert_one(job)
        # print(dbResponse.inserted_id)
        for attr in dir(dbResponse):
            print(attr)
        return Response(
            response=json.dumps(
                {"message": "job inserted", "id": f"{dbResponse.inserted_id}"}
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        print(e)


@app.route("/jobs", methods=["GET"])
def get_jobs():
    try:
        job_Data = list(db.jobs.find())
        for job in job_Data:
            job["_id"] = str(job["_id"])
        return Response(
            response=json.dumps(job_Data),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot read job"}),
            status=500,
            mimetype="application/json",
        )


@app.route("/candidates", methods=["POST"])
def insert_candidate():
    try:
        candidate = {
            "name": request.json["name"],
            "email": request.json["email"],
            "age": request.json["age"],
            "experience": request.json["experience"],
            "status": request.json["status"],
            "ranking": request.json["ranking"],
            "score": request.json["score"],
            "appliedfor": request.json["appliedfor"],
            "res": [],
        }
        candidate["res"].append(request.json["res"])
        dbResponse = db.candidates.insert_one(candidate)
        # print(dbResponse.inserted_id)
        for attr in dir(dbResponse):
            print(attr)
        return Response(
            response=json.dumps(
                {"message": "Candidate inserted", "id": f"{dbResponse.inserted_id}"}
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        print(e)


@app.route("/candidates", methods=["GET"])
def get_candidates():
    try:
        candidate_Data = list(db.candidates.find())
        for candidate in candidate_Data:
            candidate["_id"] = str(candidate["_id"])
        return Response(
            response=json.dumps(candidate_Data),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot read user"}),
            status=500,
            mimetype="application/json",
        )


@app.route("/candidatesRes/<id>", methods=["PATCH"])
def update_res(id):
    try:
        print(request.json["res"])
        dbResponse = db.candidates.update_one(
            {"_id": ObjectId(id)}, {"$push": {"res": request.json["res"]}}
        )

        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message": "Updated user"}),
                status=200,
                mimetype="application/json",
            )
        else:
            return Response(
                response=json.dumps({"message": "Nothing to update"}),
                status=200,
                mimetype="application/json",
            )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot update user"}),
            status=500,
            mimetype="application/json",
        )


@app.route("/candidates/<apliedfor>", methods=["GET"])
def viewspecific_job(apliedfor):
    try:
        candidate_Data = list(db.candidates.find({"appliedfor": apliedfor}))
        for candidate in candidate_Data:
            candidate["_id"] = str(candidate["_id"])
        return Response(
            response=json.dumps(candidate_Data),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot find user appliedfor"}),
            status=500,
            mimetype="application/json",
        )


@app.route("/questions", methods=["POST"])
def insert_questions():
    try:
        question = {
            "text": request.form["text"],
            "category": request.form["category"],
        }
        dbResponse = db.questions.insert_one(question)
        return Response(
            response=json.dumps(
                {"message": "Question inserted", "id": f"{dbResponse.inserted_id}"}
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        print(e)


@app.route("/questions", methods=["GET"])
def get_questions():
    try:
        question_Data = list(db.questions.find())
        for q in question_Data:
            q["_id"] = str(q["_id"])
        return Response(
            response=json.dumps(question_Data),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot read question"}),
            status=500,
            mimetype="application/json",
        )


@app.route("/jobs/<id>", methods=["GET"])
# @cross_origin()
def getID_job(id):
    try:
        jobData = list(db.jobs.find({"_id": ObjectId(id)}))
        for candidate in jobData:
            candidate["_id"] = str(candidate["_id"])

        # for attr in dir(dbResponse):
        #     print(f"***********{attr}***********")
        return Response(
            response=json.dumps(jobData[0]["name"]),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot update user"}),
            status=500,
            mimetype="application/json",
        )


@app.route("/specificjobs", methods=["GET"])
def get_specificjobs():
    try:
        jobArr = []
        job_Data = list(db.jobs.find())

        for job in job_Data:
            jobArr.append(str(job["name"]))
            print(jobArr)
            return Response(
                response=json.dumps(jobArr),
                status=200,
                mimetype="application/json",
            )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({job_Data}),
            status=500,
            mimetype="application/json",
        )


@app.route("/getC/<email>", methods=["GET", "POST"])
# @cross_origin()
def getID_cand(email):
    try:
        canData = list(db.candidates.find({"email": email}, {"_id": 1}))
        print(email)
        str(canData)
        #   print(str(canData))

        msg = Message(
            "FastHire",
            sender="noreply@demo.com",
            recipients=[email],
        )
        msg.body = (
            "Dear Candidate,\n\n\nYour details have been received by us successfuly. Your information is confidential and will not be shared to anyone.\nYour interview will be conducted by using your camera and microphone. When prompted to allow camera or video click Allow. Whenever you are ready to give the interview,\nClick on this link below: \n\nhttp://localhost:3000/interview/"
            + str(canData[0]["_id"])
            + "\n\n\n\nInstructions:\n1- Click on Listen button to hear the question.\n2- Click on Record to record your response.\n3- Click on Save Answer to save your answer and see the text deteced by us.\n4-Click on Next Question to switch to the next question. Click listen button again to listen to the new question.\n5-Click on Submit to submit your answer."
        )
        mail.send(msg)

        return Response(
            response=json.dumps(str(canData[0]["_id"])),
            status=200,
            mimetype="application/json",
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Cannot update user"}),
            status=500,
            mimetype="application/json",
        )


print(videoemotionlabels)


@app.route("/av", methods=["POST"])
def insert_labels():
    print(videoemotionlabels[0])
    try:
        labels = {
            "labelsV": videoemotionlabels,
            "valueV": videoemotionpercentages,
            "labelsA": audioemotionlabels,
            "valuesA": audioemotiopercentages,
        }
        print(labels)
        dbResponse = db.labels.insert_one(labels)
        return Response(
            response=json.dumps(
                {"message": "Label Inserted", "id": f"{dbResponse.inserted_id}"}
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        print(e)


labelsGlobal = []


@app.route("/gav/<id>", methods=["GET"])
def get_labels(id):
    try:
        labelsGlobal = list(db.labels.find({"_id": ObjectId(id)}))
        for q in labelsGlobal:
            q["_id"] = str(q["_id"])
        return Response(
            response=json.dumps(labelsGlobal),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        print(e)


print(labelsGlobal)


if __name__ == "__main__":
    app.run(port=90, debug=True)
