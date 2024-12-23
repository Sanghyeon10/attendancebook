import pandas as pd
import making

pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비

# 생일을 기준으로 월별 생일 리스트 출력하는 함수
def print_birthdays_by_month(file_path, sheet_name,attendance_dict):
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # "생일" 칼럼에서 날짜를 datetime 형식으로 변환
        df['생일'] = pd.to_datetime(df['생일'], format='%y.%m.%d', errors='coerce')  # 잘못된 날짜는 NaT로 처리
        df["목장"] = df['이름'].apply(lambda x: getwherefarm(x, attendance_dict))
        # print(df)

        # 월별로 그룹화하여 출력
        for month in range(1, 13):  # 1월부터 12월까지
            print()
            birthdays = df[df['생일'].dt.month == month]


            if not birthdays.empty:
                print(f"{month}월:")
                print(birthdays[['목장','이름','생일']])
                print(str(len(birthdays[['이름']])) + '명')
            else:
                print(f"{month}월: 생일 없음")


    except FileNotFoundError:
        print(f"파일 '{file_path}'을 찾을 수 없습니다.")
    except KeyError:
        print(f"'생일' 칼럼이 존재하지 않습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")



def getwherefarm(name, attendance_dict):
    group = making.next_group()  # 그룹 목록 생성
    info = ""  # 이름이 속한 그룹 정보 저장
    group_count = 0  # 이름이 속한 그룹의 개수

    for i in group:
        if name in attendance_dict[i]:  # 이름이 해당 그룹에 있는지 확인
            info += i + " "  # 그룹 이름 추가
            group_count += 1  # 그룹 카운트 증가

    if group_count > 1:  # 중복 여부 확인
        print(f"중복된 이름: '{name}', 그룹: {info.strip()}")
    elif group_count == 0:
        print(f"'{name}'는 어떤 그룹에도 속하지 않습니다.")

    return info.strip()  # 이름이 속한 그룹 정보 반환



attendance_file_path = 'farmnameAndkids.txt'
attendance_dict= making.get_keyAndlist(attendance_file_path)

# print(getwherefarm("천송현",attendance_dict))



# 사용 예제
file_path = r"C:\Users\captu\Downloads\아이들 정보.xlsx"  # 엑셀 파일 경로
sheet_name = "시트1"          # 시트 이름
print_birthdays_by_month(file_path, sheet_name,attendance_dict)