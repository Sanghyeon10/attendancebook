import pandas as pd

# 예시 시리즈 생성
data = pd.Series(['A', 'B', 'C', 'O', 'E', 'F', 'O??', 'OG', 'H', 'O'])

# 'O'를 포함하는 경우의 합계 구하기
o_included_sum = data.str.contains('O').sum()

print("O를 포함하는 경우의 합계:", o_included_sum)





#
# from datetime import datetime, timedelta
#
# # 일기 데이터 예시: {날짜: [활동1 여부, 활동2 여부, ...]}
# diary_data = {
#     "2023-08-08": ["운동", "독서", "요리"],
#     "2023-08-09": ["운동", "영화", "쇼핑"],
#     # 날짜와 활동 여부를 기록한 데이터를 입력하세요.
# }
#
# # 활동 이름 리스트
# activity_names = ["운동", "독서", "요리", "영화", "쇼핑", "등산"]  # 실제 활동 이름으로 대체하세요.
#
#
# def print_weekly_summary(data, activities):
#     today = datetime.today()
#     start_of_week = today - timedelta(days=today.weekday())
#
#     weekly_summary = {}
#
#     for date_str, activities_done in data.items():
#         date = datetime.strptime(date_str, "%Y-%m-%d")
#         if start_of_week <= date <= today:
#             for activity in activities_done:
#                 if activity not in weekly_summary:
#                     weekly_summary[activity] = 0
#                 weekly_summary[activity] += 1
#
#     print("주간 활동 요약")
#     print("----------------")
#     for activity, count in weekly_summary.items():
#         print(f"{activity}: {count}번")
#
#
# # 주간 요약 프린트
# print_weekly_summary(diary_data, activity_names)

