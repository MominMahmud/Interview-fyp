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
app = Flask(__name__)
CORS(app, support_credentials=True)




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


if __name__ == "__main__":
    app.run(port=90, debug=True)
