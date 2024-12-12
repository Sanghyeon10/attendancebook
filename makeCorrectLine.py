import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making
import datetime


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
#위치 바뀌면 수정해줄것.
file = gspread.authorize(creds)
sheet = file.open(making.nextYearAttendnce)


worksheet_list = sheet.worksheets()
print(worksheet_list)
next_group= making.next_group()

worksheet = sheet.get_worksheet(0)

print(worksheet.cell(2, 1).value)
print(type((worksheet.cell(2, 1).value)))

index = worksheet.col_values(1)[1:-1]
print(index)
gijun=""

# for j in range( )
for i in range(len(index)):
    if gijun != datetime.datetime.strptime(worksheet.cell(i+2, 1).value, "%Y-%m-%d").month:
        gijun = datetime.datetime.strptime(worksheet.cell(i+2, 1).value, "%Y-%m-%d").month
        worksheet.format("A{}:Z{}".format(str(i+2),str(i+2) ), {
            "borders": {"top": {"style": "DOUBLE"}},
        })

    else:
        worksheet.format("A{}:Z{}".format(str(i+2),str(i+2) ), {
            "borders": {"top": {"style": "DOTTED"}},
        })
    time.sleep(1)