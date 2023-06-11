from flask import Flask, Response, request, render_template
import pymongo
from pymongo import MongoClient
import json
import dns
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from fpdf import FPDF
from bson.objectid import ObjectId
import requests


from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import librosa
from moviepy.editor import *

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import cv2
from deepface import DeepFace
from pydub import AudioSegment
from pydub import silence as si
import speech_recognition as sr
from textblob import TextBlob


dic = {
    "happy": 0,
    "sad": 0,
    "fear": 0,
    "disgust": 0,
    "neutral": 0,
    "angry": 0,
    "Surprise": 0,
}
# model1 = keras.models.load_model("speechmodel")
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
lastemotions = list()
# current_emotion_count=3
emotions = [0, 0, 0, 0, 0, 0, 0]


def extract_mfcc1(file):
    y, sr = librosa.load(file, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=128).T, axis=0)
    return np.expand_dims(np.array(list(mfcc)), -1)


def speech_input(filename):
    dic["happy"] = 0
    dic["sad"] = 0
    dic["neutral"] = 0
    dic["disgust"] = 0
    dic["fear"] = 0
    dic["angry"] = 0
    dic["Surprise"] = 0
    model1 = keras.models.load_model("speechmodel")
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
    for i in range(len(li)):
        li[i]+=1
    total = sum(li)
    percentageList = [(x / total) * 100 for x in li]
    return percentageList


def audioVideoEmotion(address):
    cap = cv2.VideoCapture(address)

    # clip1 = VideoFileClip(address)
    # print(address)
    # clip1.audio.write_audiofile("test1.wav")
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
    ffmpeg_tools.ffmpeg_extract_audio(address, "test.wav")

    print(return_emoion_list())
    return (
        list(emotion_dict1.keys()),
        list(emotion_dict1.values()),
        input_main("test.wav"),
        return_emoion_list(),
    )


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while sound[
        trim_ms : trim_ms + chunk_size
    ].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def audio_text_anlysis(address):
    #sound = AudioSegment.from_file("test.wav", format="wav")
    myaudio= AudioSegment.from_file("test.wav", format="wav")
    #start_trim = detect_leading_silence(sound)
    #end_trim = detect_leading_silence(sound.reverse())

    #duration = len(sound)
    #myaudio = sound[start_trim : duration - end_trim]
    silence = si.detect_silence(myaudio, min_silence_len=1000, silence_thresh=-40)

    silence = [
        ((start / 1000), (stop / 1000)) for start, stop in silence
    ]  # convert to sec

    print(silence)
    gaps = []
    for gap in silence:
        gaps.append(gap[1] - gap[0])
    total_silence_duration = sum(gaps)
    total_speach_duration = myaudio.duration_seconds - total_silence_duration
    if (total_silence_duration<=0):
        speech_to_silence_ratio=0
    else:
        speech_to_silence_ratio = total_speach_duration / total_silence_duration
    
    audio_length_in_minutes = myaudio.duration_seconds / 60
    Avg_silence_dur_per_minute=0
    print("Speech-to-silence ratio:", speech_to_silence_ratio)
    avg_silence_duration = np.mean(gaps)
    print("Average_silence duration:", avg_silence_duration)
    if (total_silence_duration<=0):
        Avg_silence_dur_per_minute=1.1
    else:
        Avg_silence_dur_per_minute = total_silence_duration / audio_length_in_minutes
    print("Average_silence duration per minute :", Avg_silence_dur_per_minute)
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile("test.wav") as source:
        audio_data = recognizer.record(source)
    print(audio_data)
    # Convert speech to text
    try:
        text = recognizer.recognize_google(audio_data)
    except:
        text="hello my name is is waleed mukhtar. I want this job because i like companies work environment."
    # text = dic_show['alternative'][0]['transcript']
    speaker_text = text
    blob = TextBlob(text)
    words = text.split()
    unique_words = set(words)
    num_unique_words = len(unique_words)
    blob = TextBlob(text)

    polarity = blob.sentiment.polarity
    # subjectivity = blob.sentiment.subjectivity
    sentiment = ""
    if polarity > 0:
        sentiment = "Positive"
    elif polarity == 0:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"
    print("Number of unique words:", num_unique_words)
    unique_words_to_total_no_of_words_ratio = num_unique_words / len(words)
    print(
        "unque words to total number of words ratio:",
        unique_words_to_total_no_of_words_ratio,
    )
    rate_of_words_per_minute = len(words) / audio_length_in_minutes
    print("rate of words per minute:", rate_of_words_per_minute)
    return (
        speaker_text,
        silence,
        speech_to_silence_ratio,
        avg_silence_duration,
        Avg_silence_dur_per_minute,
        num_unique_words,
        unique_words_to_total_no_of_words_ratio,
        rate_of_words_per_minute,
        sentiment,
    )


app = Flask(__name__)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "labeeb0316@gmail.com"
app.config["MAIL_PASSWORD"] = "vnipwxczbsxjiphl"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
# CORS(app)
CORS(app, support_credentials=True)

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
            "questions":request.json["questions"]
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

@app.route('/getQuestionsByJobId/<id>',methods=['get'])
def getQuestionsByJobId(id):
    try:
        job = list(db.jobs.find({'_id':ObjectId(id)},{"questions":1,'_id':0}))
        return Response(
            response=json.dumps(job[0]),
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
            
        }
        print(candidate)
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


@app.route("/getQuestions", methods=["GET"])
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

@app.route('/getQuestionsByJob/<id>', methods=['GET'])
def getJobById(id):
    try:
        job = list(db.candidates.find({'_id':ObjectId(id)},{'_id':0,'appliedfor':1}))
        print(job[0])

        questions = list(db.jobs.find({'name':job[0]['appliedfor']},{'questions':1,'_id':0}))
        return Response(
            response=json.dumps(questions[0]),
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

@app.route("/getC/<email>", methods=["GET", "POST"])
# @cross_origin()
def getID_cand(email):
    try:
        canData = list(db.candidates.find({"email": email}))
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
def scoring(speech_to_silence_ratio,avg_silence_duration,Avg_silence_dur_per_minute,num_unique_words,unique_words_to_total_no_of_words_ratio,rate_of_words_per_minute,sentiment,a,b,c,d):
    maxi=max(b)
    ind=b.index(maxi)
    print(a[ind])
    max_v_em=a[ind]

    maxi=max(d)
    ind=d.index(maxi)
    print(c[ind])
    max_a_em=c[ind]
    if (speech_to_silence_ratio>=8):
        speech_to_silence_ratio=1

    else:
        speech_to_silence_ratio=speech_to_silence_ratio/8
    if (avg_silence_duration<=2.5):
        avg_silence_duration=1

    else:
        avg_silence_duration=2.5/avg_silence_duration

    if ( Avg_silence_dur_per_minute<=5):
        Avg_silence_dur_per_minute=1

    else:
        Avg_silence_dur_per_minute=5/Avg_silence_dur_per_minute

    if (unique_words_to_total_no_of_words_ratio>=0.7):
        unique_words_to_total_no_of_words_ratio=1

    elif(unique_words_to_total_no_of_words_ratio>=0.5):
        unique_words_to_total_no_of_words_ratio=unique_words_to_total_no_of_words_ratio*1.25

    elif(unique_words_to_total_no_of_words_ratio>=0.4):
        unique_words_to_total_no_of_words_ratio=unique_words_to_total_no_of_words_ratio*1.1

    if (rate_of_words_per_minute>=150):
        rate_of_words_per_minute=1

    else:
        rate_of_words_per_minute=rate_of_words_per_minute/150

    if (sentiment=='Positive'):
        sentiment=1

    elif(sentiment=='Neutral'):
        sentiment=0.5

    else:
        sentiment=0

    value=(2*rate_of_words_per_minute)+(2*unique_words_to_total_no_of_words_ratio)+(Avg_silence_dur_per_minute)+(speech_to_silence_ratio)+(avg_silence_duration)+(2*sentiment)
    vi_score=0.0
    if(max_v_em=='happy'):
        vi_score=0.9
    elif(max_v_em=='neutral'):
        vi_score=0.7
    elif(max_v_em=='surprise'):
        vi_score=-0.1
    elif(max_v_em=='sad'):
        vi_score=-0.5
    elif(max_v_em=='disgust'):
        vi_score=-0.6
    elif(max_v_em=='angry'):
        vi_score==-0.8
    elif(max_v_em=='fear'):
        vi_score=-0.7
    au_score=0.0
    if(max_a_em=='happy'):
        au_score=0.9
    elif(max_a_em=='neutral'):
        au_score=0.5
    elif(max_a_em=='surprise'):
        au_score=-0.1
    elif(max_a_em=='sad'):
        au_score=-0.5
    elif(max_a_em=='disgust'):
        au_score=-0.6
    elif(max_a_em=='angry'):
        au_score==-0.8
    elif(max_a_em=='fear'):
        au_score=-0.7
    value=au_score+vi_score+value
    print(value)
    score=(value/11)*100
    print(score)
    return score

def pdfcreator(address, st, a, b, c, d, e, f, g, h, via, vib, aua, aub):
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image("logo2.png", 20, 10, 30)
            # font
            self.set_font("helvetica", "B", 20)
            # Padding
            self.cell(80)
            # Title
            self.cell(30, 10, "Report", border=True, ln=1, align="C")
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Set position of the footer
            self.set_y(-15)
            # set font
            self.set_font("helvetica", "I", 8)
            # Pageselfmber
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

        def body(self, st, a, b, c, d, e, f, g, h, via, vib, aua, aub):
            # specself font
            score=scoring(b,c,d,e,f,g,h,via,vib,aub,aua)
            self.set_font("helvetica", "BIU", 20)
            self.cell(0, 10, "Score", ln=1)
            self.set_font("times", "", 12)
            self.cell(0, 10, str(score), ln=1)
            #self.set_font("helvetica", "BIU", 20)
            #self.cell(0, 10, "Text:", ln=1)
            #self.set_font("times", "", 12)
            #self.multi_cell(0, 10, st, ln=1)
            self.set_font("helvetica", "BIU", 20)
            self.cell(0, 2, "High Level features:", ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "silence gaps:", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(a), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Speech to Silence Ratio:", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(b), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Average silence Duration:", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(c), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Average_silence duration per minute :", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(d), ln=1)
            #self.set_font("helvetica", "BIU", 12)
            #self.cell(0, 10, "Number of unique words:", ln=1)
            #self.set_font("times", "", 12)
            #self.multi_cell(0, 10, str(e), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Unique words to total number of words ratio:", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(f), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Rate of words per minute::", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(g), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Sentiment:", ln=1)
            self.set_font("times", "", 12)
            self.multi_cell(0, 10, str(h), ln=1)
            self.set_font("helvetica", "BIU", 20)
            self.cell(0, 10, "High Level Features:", ln=1)
            self.set_font("helvetica", "BIU", 16)
            self.cell(0, 10, "Facial Expression Emotions:", ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Dominant Emotion:", ln=1)
            maxi=max(vib)
            ind=vib.index(maxi)
            print(via[ind])
            max_v_em=via[ind]
            self.set_font("times", "", 12)
            self.cell(0, 10, str(max_v_em), ln=1)
            self.cell(0, 10, "percentage:"+str(maxi), ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "percentages:", ln=1)
            #self.multi_cell(0, 10, str(via), ln=1)
            #self.multi_cell(0, 10, str(vib), ln=1)
            #total = sum(vib)
            #plt.bar(via, [v / total for v in vib], color="salmon")
            #plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
            #plt.grid(axis="y")
            #plt.savefig("plot.png")
            #self.image("plot.png", x=None, y=None, w=0, h=0, type="", link="")
            self.set_font("helvetica", "BIU", 16)
            self.cell(0, 10, "Audio Emotion:", ln=1)
            self.set_font("helvetica", "BIU", 12)
            self.cell(0, 10, "Dominant Emotion:", ln=1)
            maxi=max(aua)
            ind=aua.index(maxi)
            print(aub[ind])
            max_au_em=aub[ind]
            self.set_font("times", "", 12)
            self.cell(0, 10, str(max_au_em), ln=1)
            self.cell(0, 10, "percentage:"+str(maxi), ln=1)
            #self.multi_cell(0, 10, str(aub), ln=1)
            #self.multi_cell(0, 10, str(aua), ln=1)

            #total = sum(aua)
            #plt.bar(aub, [v / total for v in aua], color="salmon")
            #plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
            #plt.grid(axis="y")
            #plt.savefig("plot1.png")
            #self.image("plot1.png", x=None, y=None, w=0, h=0, type="", link="")

    # Create a PDF object
    pdf = PDF("P", "mm", "Letter")

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add Page
    pdf.add_page()
    pdf.body(st, a, b, c, d, e, f, g, h, via, vib, aua, aub)
    pdf.output(address)


# @cross_origin(supports_credentials=True)
# @app.route("/av", methods=["POST"])
# # def insert_labels():
#     v_id = request.json["id"]
#     fpath = v_id + ".mp4"

#     print(fpath)
#     (
#         videoemotionlabels,
#         videoemotionpercentages,
#         audioemotiopercentages,
#         audioemotionlabels,
#     ) = audioVideoEmotion(fpath)
#     (
#         speakText,
#         silence,
#         StoSR,
#         avgSDUR,
#         avgSPM,
#         numUnique,
#         uniqueWords,
#         rateWPM,
#         sentiment,
#     ) = audio_text_anlysis(fpath)
#     pdfcreator(
#         str(v_id) + ".pdf",
#         speakText,
#         silence,
#         StoSR,
#         avgSDUR,
#         avgSPM,
#         numUnique,
#         uniqueWords,
#         rateWPM,
#         sentiment,
#         videoemotionlabels,
#         videoemotionpercentages,
#         audioemotiopercentages,
#         audioemotionlabels,
#     )
#     try:
#         labels = {
#             "_id": v_id,
#             "labelsV": videoemotionlabels,
#             "valueV": videoemotionpercentages,
#             "labelsA": audioemotionlabels,
#             "valuesA": audioemotiopercentages,
#             "labelsV": videoemotionlabels,
#             "valueV": videoemotionpercentages,
#             "labelsA": audioemotionlabels,
#             "valuesA": audioemotiopercentages,
#             "speakerText": speakText,
#             "silence": silence,
#             "StoSR": StoSR,
#             "avgSDUR": avgSDUR,
#             "avgSPM": avgSPM,
#             "numUnique": numUnique,
#             "uniqueWords": uniqueWords,
#             "rateWPM": rateWPM,
#             "sentiment": sentiment,
#         }
#         print(labels)
#         dbResponse = db.labels.insert_one(labels)
#         return Response(
#             response=json.dumps(
#                 {"message": "Label Inserted", "id": f"{dbResponse.inserted_id}"}
#             ),
#             status=200,
#             mimetype="application/json",
#         )
#     except Exception as e:
#         print(e)


labelsGlobal = []



@app.route("/gav/<id>", methods=["GET"])
def get_labels(id):
    try:
        labelsGlobal = list(db.labels.find({"_id": id}))
        for q in labelsGlobal:
            q["_id"] = str(q["_id"])
        return Response(
            response=json.dumps(labelsGlobal),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        print(e)


# print(labelsGlobal)


# @cross_origin(supports_credentials=True)
# @app.route("/av", methods=["POST"])
# def insert_metrics():
#     # v_id = request.json["id"]
#     # fpath = v_id + ".mp4"
#     fpath = "test.wav"
#     # print("RESULT ****************" + audio_text_anlysis(fpath))
#     (
#         speakText,
#         silence,
#         StoSR,
#         avgSDUR,
#         avgSPM,
#         numUnique,
#         uniqueWords,
#         rateWPM,
#         sentiment,
#     ) = audio_text_anlysis(fpath)
#     (
#         videoemotionlabels,
#         videoemotionpercentages,
#         audioemotiopercentages,
#         audioemotionlabels,
#     ) = audioVideoEmotion(fpath)

#     print(
#         "################################################################################################################################################"
#     )

#     print(speakText)
#     print(silence)
#     print(StoSR)
#     print(avgSDUR)

#     try:
#         valuesSaver = {
# "labelsV": videoemotionlabels,
# "valueV": videoemotionpercentages,
# "labelsA": audioemotionlabels,
# "valuesA": audioemotiopercentages,
# "speakerText": speakText,
# "silence": silence,
# "StoSR": StoSR,
# "avgSDUR": avgSDUR,
# "avgSPM": avgSPM,
# "numUnique": numUnique,
# "uniqueWords": uniqueWords,
# "rateWPM": rateWPM,
# "sentiment": sentiment,
#         }

#         dbResponse = db.labels.insert_one(valuesSaver)
#         return Response(
#             response=json.dumps(
#                 {"message": "Label Inserted", "id": f"{dbResponse.inserted_id}"}
#             ),
#             status=200,
#             mimetype="application/json",
#         )
#     except Exception as e:
#         print(e)

@app.route('/setEmotions', methods=['POST'])
def convert_video():
    r = request.files
    print(r)
    file = r.get('file')
    file.save(file.filename+'.webm')
    fpath = file.filename + ".webm"

    print(fpath)
    (
        videoemotionlabels,
        videoemotionpercentages,
        audioemotiopercentages,
        audioemotionlabels,
    ) = audioVideoEmotion(fpath)
    (
        speakText,
        silence,
        StoSR,
        avgSDUR,
        avgSPM,
        numUnique,
        uniqueWords,
        rateWPM,
        sentiment,
    ) = audio_text_anlysis(fpath)
    pdfcreator(
        file.filename + ".pdf",
        speakText,
        silence,
        StoSR,
        avgSDUR,
        avgSPM,
        numUnique,
        uniqueWords,
        rateWPM,
        sentiment,
        videoemotionlabels,
        videoemotionpercentages,
        audioemotiopercentages,
        audioemotionlabels,
    )
    try:
        labels = {
            "_id": file.filename,
            "labelsV": videoemotionlabels,
            "valueV": videoemotionpercentages,
            "labelsA": audioemotionlabels,
            "valuesA": audioemotiopercentages,
            "labelsV": videoemotionlabels,
            "valueV": videoemotionpercentages,
            "labelsA": audioemotionlabels,
            "valuesA": audioemotiopercentages,
            "speakerText": speakText,
            "silence": silence,
            "StoSR": StoSR,
            "avgSDUR": avgSDUR,
            "avgSPM": avgSPM,
            "numUnique": numUnique,
            "uniqueWords": uniqueWords,
            "rateWPM": rateWPM,
            "sentiment": sentiment,
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


    return "Success"

if __name__ == "__main__":
    app.run(port=90, debug=True)
