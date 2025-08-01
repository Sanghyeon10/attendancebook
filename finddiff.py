import pandas as pd
import making




pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비

# 비교할 엑셀 파일의 경로
file_path1 = r'{}{}.xlsx'.format(making.addressgibon, making.ThisYearAttendnce)
file_path2 = r'{}백업3.xlsx'.format(making.addressgibon)



# 엑셀 파일 불러오기

all_group = making.all_group()
# print(pd.read_excel(file_path1, sheet_name=None))
for i in all_group:
    df1 = pd.read_excel(file_path1, sheet_name=None)[i]
    df2 = pd.read_excel(file_path2, sheet_name=None)[i]

    # 열 단위로 비교하여 차이가 있는지 확인
    diff = pd.concat([df2, df1]).drop_duplicates(keep=False)

    # 차이가 있는 행 출력

    print(i)
    print('칼럼명같음?',set(df1.columns)== set(df2.columns))
    diff = diff[diff['날짜\이름']!='비고'] #비고는 의미가 없으므로 제거


    # 칼럼을 여러 조각으로 나누어 프린트하기
    chunk_size = 20  # 각 조각의 크기를 설정, 짤려서 안 보이는게 없는게 기준

    num_chunks = len(diff.columns) // chunk_size + 1

    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk_columns = diff.columns[start:end]
        print(diff[chunk_columns])
        print()  # 각 조각 사이에 공백 라인 삽입







