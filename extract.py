from dotenv import load_dotenv
import pandas as pd
import requests
import openpyxl
import shutil
import sys
import os

load_dotenv()

#function to create folder

def createFolder(nameOfFolder):

    if not os.path.exists(nameOfFolder):

        os.mkdir(nameOfFolder)

        folderName = nameOfFolder

        return folderName
 
    while True:

        confirmAction = input("Folder name ({}) already exist, do you want to overwrite [y/n]: ".format(nameOfFolder))

        if confirmAction == 'y' or confirmAction == 'Y':

            shutil.rmtree(nameOfFolder)

            os.mkdir(nameOfFolder)

            folderName = nameOfFolder

            break

            
        elif confirmAction == 'n' or confirmAction == 'N':

            newdir = input("Input new folder name: ")

            folderName = createFolder(newdir)

            break

        else:

            print('\nWrong value entered')
    
    return folderName

# function to send message via telegram bot

def sendToTelegram(document, caption):

    apiToken = os.getenv('botToken')

    chatID = os.getenv('chatID')
    
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendDocument'

    try:

        payload = {'chat_id': chatID, 'caption': caption}
        files = {'document': open(document, "rb")}

        response = requests.post(apiURL, data=payload, files=files)

        if response.status_code == 200:

            print("Document sent successfully!")

        else:

            print(f"Failed to send document: {response.text}")
            
    except Exception as e:

        print(e)


# allow user to select programe name

print ("1. EMY \n2. ETY")

try:

    programe = int(input("Kindly input which programe to generate result for: "))

    if programe != 1 and programe != 2:

        print('wrong value entered')

        os.execv(sys.executable, ['python'] + sys.argv)
    
    if programe == 1:

        programe = 'EMY'

        fullPrograme = "ElectroMechanics"

        resultTemplate = 'emyTemplate.xlsx'

    else:

        programe = "ETY"

        fullPrograme = "ElectroTechnics"

        resultTemplate = 'etyTemplate.xlsx'

except ValueError:

    print('Please select from the above option')

    os.execv(sys.executable, ['python'] + sys.argv)

# allow user to select class number

while True:

    try:

        classNumber = int(input("Please input only number excluding 'C': "))

        className = programe+"-C"+str(classNumber)

        workbook = openpyxl.load_workbook('emyety.xlsm')
        sheet_names = workbook.sheetnames
        
        if className not in sheet_names:

            print("Class details not available in excel database\nKindly provide all necessary details again or update excel database")

            os.execv(sys.executable, ['python'] + sys.argv)

        while True:

            confirmSelection = input("Do you want to generate result sheet for every student in "+ className + " (Y/N): ")

            if confirmSelection == "y" or confirmSelection == "Y":

                folder = className + " individual compiled result"
                
                path = createFolder(folder)

                break

            elif confirmSelection == "n" or confirmSelection == "N":

                os.execv(sys.executable, ['python'] + sys.argv)

            else:

                print ("wrong value entered")

        break

    except ValueError:

        print("Please input a number\n")

#load work sheet        

template = openpyxl.load_workbook(resultTemplate)
worksheet = template.worksheets[0]

data = pd.read_excel('emyety.xlsm', sheet_name=className, skiprows=5, header=None, nrows=24)

scoreList = []
currentCourseColumn = 11
trackFailure = 0
probation = []
termination = []

# iterate through worksheet and manipulate data

for _, row in data.iterrows():

    lastName = row.iloc[1]
    firstName = row.iloc[2]
    middleName = row.iloc[3]
    
    score = row.iloc[5:].values

    score = pd.Series(score).fillna('NA').values

    for scores in score[:33]:

        scoreList.append(scores)
    
    average = scoreList[32]

    for scores in scoreList[:32]:

        try:

            if int(scores) < 60:

                trackFailure += 1
        
        except:

            pass

        worksheet.cell(row=currentCourseColumn, column=4, value=scores)

        currentCourseColumn += 1

    name = str(lastName) + " " + str(firstName) + " " + str(middleName)

    worksheet.cell(row=6, column=3, value=name)
    worksheet.cell(row=6, column=5, value=average)
    worksheet.cell(row=4, column=3, value=fullPrograme)
    worksheet.cell(row=4, column=5, value=className)

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

        template.save('{}/{}.xlsx'.format(path,name))
    
    except:

        pass

# loop to delete null report file created cause of incomplete class

for filename in os.listdir(path):
        
    if "nan" in filename:

        file_path = os.path.join(path, filename)

        os.remove(file_path)

# create file to store probation and termination list

probationFile = open("ProbationList.txt", "x")
terminationFile = open("TerminationList.txt", "x")

# generate student on probation

for watchlist in probation:
    
    probationFile.write(watchlist + '\n')

# generate student on termination

for watchlist in termination:
    
    terminationFile.write(watchlist + '\n')

# Save and close files before sending

probationFile.close()
terminationFile.close()

# send generated data to telegram

caption = "This is a txt file containing list of student due for probation"

sendToTelegram("ProbationList.txt", caption)

caption = "This is a txt file containing list of student due for termination"

sendToTelegram("TerminationList.txt", caption)

#delete file after sending

os.remove("TerminationList.txt")
os.remove("ProbationList.txt")