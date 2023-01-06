from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

####Connecting to the database

try:
    mongo = pymongo.MongoClient(
        host="localhost", port=27017, serverSelectionTimeoutMS=1000
    )
    db = mongo.fastHire

    mongo.server_info()
except:
    print("Couldn't connect to database")

############################
@app.route("/users", methods=["GET"])
def get_user():
    try:

        data = list(db.jobs.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json",
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Cannot get user"}),
            status=500,
            mimetype="application/json",
        )


id = 1
################################################################
@app.route("/users", methods=["POST"])
def insert_job():
    try:
        job = {
            "name": request.form["name"],
            "description": request.form["description"],
            "skills": request.form["skills"],
            "requirements": request.form["requirements"],
            "education": request.form["education"],
        }

        # job = {
        #     "name": "Web Developer",
        #     "description": "Web Developer required for our company urgent",
        # }

        dbResponse = db.jobs.insert_one(job)
        print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response=json.dumps(
                {"message": "Job inserted", "id": f"{dbResponse.inserted_id}"}
            ),
            status=200,
            mimetype="application/json",
        )

    except Exception as ex:
        print("********************************")
        print(ex)


################################


if __name__ == "__main__":
    app.run(port=80, debug=True)
