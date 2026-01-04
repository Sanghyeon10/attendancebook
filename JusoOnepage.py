import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making
import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

def getSchoolList(df):
    text=""
    # 초등학교 리스트 정의
    초등학교_목록 = ['원묵초','중화초','새솔초', '면목초', "금성초", "묵현초", "불암초", "대광초", "봉화초", '갈매초', '장위초', "안평초", '태릉초',
               "경희초",'신현초',"샛별초","미사중앙초","서울동원초","회암초", "화접초","노일초","동원초","양원숲초","상봉초","다산하늘초"]  # 여기에 원하는 학교를 계속 추가

    # 새로운 '초등학교' 칼럼 생성 및 초기화
    df['초등학교'] = None

    # 알 수 없는(리스트에 없는) 초등학교 비고 내용을 저장할 리스트
    알수없는_학교_비고 = []

    # 비고에서 초등학교 이름이 포함되어 있는지 확인
    for idx in df.index:
        비고내용 = str(df.loc[idx, '비고'])  # 비고 칼럼 값 문자열로 변환
        학교_찾음 = False
        for 학교 in 초등학교_목록:
            if 학교 in 비고내용:
                df.loc[idx, '초등학교'] = 학교
                학교_찾음 = True
                break  # 하나라도 찾으면 멈춤
        # '초'가 포함되어 있고, 위 리스트에서 못 찾은 경우 출력용으로 저장
        if not 학교_찾음 and '초' in 비고내용:
            알수없는_학교_비고.append(비고내용)

    # 리스트에 없는 초등학교 비고내용 출력
    if 알수없는_학교_비고:
        print("\n[초등학교 리스트에 없는 비고 내용들]:")
        for 내용 in set(알수없는_학교_비고):  # 중복 제거
            print("-", 내용)
    else:
        print("\n모든 '초' 포함 비고 내용이 목록에 있음.")

    # 초등학교가 명시된 행만 필터링
    초등학교_명단 = df[df['초등학교'].notna()]

    # 결과 확인
    # print("\n[초등학교 전체 명단]")
    # print(초등학교_명단)

    # 학교별 이름 명단 출력
    # print("\n[학교별 이름 명단]")

    # ✅ 학교별 인원 많은 순서대로 정렬
    학교별_카운트 = 초등학교_명단['초등학교'].value_counts()

    for 학교 in 학교별_카운트.index:
        학교_df = 초등학교_명단[초등학교_명단['초등학교'] == 학교]
        text += f"\n✅ {학교} ({len(학교_df)}명)\n" + 학교_df[['이름', '목장']].to_string(index=False) + "\n"

    return text



pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비

all_group= making.all_group()

attendance_file_path = 'farmnameAndkids.txt' #기존 텍본파일과 다른것 사용하기.
# 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
attendance_dict= making.get_nextyearinfo(attendance_file_path)


making.move_attendance_file(["아이들 정보"]) #다운로드 파일부터 개인파일로 옮기기
df = pd.read_excel(making.destination_folder+"아이들 정보.xlsx", sheet_name='시트1' ,index_col=0 )



df=df[['비고']]
df= df.reset_index()
# print(df)

for i in range(len(df)):
    for farm_name, attendees in attendance_dict.items():
        if df.loc[df.index[i], '이름'] in  attendees:
            df.loc[df.index[i], '목장'] = farm_name

df= df.dropna(subset=['목장'])
df=df[["이름",'목장','비고']].sort_values(by="목장")
# print(df)


lines = [x.strip() for x in getSchoolList(df).split('\n') if x.strip() and "이름" not in x ]
lines2= [x.strip() for x in making.GetAttendanceScoreYear().split('\n') if x.strip() ]
new_index = max(len(df), len(lines), len(lines2))
df = df.reset_index(drop=True)
df = df.reindex(range(new_index))

df["이름,목장"] = pd.Series(lines)
df['개근,정근'] = pd.Series(lines2)

# 예전 코드
# df.loc[new_index] = [None] * len(df.columns)  # 먼저 빈 행 추가
# df.at[new_index, df.columns[0]] = getSchoolList(df)          # 첫 번째 열만 채움
# df.at[new_index,df.columns[1]]= making.GetAttendaceScroe()


print(df)
# input("stop")

JunsoOnepage="주소원페이지"

df.to_excel(making.year + JunsoOnepage+'.xlsx')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)

making.upload_data_to_sheets(file,[making.year + JunsoOnepage])

