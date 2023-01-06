from gc import collect
from flask import Blueprint,jsonify,make_response
from flask import request
from app import mongo
import json
main = Blueprint('main',__name__,url_prefix='/')

@main.route('/')
def index():
    return "hello"

@main.route('/questions')
def add():

    dbs=list(mongo.db.questions.find({},{'_id':0,'question':1}))
    return json.dumps(dbs)
