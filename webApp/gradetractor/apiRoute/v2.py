# Interfacing directly with Google spreadsheet

from flask_jwt_extended import jwt_required,create_access_token, create_refresh_token, set_access_cookies, decode_token, get_jwt_identity#,  jwt_manager
# from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify#, request, session,send_file, after_this_request
from flask_restful import Resource, reqparse
# import openpyxl, shutil, uuid, os, requests
# from werkzeug.utils import secure_filename
from gradetractor import api, jwt#, db, app
# import pandas as pd

from dotenv import load_dotenv
import gspread
import os, json
from gspread.exceptions import SpreadsheetNotFound, APIError
load_dotenv()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

accountCredentials = gspread.service_account(filename=os.getenv("googleCred"))

moduleSpreadSheet = "" #varaible to hold the spreadsheet of the module to work with - EMY, ETY, MOD, MECH

availableModules = ["emy", "ety", "mod", "mech"]

# def allowed_file(filename):

#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def validateNumberOfFiles(path): #function to be used as a wrapper to confirm if both template and db excel fiile has been uploaded

#     path = os.path.join(app.config['UPLOAD_FOLDER'], session.get('resultDbPath')) #root path for expcted uploaded document

#     totalFiles = [files for files in os.listdir(path) if os.path.isfile(os.path.join(path,files))] #list all the files in the directory

#     expectedFiles= ["result.xlsx", "template.xlsx"]

#     missingFile = [file for file in expectedFiles if file not in totalFiles] #iterate through to check if files to be worked with are present

#     if "template.xlsx" in missingFile:

#         return {"error": "Result template not uploaded. Please upload the template file before proceeding."}, 404
        
#     if "result.xlsx" in missingFile:

#         return {"error": "Results database not uploaded. Please upload the results file before proceeding."}, 404

#     return True

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return ({"message": "expired token"}), 401

@jwt.invalid_token_loader
def handle_invalid(error):
    return ({"message": "invalid token", "error":error}), 401

class allClassesV2(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("studentModule", required=True)

    def post(self):
        
        args = self.parser.parse_args()
        studentModule = args["studentModule"].lower()

        global moduleSpreadSheet

        if studentModule not in availableModules:

            return jsonify({

                "error": "unknown module received", 
                "available modules": availableModules

            }), 404
        
        
        match studentModule:

            case "emy":

                moduleSpreadSheet = os.getenv("emyResultSheet")
            
            case "ety":

                moduleSpreadSheet = os.getenv("etyResultSheet")

        try:
                    
            classes = list(map(lambda classesName: classesName.title, accountCredentials.open_by_key(moduleSpreadSheet).worksheets()))
            
            return {

                "availableClasses":classes,

            },200

        except Exception as e:

            return {
                
                "error": str(e)
            
            }, 500

class genResultV2(Resource):
    @jwt_required()
    def post(self):

        embeddedIdentity = json.loads(get_jwt_identity()) #unserialize the data back into string same way it was serialize into json data on the login endpoint

        classCode = embeddedIdentity["classCode"]
        studentID = embeddedIdentity["studentID"]
        moduleSpreadSheet = embeddedIdentity["moduleSpreadSheet"]

        worksheet = accountCredentials.open_by_key(moduleSpreadSheet).worksheet(classCode)
        userID = worksheet.find(studentID)
        studentData = worksheet.row_values(userID.row)
        print (embeddedIdentity, moduleSpreadSheet)
        # for i in id:
        #     print (i)
        # args = self.parser.parse_args()
        # className = args["className"]
        # spreadSheetaccess_token = args["spreadsheet"]

        # if not session.get("resultDbPath"):

        #     return {"error": "Results database not uploaded. Please upload the results file before proceeding."}, 400

class loginV2(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("classCode", required=True)
        self.parser.add_argument("studentID", required=True)
        self.parser.add_argument("password", required=True)
    
    def post(self):

        args = self.parser.parse_args()
        classCode = args["classCode"]
        studentID = args["studentID"]
        password = args["password"]

        global moduleSpreadSheet

        if not moduleSpreadSheet:

            return ({

                "error":"select module by retrieving all classes"

            }), 400

        worksheet = accountCredentials.open_by_key(moduleSpreadSheet).worksheet(classCode)
       
        try:
            userID = worksheet.find(studentID)
            
            if userID and userID.row:

                userPassword = worksheet.row_values(userID.row)

                if password in userPassword:

                    # Embedding class code and student id into the token so as to identify which student is currently in session and extract their data from jwt protected endpoints
                    identityData = {

                        "classCode":classCode,
                        "studentID":studentID,
                        "moduleSpreadSheet": moduleSpreadSheet
                    
                    }

                    embeddedIdentity = json.dumps(identityData)


                    refresh_token = create_refresh_token(identity=embeddedIdentity)
                    access_token = create_access_token(identity=embeddedIdentity, fresh=True, additional_claims={"refresh_jti": decode_token(refresh_token)["jti"]})

                    response = jsonify(

                        {
                            "success": "login successful",
                            "token":{
                                "access_token":access_token, "refresh_token":refresh_token
                            }
                        }
                    )

                    set_access_cookies(response, access_token)
                    
                    return response

            return ({
                
                "error":"Student ID or Password is incorrect"

            }), 404

        except Exception as e:
            
            return ({
                
                "error": str(e)
            
            }), 500

# api.add_resource(reg, '/api/v1/reg', '/api/v1/reg/')
api.add_resource(loginV2, '/api/v2/login', '/api/v2/login/')
# api.add_resource(results, '/api/v1/result', '/api/v1/result/')
api.add_resource(allClassesV2, '/api/v2/extractClasses', '/api/v2/extractClasses/')
# api.add_resource(templates, '/api/v1/template', '/api/v1/template/')
api.add_resource(genResultV2, '/api/v2/genResult', '/api/v2/genResult/')