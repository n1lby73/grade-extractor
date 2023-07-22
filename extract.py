import openpyxl
import pandas as pd
import os
import sys

print ("1. EMY \n2. ETY")

try:

    programe = int(input("Kindly input which programe to generate result for: "))

    if programe != 1 and programe != 2:

        print('wrong value entered')

        os.execv(sys.executable, ['python'] + sys.argv)
    
    if programe == 1:

        programe = 'EMY'

    else:

        programe = "ETY"

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

        break

    except ValueError:

        print("Please input a number\n")


className = programe+"-C"+classNumber

workbook = openpyxl.load_workbook('emyety.xlsm')
sheet_names = workbook.sheetnames

template = openpyxl.load_workbook('emyTemplate.xlsx')
worksheet = template.worksheets[0]

# workbook = openpyxl.load_workbook('emyety.xlsm')
# sheet_names = workbook.sheetnames

# data = pd.read_excel('results.xlsx', skiprows=1, header=None)

# scoreList = []
# currentCourseColumn = 11

# for _, row in data.iterrows():

#     lastName = row.iloc[1]
#     firstName = row.iloc[1]
#     middleName = row.iloc[2]
    
#     score = row.iloc[5:].values

#     score = pd.Series(score).fillna('NA').values

#     for scores in score[:33]:

#         scoreList.append(scores)
    
#     average = scoreList[32]

#     for scores in scoreList[:32]:

#         worksheet.cell(row=currentCourseColumn, column=4, value=scores)

#         currentCourseColumn += 1

#     name = lastName +" " + firstName + " " + middleName

#     worksheet.cell(row=6, column=3, value=name)
#     worksheet.cell(row=6, column=5, value=average)

#     scoreList = []
#     currentCourseColumn = 11

#     template.save('{}.xlsx'.format(name))