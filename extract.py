import openpyxl
import pandas as pd

template = openpyxl.load_workbook('results.xlsx')

data = pd.read_excel('results.xlsx')

for index, row in data.iterrows():
    lastName = row['SURNAME']
    firstName = row['FIRST NAME']
    middleName = row['MIDDLE NAME']
    
    name = lastName +" " + firstName + " " + middleName
    print (name)