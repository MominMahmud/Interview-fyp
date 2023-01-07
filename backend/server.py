# from flask import Flask, Response, request
# import pymongo
# import json
# from bson.objectid import ObjectId

# app = Flask(__name__)

# ####Connecting to the database

# try:
#     mongo = pymongo.MongoClient(
#         host="localhost", port=27017, serverSelectionTimeoutMS=1000
#     )
#     db = mongo.fastHiree

#     mongo.server_info()
# except:
#     print("Couldn't connect to database")

# ############################
# @app.route("/jobsS", methods=["GET"])
# def get_user():
#     try:

#         data = list(db.jobs.find())
#         for user in data:
#             user["_id"] = str(user["_id"])
#         return Response(
#             response=json.dumps(data),
#             status=500,
#             mimetype="application/json",
#         )

#     except Exception as ex:
#         print(ex)
#         return Response(
#             response=json.dumps({"message": "Cannot get user"}),
#             status=500,
#             mimetype="application/json",
#         )


# id = 1
# ################################################################
# @app.route("/jobs", methods=["POST"])
# def insert_job():
#     try:
#         job = {
#             "name": request.form["name"],
#             "description": request.form["description"],
#             "skills": request.form["skills"],
#         }

#         return "hell"

#         # job = {
#         #     "name": "Web Developer",
#         #     "description": "Web Developer required for our company urgent",
#         # }

#         dbResponse = db.jobs.insert_one(job)
#         print(dbResponse.inserted_id)
#         # for attr in dir(dbResponse):
#         #     print(attr)
#         return Response(
#             response=json.dumps(
#                 {"message": "Job inserted", "id": f"{dbResponse.inserted_id}"}
#             ),
#             status=200,
#             mimetype="application/json",
#         )

#     except Exception as ex:
#         print("********************************")
#         print(ex)


from flask import Flask, Response, request
import pymongo
from pymongo import MongoClient
import json
import dns

from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        "mongodb+srv://admin:1234@fyp.dhi0fxe.mongodb.net/test?authMechanism=DEFAULT"
    )
    db = mongo["fastHire"]
    mongo.server_info()
except:
    print("Couldn't connect to Db")


@app.route("/jobs", methods=["POST"])
def create_job():
    try:
        job = {
            "name": request.form["name"],
            "desc": request.form["desc"],
            "skills": request.form["skills"],
            "edu": request.form["edu"],
            "exp": request.form["exp"],
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
        job_Data = list(db.jobs.find({"exp": "5"}))
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


@app.route("/candidates/", methods=["POST"])
def insert_candidate():
    try:
        candidate = {
            "name": request.form["name"],
            "age": request.form["age"],
            "experience": request.form["experience"],
            "status": request.form["status"],
            "ranking": request.form["ranking"],
            "score": request.form["score"],
            "appliedfor": request.form["appliedfor"],
        }
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


@app.route("/jobs/<id>", methods=["PATCH"])
def update_job(id):
    try:
        dbResponse = db.jobs.update_one(
            {"_id": ObjectId(id)}, {"$set": {"name": request.form["name"]}}
        )

        # for attr in dir(dbResponse):
        #     print(f"***********{attr}***********")
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


if __name__ == "__main__":
    app.run(port=90, debug=True)
