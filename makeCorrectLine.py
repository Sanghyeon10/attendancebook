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

##파일이름 설정 ,a부터 bJ까지
# sheet = file.open(making.nextYearAttendnce)
sheet = file.open("원페이지")

worksheet_list = sheet.worksheets()
print(worksheet_list)
next_group= making.next_group()

worksheet = sheet.get_worksheet(0)

print(worksheet.cell(2, 1).value)
print(type((worksheet.cell(2, 1).value)))

index = worksheet.col_values(1)[1:-1]
# print(index)
gijun=""

columns= worksheet.row_values(1)[1:-1]
# for j in range( )
for i in range(len(columns)):
    if gijun != datetime.datetime.strptime(worksheet.cell(1, i+2).value, "%Y-%m-%d").month:
        gijun = datetime.datetime.strptime(worksheet.cell(1, i+2).value, "%Y-%m-%d").month
        worksheet.format("{}1:{}77".format(making.getrangecolumns(i+1),making.getrangecolumns(i+1)) , {
            "borders": {"left": {"style": "DOUBLE"}},
        })

    else:
        gijun = datetime.datetime.strptime(worksheet.cell(1, i+2).value, "%Y-%m-%d").month
        worksheet.format("{}1:{}77".format(making.getrangecolumns(i+1),making.getrangecolumns(i+1)) , {
            "borders": {"left": {"style": "DOTTED"}}
        })


    # else: # 세로줄만들기.
    #     worksheet.format("A{}:BB{}".format(str(i+2),str(i+2) ), {
    #         "borders": {"top": {"style": "DOTTED"}},
    #     })


    print(making.getrangecolumns(i + 1))
    time.sleep(2)