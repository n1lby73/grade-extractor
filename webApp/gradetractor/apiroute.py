from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager
from flask_restful import Resource, reqparse
from flask import jsonify, request, session
from werkzeug.utils import secure_filename
from gradetractor import api, jwt
from gradetractor import app
import openpyxl
import uuid
import os

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class results(Resource):
    @jwt_required()        
    def post(self):

        # Check if the 'file' key exists in the request
        if 'file' not in request.files:

            return {'error': "No file part"}, 400
        
        file = request.files['file']
        
        # Check if the file is of allowed format
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            # rename file
            filename = "result.xlsx"

            uniqueId = str(uuid.uuid4())
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],uniqueId))

            session["path"] = uniqueId

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqueId, filename))

            return {'message': 'File uploaded successfully'}, 200
        
        else:

            return {'error': "Wrong file format"}, 400
        
class templates(Resource):
    @jwt_required()        
    def post(self):

        if not session.get("path"):

            return {'error': 'excel database containing all classes has not been uploaded'}, 404
        
        # Check if the 'file' key exists in the request
        if 'file' not in request.files:

            return {'error': "No file part"}, 400
        
        file = request.files['file']
        
        # Check if the file is of allowed format
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            # rename file
            filename = "template.xlsx"

            path = session.get("path")

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], path, filename))

            return {'message': 'File uploaded successfully'}, 200
        
        else:

            return {'error': "Wrong file format"}, 400

class allClasses(Resource):
    @jwt_required()
    def get(self):

        if not session.get("path"):

            return {'error': 'excel database containing all classes has not been uploaded'}, 404
        
        resultSheet = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), 'result.xlsx')

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

class reg(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)
    
    def post(self):

        args = self.parser.parse_args()
        email = args["email"]
        password = args["password"]

        # users_collection = db.usersfhg
        # users_collection.insert({'email':email, 'password':password})
        # db.users.insert_one({'email':email, 'password':password})

api.add_resource(reg, '/api/v1/reg', '/api/v1/reg/')
api.add_resource(login, '/api/v1/login', '/api/v1/login/')
api.add_resource(results, '/api/v1/result', '/api/v1/result/')
api.add_resource(allClasses, '/api/v1/index', '/api/v1/index/')
api.add_resource(templates, '/api/v1/template', '/api/v1/template/')
api.add_resource(genResult, '/api/v1/genResult', '/api/v1/genResult/')