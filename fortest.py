import re
import pandas as pd

def calculate_o_ratio_for_series(series):
    start_index = 5  # 6번째 칸까지의 것은 세지 않습니다
    end_index = len(series)-1 #-1해줘야 인덱스 안벗어남
    selected_data = series[start_index:]

    selected_data = selected_data.fillna("") # 결측치 있으면 .str에서 오류남

    # 'O'와 'X'의 개수 세기
    o_count = selected_data.str.count('O').sum()
    x_count = selected_data.str.count('X').sum()

    # 'O'의 비율 계산
    total_count = o_count + x_count
    o_ratio = o_count / total_count if total_count > 0 else 0.0




    series[end_index] = o_ratio

    return series

# 테스트를 위한 예제 데이터
data = pd.Series(['O', 'O', 'X', 'X', None, None, None, 'O', None, 42])

result_series = calculate_o_ratio_for_series(data)
print(result_series)
