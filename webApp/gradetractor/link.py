import gspread
import os
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials

load_dotenv()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
# accountCredentials = Credentials.from_service_account_file(serviceAccountCredentials.json, scopes=scopes)
accountCredentials = gspread.service_account(filename=os.getenv("file"))
# client = gspread.authorize(creds)

resultSheetId = os.getenv("resultSheet")
# # result = client.open_by_key(resultSheetId)

# list =sheet.sheet1.row_values(1)
fullspreadsheet = accountCredentials.open_by_key(resultSheetId)

# print(sh.sheet1.get('A1:AN29'))
# print (list)
# print (worksheet.find("EMY029001"))
value = map(lambda x: x.title, fullspreadsheet.worksheets())
# for i in value:
#     print (i)

if "EMY-C29" in value:
    print("here")
    worksheet = fullspreadsheet.worksheet("EMY-C29")
    location = worksheet.find("EMY029001")
    print(location.row, location.col)
    print(worksheet.get("F7:AL7"))
    