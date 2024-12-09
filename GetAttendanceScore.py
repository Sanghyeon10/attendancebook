import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making

all_group= making.all_group()
accumulatedDF=pd.DataFrame( index=making.index())
getscoredic={}

# pd.set_option('display.max_rows', None)  # 모든 행을 출력
# pd.set_option('display.max_columns', None)  # 모든 열을 출력
# pd.set_option('display.width', None)  # 열 너비 제한 없음
# pd.set_option('display.max_colwidth', None)  # 열 내용 생략 없음

# 엑셀 파일의 모든 시트를 병합하는 함수

def getABCD(score):
    if score>=75:
        return "A"
    elif score>=50:
        return "B"
    elif score>=25:
        return "C"
    else:
        return "D"

def merge_sheets_to_dataframe(file_path):

    file_path = making.addressgibon + "2024 초등부 출석표.xlsx"
    #작년 출석자료 파일위치


    # 모든 시트를 데이터프레임으로 읽기
    sheet_dfs = pd.read_excel(file_path, sheet_name=None)  # 모든 시트를 딕셔너리로 읽음

    # 각 시트를 병합하기 전에 이름을 추가하여 구분 (예: 목장 이름)
    merged_df = pd.DataFrame()  # 빈 데이터프레임 생성

    for sheet_name, df in sheet_dfs.items():
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.set_index(df.columns[0], inplace=True)
        df.drop(columns=['기타'], inplace=True)
        df = df.fillna('')
        print(sheet_name)

        if sheet_name != '새신자':
            for name in df.columns:
                if name not in getscoredic.keys():
                    getscoredic[name] = getABCD(int(df.loc[df.index[-1],name]))
                else:
                    print("중복이름",name)

    # print(getscoredic)
    return getscoredic



# 결과 확인

# print(merged_df)
file_path = making.addressgibon+making.ThisYearAttendnce+".xlsx"  # 병합할 엑셀 파일 경로
dict = merge_sheets_to_dataframe(file_path)


