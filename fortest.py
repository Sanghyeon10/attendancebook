import pandas as pd
import numpy as np

# 큰 데이터프레임 생성 예시 (10개의 행, 10개의 열)
np.random.seed(42)
data = np.random.randint(0, 100, size=(10, 10))
columns = [f'칼럼{i}' for i in range(10)]

df = pd.DataFrame(data, columns=columns)

# 칼럼을 여러 조각으로 나누어 프린트하기
chunk_size = 3  # 각 조각의 크기를 설정

num_chunks = len(df.columns) // chunk_size + 1

for i in range(num_chunks):
    start = i * chunk_size
    end = (i + 1) * chunk_size
    chunk_columns = df.columns[start:end]
    print(df[chunk_columns])
    print()  # 각 조각 사이에 공백 라인 삽입
