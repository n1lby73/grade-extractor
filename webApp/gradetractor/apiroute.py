from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager
from flask_restful import Resource, reqparse
from gradetractor import api, jwt, mongo
from flask import jsonify, request 
import openpyxl

resultSheet = "emyety.xlsx"

class allClasses(Resource):
    @jwt_required()
    def get(self):

        resultDb = openpyxl.load_workbook(resultSheet)
        classes = resultDb.sheetnames
        print (classes)

        filteredClasses = []
        unwantedWorkbook = []

        for i in classes:

            if "emy" in i.lower() or "ety" in i.lower():

                filteredClasses.append(i)

        for i in filteredClasses:

            if "Assessment" in i or ">" in i:
                unwantedWorkbook.append(i)

        filteredClasses = [classes for classes in filteredClasses if classes not in unwantedWorkbook]

        return jsonify(allClasses=filteredClasses)


class genResult(Resource):
    @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("className", required=True)

    def post(self):

        args = self.parser.parse_args()
        className = args["className"]
        

class login(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)
    
    def post(self):

        args = self.parser.parse_args()
        email = args["email"]
        password = args["password"]


api.add_resource(login, '/api/v1/login', '/api/v1/login/')
api.add_resource(allClasses, '/api/v1/index', '/api/v1/index/')
api.add_resource(genResult, '/api/v1/genResult', '/api/v1/genResult/')