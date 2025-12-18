import pandas as pd
import making
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making
import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import re


pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비

namedict = making.get_name()



# 생일을 기준으로 월별 생일 리스트 출력하는 함수
def print_birthdays_by_month(file_path, sheet_name,attendance_dict):
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # "생일" 칼럼에서 날짜를 datetime 형식으로 변환
        df['생일'] = pd.to_datetime(df['생일'], format='%y.%m.%d', errors='coerce')  # 잘못된 날짜는 NaT로 처리
        df["목장"] = df['이름'].apply(lambda x: getwherefarm(x, attendance_dict))
        # df= df[df['목장']!=""]
        # print(df)

        textprint = pd.DataFrame(columns=['목장','이름','생일'])
        # 월별로 그룹화하여 출력
        for month in range(1,13):  # 1월부터 12월까지
            print()
            birthdays = df[df['생일'].dt.month == month]


            if not birthdays.empty:
                # print(f"{month}월:")
                # print(birthdays[['목장','이름','생일']].sort_values(by="목장"))
                # print(str(len(birthdays[['이름']])) + '명')

                # Beforetextprint= pd.concat([textprint, birthdays[['목장','이름','생일']].sort_values(by="목장").fillna('')], ignore_index=True)
                Beforetextprint = birthdays[['목장', '이름', '생일']].sort_values(by="목장").fillna('')
                new_row = pd.DataFrame({'목장': month, '이름': "월",'생일': (str(len(birthdays[['이름']])) + '명') },index=["gijun"])
                temptemp = pd.concat([ new_row,Beforetextprint] , ignore_index=True)
                textprint= pd.concat([textprint, temptemp] , ignore_index=True)

            else:
                print(f"{month}월: 생일 없음")


            # print(textprint)


    except FileNotFoundError:
        print(f"파일 '{file_path}'을 찾을 수 없습니다.")
    except KeyError:
        print(f"'생일' 칼럼이 존재하지 않습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    # print(textprint)
    return textprint

def getwherefarm(name, attendance_dict):
    group = making.next_group()  # 그룹 목록 생성
    info = ""  # 이름이 속한 그룹 정보 저장
    group_count = 0  # 이름이 속한 그룹의 개수

    for i in group:
        if name in attendance_dict[i]:  # 이름이 해당 그룹에 있는지 확인
            info += i + " "  # 그룹 이름 추가
            group_count += 1  # 그룹 카운트 증가

    if group_count > 1:  # 중복 여부 확인
        print(f"중복된 이름: '{name}', 그룹: {info.strip()}")
    elif isinstance(name, str) and (name in namedict.values() or re.search(r'\(음력\)$', name)):
        # print(f"'{name}'는 선생님." )
        info = info +"선생님"

    elif group_count == 0:
        print(f"'{name}'는 어떤 그룹에도 속하지 않습니다.")

    return info.strip()  # 이름이 속한 그룹 정보 반환


def update_attendance(row, full_name_list,attended):
    name = row['이름']
    if name not in full_name_list:
        return row['출석상태']  # 명부에 없으면 그대로 유지
    elif name in attended:
        return row['출석상태'] + 'O'
    else:
        return row['출석상태'] + 'X'

def attadancestate(textprint):
    tempdf = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, making.ThisYearAttendnce), sheet_name=None)
    all_group = making.all_group()
    textprint['출석상태']=""

    ## 오늘의 출석정보
    attended=[]
    full_name_list=[]
    attendance_dict, __ = making.make_data_from_file("attendance.txt")
    full_name_dict, ___ = making.make_data_from_file("farmnameAndkids.txt")

    for key in attendance_dict.keys():
        attended += attendance_dict[key]

    for key in full_name_dict.keys():
        full_name_list += full_name_dict[key]

    # print(full_name_list)

    # 시작일과 종료일 설정
    start_date = (datetime.datetime.now() - datetime.timedelta(weeks=6) - datetime.timedelta(
        days=datetime.datetime.now().weekday() + 1)).date()
    print(start_date)
    end_date = (datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 1)).date()
    print(end_date)
    # datetime.date → datetime64로 변환
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    for i in range(len(all_group[:-1])): ##새신자는 제외
        df = tempdf[all_group[i]]  # 해당하는 목장 정보 불러오기
        # print(df)
        df=df.fillna("")
        df['날짜\\이름'] = pd.to_datetime(df['날짜\\이름'], errors='coerce')
        # 인덱스를 날짜로 설정하고 시분초 제거
        df.set_index('날짜\\이름', inplace=True)


        # 날짜 범위로 슬라이싱 (정확한 일치 대신 범위로)
        df_range = df.loc[start_date:end_date]

        # 원하는 컬럼 선택 (예: 첫 번째 컬럼)
        for name in df.columns:
            selected_values = df_range.loc[:, name].astype(str).tolist()
            # 문자열 결합
            result = ''.join(selected_values)


            for k in range(len(textprint)):
                if textprint.loc[textprint.index[k],'이름']==name:
                    textprint.loc[textprint.index[k],'출석상태'] = result
            #
            # print(name, result)

    textprint['출석상태'] = textprint.apply(
        lambda row: update_attendance(row, full_name_list=full_name_list, attended=attended),
        axis=1
    )



attendance_file_path = 'farmnameAndkids.txt'
attendance_dict= making.get_keyAndlist(attendance_file_path)

# print(getwherefarm("천송현",attendance_dict))



# 사용 예제
file_path = making.destination_folder+"아이들 정보.xlsx"  # 엑셀 파일 경로
sheet_name = "시트1"          # 시트 이름
textprint = print_birthdays_by_month(file_path, sheet_name,attendance_dict)
textprint['생일'] = textprint['생일'].apply(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, datetime.datetime) else x)
attadancestate(textprint)

birthdaylist="생일자 리스트"

textprint.to_excel(making.year +birthdaylist+'.xlsx')

print(textprint)


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)


making.upload_data_to_sheets(file,[making.year +birthdaylist])