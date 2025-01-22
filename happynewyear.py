import pandas as pd
import datetime
import making
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


next_group = making.next_group()

# 출석 정보가 저장된 파일 경로를 입력합니다.
attendance_file_path = 'farmnameAndkids.txt' #기존 텍본파일과 다른것 사용하기.

makeline=False
setname=False
backupsetname=False


# 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
attendance_dict= making.get_nextyearinfo(attendance_file_path)


# 각 목장의 출석 정보 리스트를 출력합니다.
for farm_name, attendees in attendance_dict.items():
    print(f'{farm_name} 목장 출석자: {attendees}', '인원수:' ,len(attendees))


# 엑셀표 작성해서 출력함
for i in range(len(next_group)):
    df = pd.DataFrame(columns=attendance_dict[next_group[i]], index=making.next_index())
    df.rename_axis('날짜\이름',inplace=True)

    df.to_excel("{}.xlsx".format(next_group[i]),  index=True )  # 5-1식으로 출력




## 양식 최적화시키기

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
#위치 바뀌면 수정해줄것.
file = gspread.authorize(creds)
sheet = file.open(making.nextYearAttendnce)



#스프레드 시트 이름 초기화
making.SetName(setname,file,making.nextYearAttendnce)

for i in range(6):
    making.SetName(backupsetname, file, "백업"+str(i))




##업로드하기 기능

uploadlist = making.next_group()
print("uploadlist:", uploadlist)
now =datetime.datetime.now()
N = int(now.strftime("%U"))% 6

making.upload_data_to_allsheets(file,[making.nextYearAttendnce ], uploadlist, uploadlist )

# 선 초기화
making.MakeCorrectLine(makeline,file,making.nextYearAttendnce, next_group[0]) # next_group[0]

