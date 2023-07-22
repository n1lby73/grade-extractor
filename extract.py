import pandas as pd
import openpyxl
import shutil
import sys
import os


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

print ("1. EMY \n2. ETY")

try:

    programe = int(input("Kindly input which programe to generate result for: "))

    if programe != 1 and programe != 2:

        print('wrong value entered')

        os.execv(sys.executable, ['python'] + sys.argv)
    
    if programe == 1:

        programe = 'EMY'

        resultTemplate = 'emyTemplate.xlsx'

    else:

        programe = "ETY"

        resultTemplate = 'etyTemplate.xlsx'

except ValueError:

    print('Please select from the above option')

    os.execv(sys.executable, ['python'] + sys.argv)

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

template = openpyxl.load_workbook(resultTemplate)
worksheet = template.worksheets[0]

# workbook = openpyxl.load_workbook('emyety.xlsm')
# sheet_names = workbook.sheetnames

data = pd.read_excel('emyety.xlsm', sheet_name=className, skiprows=1, header=None)

scoreList = []
currentCourseColumn = 11

for _, row in data.iterrows():

    lastName = row.iloc[1]
    firstName = row.iloc[1]
    middleName = row.iloc[2]
    
    score = row.iloc[5:].values

    score = pd.Series(score).fillna('NA').values

    for scores in score[:33]:

        scoreList.append(scores)
    
    average = scoreList[32]

    for scores in scoreList[:32]:

        worksheet.cell(row=currentCourseColumn, column=4, value=scores)

        currentCourseColumn += 1

    name = lastName +" " + firstName + " " + middleName

    worksheet.cell(row=6, column=3, value=name)
    worksheet.cell(row=6, column=5, value=average)
    worksheet.cell(row=4, column=3, value=programe)
    worksheet.cell(row=4, column=5, value=className)

    scoreList = []
    currentCourseColumn = 11

    template.save('{}/{}.xlsx'.format(path,name))