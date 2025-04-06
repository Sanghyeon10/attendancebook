import datetime
import pandas as pd
import making

pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비


tempdf = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, making.ThisYearAttendnce), sheet_name=None)
all_group= making.all_group()


for i in range(len(all_group[:-1])):
    df = tempdf[all_group[i]]  # 해당하는 목장 정보 불러오기
    print(df)

    df['날짜\\이름'] = pd.to_datetime(df['날짜\\이름'], errors='coerce')
    # 인덱스를 날짜로 설정하고 시분초 제거
    df.set_index('날짜\\이름', inplace=True)


    # 시작일과 종료일 설정
    start_date = (datetime.datetime.now() - datetime.timedelta(weeks=4)).date()
    end_date = datetime.datetime.now().date()

    # datetime.date → datetime64로 변환
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # 날짜 범위로 슬라이싱 (정확한 일치 대신 범위로)
    df_range = df.loc[start_date:end_date]

    # 원하는 컬럼 선택 (예: 첫 번째 컬럼)
    for name in df.columns:
        selected_values = df_range.loc[:, name].astype(str).tolist()
        # 문자열 결합
        result = ''.join(selected_values)


        print(name,result)
