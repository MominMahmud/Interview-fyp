from flask import Flask, Response, request, render_template
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
