# Interfacing directly with Google spreadsheet

from flask_jwt_extended import jwt_required,create_access_token, create_refresh_token, set_access_cookies, decode_token, get_jwt_identity
from flask import jsonify
from flask_restful import Resource, reqparse
from gradetractor import api, jwt

from dotenv import load_dotenv
import gspread
import os, json
from gspread.exceptions import SpreadsheetNotFound, APIError
load_dotenv()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

accountCredentials = gspread.service_account(filename=os.getenv("googleCred"))

moduleSpreadSheet = "" #varaible to hold the spreadsheet of the module to work with - EMY, ETY, MOD, MECH

availableModules = ["emy", "ety", "mod", "mech"]

#copied function, as at this commit no idea on how it fully works
#retrieve the co-ordinates and convert the column number to letter notation utilizing ASCII 

def colNumberToLetter(col_num):
    result = ''
    while col_num > 0:
        col_num -= 1
        remainder = col_num % 26
        result = chr(remainder + ord('A')) + result # ord() converts string A to it ASCII value, chr() converts the calculated value back to the ASCII letter
        col_num //= 26
    return result

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
        moduleSpreadSheet = embeddedIdentity["moduleSpreadSheet"] #note that sheet id can also be retrieved if token falls into wrong hand

        worksheet = accountCredentials.open_by_key(moduleSpreadSheet).worksheet(classCode)
        userID = worksheet.find(studentID)
        studentData = worksheet.row_values(userID.row)

        # Retrieve all available course utilizing Technical Communication as the first on the list and Gradde to be the one signifying the end of the list
    
        locateStartCourse = worksheet.find("Technical Communication")
        locateEndCourse = worksheet.find("GRADE")

        # Convert column value to regular alphabet notation

        startCourseColumn = colNumberToLetter(locateStartCourse.col)
        endCourseColumn = colNumberToLetter(locateEndCourse.col)

        # Retrieve row number and covert to string
        
        startCourseRow = str(locateStartCourse.row)
        endCourseRow = str(locateEndCourse.row)

        print (worksheet.get(startCourseColumn+startCourseRow+":"+endCourseColumn+endCourseRow))
        
        return {

            "studentData":studentData
            # "studentData":worksheet.get_all_records()
            # worksheet.get_all_values()

        }, 200
   
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
       
        try:

            worksheet = accountCredentials.open_by_key(moduleSpreadSheet).worksheet(classCode)

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

            }), 401

        except gspread.exceptions.WorksheetNotFound:

            return ({

                "error" : "Invalid class code"

            }), 404

        except Exception as e:
            
            return ({
                
                "error": str(e)
            
            }), 500

# api.add_resource(reg, '/api/v1/reg', '/api/v1/reg/')
api.add_resource(loginV2, '/api/v2/login', '/api/v2/login/')
api.add_resource(allClassesV2, '/api/v2/extractClasses', '/api/v2/extractClasses/')
api.add_resource(genResultV2, '/api/v2/genResult', '/api/v2/genResult/')