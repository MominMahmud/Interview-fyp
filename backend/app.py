from flask import Flask,request

from extentions import mongo
from main.routes import main
from flask_cors import CORS


def create_app():
    app=Flask(__name__)
    app.config['MONGO_URI']='mongodb+srv://waleed:1234@cluster0.hrkaqrs.mongodb.net/FastHire?retryWrites=true&w=majority'
    mongo.init_app(app)
    app.register_blueprint(main)
    CORS(app, resources={r'/*': {'origins': '*'}})
    return app