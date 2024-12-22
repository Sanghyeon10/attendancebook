import pandas as pd

# 예시 데이터프레임
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['a', 'b', 'c']
})

# 새로 삽입할 행
new_row = [4, 'd']

# 삽입할 위치 (2번째 행 뒤에 삽입)
insert_position = 2

# 데이터프레임을 나누고 새 행 삽입
df_top = df.iloc[:insert_position]
df_bottom = df.iloc[insert_position:]
df = pd.concat([df_top, pd.DataFrame([new_row], columns=df.columns), df_bottom]).reset_index(drop=True)

print(df)
