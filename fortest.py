import re

def read_nocome_from_file(nocome_file_path):
    nocome_dict = {}

    with open(nocome_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 정규 표현식을 사용하여 첫 번째 공백문자로 분리합니다.
            pattern = r'^(\S+)\s(.+)$'
            match = re.match(pattern, line)

            if match:
                # 두 개의 그룹으로 나눈 문자열을 변수에 저장합니다.
                farm_name = match.group(1)
                reason = match.group(2).strip()  # 리스트에서 양쪽 공백 제거
                # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
                nocome_dict[farm_name] = reason

    return nocome_dict

# 예시: 테스트 파일 'nocome.txt'에서 데이터 읽기
nocome_file_path = 'nocome.txt'
nocome_dict = read_nocome_from_file(nocome_file_path)
print(nocome_dict)
