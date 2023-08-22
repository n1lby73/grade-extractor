from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api
from flask import Flask

app = Flask(__name__)

from gradetractor import config

api = Api(app)
mongo = PyMongo(app)
jwt = JWTManager(app)

users_collection = mongo.db.users

from gradetractor import apiroute