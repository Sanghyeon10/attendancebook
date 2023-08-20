import pandas as pd
import making

# 비교할 엑셀 파일의 경로
file_path1 = r'C:\Users\User\Downloads\2023 초등부 출석표.xlsx'
file_path2 = r'C:\Users\User\Downloads\2023 초등부 출석표의 사본8월14일.xlsx'

# 엑셀 파일 불러오기

all_group = making.all_group()
# print(pd.read_excel(file_path1, sheet_name=None))
for i in all_group:
    df1 = pd.read_excel(file_path1, sheet_name=None)[i]
    df2 = pd.read_excel(file_path2, sheet_name=None)[i]

    # 열 단위로 비교하여 차이가 있는지 확인
    diff = pd.concat([df1, df2]).drop_duplicates(keep=False)

    # 차이가 있는 행 출력

    print(i)
    print('칼럼명같음?',df1.columns.tolist()==df2.columns.tolist())
    print(diff)







