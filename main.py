import subprocess
import time
import os
import sys


def removingexcel(file_path):
    if os.path.exists(file_path):
        # 파일 제거
        os.remove(file_path)
        print(file_path,"파일이 성공적으로 제거되었습니다.")
    else:
        print(file_path,"파일이 존재하지 않습니다.")



print('최신껄로 다운로드 후 진행할것+nocome텍스트파일 확인하기')
subprocess.Popen([sys.executable, "beforecheck.py"]).communicate() #명단 제대로 인식되는지 누락여부 먼저 체크
subprocess.Popen([sys.executable, "makefile.py"]).communicate() #파일 생성하기 이번주 아닌거 작성시에는 코드 N입력 코드 수정해서쓰기
subprocess.Popen([sys.executable, "new.py"]).communicate()  #파일 생성하기
# subprocess.run(["python", "make order.py"]) #출석율순으로 정렬+ 명단 프린트해주기


subprocess.Popen([sys.executable, "upload.py"]).communicate() #구글 스르페드 시트에 업로드
subprocess.Popen([sys.executable, "newupload.py"]).communicate()
subprocess.Popen([sys.executable, "hongattendance.py"]).communicate() #특정 목장을 위해 따로 만들어진 출석부


file_path = r"C:\Users\user\Downloads/2023 초등부 출석표.xlsx" #삭제안하면, 실수할수 있어서 자동삭제.
removingexcel(file_path)
file_path = r"C:\Users\user\Downloads/새친구 관리엑셀표.xlsx"
removingexcel(file_path)

input('사본 만들기?+nocome은 지우기')
