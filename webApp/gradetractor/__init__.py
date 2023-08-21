from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

from gradetractor import config

mongo = PyMongo(app)

from gradetractor import apiroutes