import openpyxl
import pandas as pd

template = openpyxl.load_workbook('template.xlsx')
worksheet = template.worksheets[0]

data = pd.read_excel('results.xlsx')

scoreList = []
currentCourseColumn = 11

for index, row in data.iterrows():

    lastName = row['SURNAME']
    firstName = row['FIRST NAME']
    middleName = row['MIDDLE NAME']
    
    score = data.iloc[index,5:].values

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

    scoreList = []
    currentCourseColumn = 11

    template.save('{}.xlsx'.format(name))