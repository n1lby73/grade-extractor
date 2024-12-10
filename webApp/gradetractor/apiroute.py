from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token, jwt_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, session,send_file
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from gradetractor import api, jwt, db, app
import pandas as pd
import openpyxl
import shutil
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

            return {'error': "No file path"}, 400
        
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
    # @jwt_required()
    def get(self):

        if not session.get("path"):

            return {'error': 'excel database containing all classes has not been uploaded'}, 404
        
        resultSheet = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), 'result.xlsx')

        resultDb = openpyxl.load_workbook(resultSheet)
        classes = resultDb.sheetnames

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
    # @jwt_required()
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("className", required=True)

    def post(self):

        args = self.parser.parse_args()
        className = args["className"]

        if not session.get("path"):

            return {"error":"excel db and template not uploaded"}, 400
        
        resultSheet = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), 'result.xlsx')

        resultDb = openpyxl.load_workbook(resultSheet)

        parentPath = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), className+" report")
        subPath = os.path.join(parentPath, "individual Result")

        os.makedirs(parentPath, exist_ok=True)
        os.makedirs(subPath, exist_ok=True)

        # Input current number of courses
        # selected class that code is working on

        currentClass = resultDb[className]

        # count number of courses 

        # Specify the row number to start the count

        row_number_to_search = 3
        courseCounted = 0
        startColumn = 0

        # get first column that course count begins

        for cell in currentClass[row_number_to_search]:

            cell_value = cell.value

            if cell_value is not None:

                startColumn = cell.column

                break

        # start count to know how many courses

        for cell in currentClass.iter_cols(min_col=startColumn, min_row=row_number_to_search, max_row=row_number_to_search):

            cell_value = cell[0].value

            if cell_value != "AVERAGE":
            
                courseCounted += 1

            else:

                totalCourse = courseCounted + 1 # including column for average(count start from index zero)
                averageValue = courseCounted

                break
            
        # iteration to assign how many student are available while keeping max at 24

        # max number of student in class

        maxStudent = 24 # that is the maximum number of student in a class
        startRow = 7 # from main db, names majorly starts from column 7
        cellCount = 0
        startColumn = 1
        numberOfStudent = 0

        for cell in currentClass.iter_rows(min_col=startColumn, min_row=startRow):
        
            cell_value = cell[0].value

            if cell_value is not None and cellCount <= maxStudent:
            
                numberOfStudent += 1
                cellCount += 1

            else:
            
                break
            
        #course index for db

        courseRowDb = 5
        courseColumnDb = 6

        #course index for template

        courseRowTemplate = 11
        courseColumnTemplate = 3

        # other variable

        scoreList = []
        currentCourseColumn = 11
        trackFailure = 0
        probation = []
        termination = []
        courseNameDb = []
        courseNameTemplate = []

        #load work sheet        

        resultTemplate = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), 'template.xlsx')
        resultSheet = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), 'result.xlsx')

        template = openpyxl.load_workbook(resultTemplate)
        templateWorksheet = template.worksheets[0]

        data = pd.read_excel(resultSheet, sheet_name=className, skiprows=6, header=None, nrows=numberOfStudent) #skip rows is 6 because after that row student names which is the data we need starts counting

        # extract all course name from db and template

        for i in range(courseCounted):
        
            dbCell = currentClass.cell(row=courseRowDb, column=courseColumnDb).value
            courseNameDb.append(dbCell)

            courseColumnDb += 1

        for i in range(courseCounted):
        
            templateCell = templateWorksheet.cell(row=courseRowTemplate, column=courseColumnTemplate).value
            courseNameTemplate.append(templateCell)

            courseRowTemplate += 1

        # iterate through templateWorksheet and manipulate data

        for _, row in data.iterrows():
        
            lastName = row.iloc[1]
            firstName = row.iloc[2]
            middleName = row.iloc[3]

            # Check if any of the names is NaN, if yes, set them to empty strings

            if pd.isna(firstName):
            
                firstName = ""

            if pd.isna(middleName):
            
                middleName = ""

            # ommited last name(every individual would surely have a last name) to keep track of empty result that would be called nan

            score = row.iloc[5:].values

            score = pd.Series(score).fillna('NA').values

            for scores in score[:totalCourse]:
            
                scoreList.append(scores)

            average = scoreList[averageValue]

            # check for failures

            for scores in scoreList[:averageValue]:
            
                try:
                
                    if int(scores) < 60:
                    
                        trackFailure += 1

                except:
                
                    pass
                
            # Create a dictionary to store the mapping of course names and their corresponding scores
            course_score_mapping = dict(zip(courseNameDb, score[:totalCourse]))

            # Iterate through the course names in the template
            for coursesTemplate in courseNameTemplate:
            
                # Check if the course name exists in the mapping
                if coursesTemplate in course_score_mapping:
                
                    # Get the score from the mapping for the current course name
                    score_for_course = course_score_mapping[coursesTemplate]

                else:
                
                    # If the course name is not found in the mapping, set the score to 'NA'
                    score_for_course = ' '
                # Write the score to the corresponding cell in the template

                templateWorksheet.cell(row=currentCourseColumn, column=4, value=score_for_course)
                currentCourseColumn += 1

            name = str(lastName) + " " + str(firstName) + " " + str(middleName)

            templateWorksheet.cell(row=6, column=3, value=name)
            templateWorksheet.cell(row=6, column=5, value=average)
            templateWorksheet.cell(row=4, column=5, value=className)

            # check number of failed courses

            if trackFailure == 2:
            
                probation.append(name)

            if trackFailure > 2:
            
                termination.append(name)

            # clear variable memory

            trackFailure = 0
            scoreList = []
            currentCourseColumn = 11

            #save file

            try:
            
                template.save('{}/{}.xlsx'.format(subPath,name))

            except:
            
                pass
            
        # loop to delete null report file created cause of incomplete class

        for filename in os.listdir(subPath):

            if "nan" in filename:
            
                file_path = os.path.join(subPath, filename)

                os.remove(file_path)

        # create file to store probation and termination list

        probationFilePath = os.path.join(parentPath, className + " Probation List.txt")
        terminationFilePath = os.path.join(parentPath, className + " Termination List.txt")

        probationFile = open(probationFilePath, "w")
        terminationFile = open(terminationFilePath, "w")

        # generate student on probation

        for watchlist in probation:

            probationFile.write(watchlist + '\n')

        # generate student on termination

        for watchlist in termination:

            terminationFile.write(watchlist + '\n')

        # Save and close files before sending

        probationFile.close()
        terminationFile.close()

        # zip folder containing results

        resultPath = os.path.join(app.config['UPLOAD_FOLDER'], session.get('path'), className + " generated result")
        zippedResultPath = shutil.make_archive(resultPath, 'zip', parentPath)

        return send_file(zippedResultPath, as_attachment=True)

class login(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)
    
    def post(self):

        args = self.parser.parse_args()
        email = args["email"].lower()
        password = args["password"]

        checkUser = db.users.find_one({"email":email})

        if not checkUser or not check_password_hash(checkUser.get("password"), password):

            return ({"Error":"Email or password is incorrect"})
        
class reg(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", required=True)
        self.parser.add_argument("password", required=True)
    
    def post(self):

        args = self.parser.parse_args()
        email = args["email"].lower()
        password = args["password"]

        checkExistingMail = db.users.find_one({"email":email})

        if checkExistingMail:

            return ({"Error":"Mail already exist"})
        
        hashedPass = generate_password_hash(password)

        data = {'email':email, 'password':hashedPass}
        result = db.users.insert_one(data)

        if result.inserted_id:
            
            return ({"message":"Data inserted successfully", "inserted_id":str(result.inserted_id)}), 201
        
        else:

            return jsonify('error', 'Failed to insert data'), 500

api.add_resource(reg, '/api/v1/reg', '/api/v1/reg/')
api.add_resource(login, '/api/v1/login', '/api/v1/login/')
api.add_resource(results, '/api/v1/result', '/api/v1/result/')
api.add_resource(allClasses, '/api/v1/index', '/api/v1/index/')
api.add_resource(templates, '/api/v1/template', '/api/v1/template/')
api.add_resource(genResult, '/api/v1/genResult', '/api/v1/genResult/')