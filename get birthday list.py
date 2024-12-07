import pandas as pd

# 생일을 기준으로 월별 생일 리스트 출력하는 함수
def print_birthdays_by_month(file_path, sheet_name):
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # "생일" 칼럼에서 날짜를 datetime 형식으로 변환
        df['생일'] = pd.to_datetime(df['생일'], format='%y.%m.%d', errors='coerce')  # 잘못된 날짜는 NaT로 처리

        # 월별로 그룹화하여 출력
        for month in range(1, 13):  # 1월부터 12월까지
            print()
            birthdays = df[df['생일'].dt.month == month]
            if not birthdays.empty:
                print(f"{month}월:")
                print(birthdays[['이름','생일']])
                print(str(len(birthdays[['이름','생일']])) + '명')
            else:
                print(f"{month}월: 생일 없음")


    except FileNotFoundError:
        print(f"파일 '{file_path}'을 찾을 수 없습니다.")
    except KeyError:
        print(f"'생일' 칼럼이 존재하지 않습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 사용 예제
file_path = r"C:\Users\captu\Downloads\아이들 정보.xlsx"  # 엑셀 파일 경로
sheet_name = "시트1"          # 시트 이름
print_birthdays_by_month(file_path, sheet_name)