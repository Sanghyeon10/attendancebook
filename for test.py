import pandas as pd

# 가상의 DataFrame 생성
data = {
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8]
}

df1 = pd.DataFrame(data)

# 업데이트용 DataFrame 생성
data_to_update = {
    'A': [0, 0, 0, 0],
    'B': [10, 20, 30, 40]
}

df2 = pd.DataFrame(data_to_update)

# filter_func를 정의하여 업데이트할 조건 설정
def filter_condition(x):
    return x > 2  # 값이 2보다 큰 경우에만 업데이트

# filter_func을 사용하여 df1을 df2로 업데이트
df1.update(df2, filter_func=filter_condition)

print(df1)
