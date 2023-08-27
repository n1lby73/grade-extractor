from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager
from flask_restful import Resource, reqparse
from flask import jsonify, request, session
from werkzeug.utils import secure_filename
from gradetractor import api, jwt
import openpyxl
import os
from gradetractor import app
# resultSheet = "emyety.xlsx"

# Custom validation function to check the file extension
def allowed_file(filename):

    ALLOWED_EXTENSIONS = set(['.xlsx'])
    
    if "." in filename:
        
        # Perform string formatting to retrieve only extension

        startIndex = filename.find(".")
        endIndex = filename.find("'", startIndex)
      
        extension = filename[startIndex:endIndex]

        if extension in ALLOWED_EXTENSIONS:
            
            # string formatting to extract file name 

            nameIndexStart = filename.find("'")
            nameIndexEnd = filename.find(".", nameIndexStart+1) # +1 to omit " ' "

            name = filename[nameIndexStart+1:nameIndexEnd]+extension
            # print (name)
            return name

class results(Resource):
    # @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file',  required=True,  location='files',  dest='files')
        # self.parser.add_argument("resultdb", required=True)

    def post(self):
        
        args = self.parser.parse_args()
        uploaded_result = args['files']

        checkFileFormat = allowed_file(uploaded_result)
        # print (checkFileFormat)
        if checkFileFormat:
            
            uploaded_result.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(uploaded_result.filename)))
            # session['excelResultDb'] = checkFileFormat  # Store the files in the session
            
            return {'message': 'uploaded successfully'}, 200
        
        return {'error': "wrong filetype"}, 406

class allClasses(Resource):
    @jwt_required()
    def get(self):

        resultSheet = session.get('excelResultDb')
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
api.add_resource(genResult, '/api/v1/genResult', '/api/v1/genResult/')