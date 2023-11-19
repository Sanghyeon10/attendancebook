import pandas as pd

# 예시 데이터프레임 생성
data = {'열1': [1, 2, 3, 'X', 'X', 'X', 5],
        '열2': ['X', 2, 'X', "X", 5, 'X', 'X']}
df = pd.DataFrame(data)

# 특정 행의 인덱스
row_index = 3

# 특정 행에서 'X'와 'X'가 아닌 값의 개수 세기
count_x_in_row = df.loc[row_index].tolist().count('X')
count_not_x_in_row = len(df.columns) - count_x_in_row

print(f"행 {row_index}에서 'X'의 개수: {count_x_in_row}")
print(f"행 {row_index}에서 'X'가 아닌 값의 개수: {count_not_x_in_row}")
