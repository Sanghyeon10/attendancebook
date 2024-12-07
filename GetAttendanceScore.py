import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making

all_group= making.all_group()
accumulatedDF=pd.DataFrame( index=making.index())

pd.set_option('display.max_rows', None)  # 모든 행을 출력
pd.set_option('display.max_columns', None)  # 모든 열을 출력
pd.set_option('display.width', None)  # 열 너비 제한 없음
pd.set_option('display.max_colwidth', None)  # 열 내용 생략 없음

# 엑셀 파일의 모든 시트를 병합하는 함수
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

        jongbocheck =set(df.columns) & set(merged_df.columns) #교집합이 있는경우(겹치는게 있다)
        havetoaddlist= list(set(df.columns)-set(merged_df.columns))

        # print(df)
        print(jongbocheck)

        if jongbocheck != set() :# 겹치는게 있다면
            # df.update(merged_df, overwrite=True, filter_func=lambda x: x == "X")  # 추가해야할 df의 정보를 먼저 업데이트 새신자 목장 데이터 오류방지.
            # merged_df.update(df, overwrite=True)
            merged_df = merged_df.join(df[havetoaddlist], how='left')  # 덮어씌울게 없으면 따로 추가해주기.
            # merged_df = pd.merge(merged_df, df[remainlist], left_index=True, right_index=True, how='outer', suffixes=(None, f"_{sheet_name}"))
        else: #안겹치면 그냥 더하기
            merged_df = pd.merge(merged_df, df, left_index=True, right_index=True, how='outer')

        if merged_df.empty: #첫번째로 비어있는건 통째로 복사
            merged_df = df.copy()

        print(merged_df)
    return merged_df




# 결과 확인

# print(merged_df)
file_path = making.addressgibon+making.ThisYearAttendnce+".xlsx"  # 병합할 엑셀 파일 경로
merged_df = merge_sheets_to_dataframe(file_path)

# 병합 결과를 새 엑셀 파일로 저장
merged_df.to_excel("AttendanceScore.xlsx", index=False)
