from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.app_context().push()

from gradetractor import config

api = Api(app)
mongo = PyMongo(app)
db = mongo.db
jwt = JWTManager(app)
CORS(app, cors_allowed_origin=['http://127.0.0.1:5000/api/v1/result'])

users_collection = db.users

from gradetractor.apiRoute import v1, v2