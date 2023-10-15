import pandas as pd

# 예제 시리즈 생성
A = pd.Series([1, 2, 3, 4, 5])
B = pd.Series([10, 20, 30, 40, 50])

# 조건을 만족하는 A의 값에 해당하는 B의 값을 가져오고 싶다면
condition = A == 3  # 예를 들어, A 시리즈에서 값이 3인 경우

# 조건을 만족하는 경우 B 시리즈의 값을 가져옴
result = B[condition]

print(result)
