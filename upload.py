import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time




scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\A\\PycharmProjects\\pythonProject3\\abiding-honor-375915-c16db88a8008.json")

file = gspread.authorize(creds)
sh = file.open('2023 초등부 출석표') #woorbook = sh
# print(type(sh.worksheets()[1]))

input('구글에 업로드가 맞는가? 하기전 사본만들기,원본파일 다른곳에 두기!')

all_group=['4-1','4-2','4-3','4-4','4-5','5-1','5-2','5-3','5-4','6-1','6-2','6-3','6-4']
worksheet_list = sh.worksheets()

if len(worksheet_list)!= len(all_group): #에러상황일수도? 워크 시트 기준으로해야맞음
    print(worksheet_list)
    print(all_group)
    input('시트와 변수개수가 안맞다!')
    # time.sleep(600)

for i in range(len(all_group)):
    if all_group[i] == '7-7': #일부분만 올릴때 쓰기
        sheet= sh.worksheet(all_group[i]) #구글 스프레드기준 찾기

        tempdf = pd.read_excel(r'{}.xlsx'.format(all_group[i])) #해당파일찾고 데이터 옮겨오기
        tempdf = tempdf.fillna('')

        sheet.update([tempdf.columns.values.tolist()] +tempdf.values.tolist()) #데이터 덧씌우기

        time.sleep(2)
        print(all_group[i])
    else:
        pass


# print(dataframe.columns.values.tolist())
# print(dataframe.index[5])

# sheet.update_cell(1, 2, 'Bingo!')
# sheet = sh.worksheet("5-1")

# df = {'col0': [1, 2, 3, 4],
#             'col1': [10, 20, 30, 40],
#             'col2': [100, 200, 300, 400]}
# sheet.update(df)

# sheet.insert_row(['날짜\이름','윤시원', '김혜준', '김선', '최시환'], 1)
# sheet.update('A1:A66', list_of_dicts)





# worksheet = sh.add_worksheet(title='4-2',  rows='100', cols='20')
# sh.share('capture490@gmail.com', perm_type='user', role='writer')
# print(sheet.range('A2:A5'))

