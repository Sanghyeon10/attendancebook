import subprocess
import time
import os


def removingexcel(file_path):
    if os.path.exists(file_path):
        # 파일 제거
        os.remove(file_path)
        print(file_path,"파일이 성공적으로 제거되었습니다.")
    else:
        print(file_path,"파일이 존재하지 않습니다.")



print('최신껄로 다운로드 후 진행할것+nocome텍스트파일 확인하기')
subprocess.run(["python", "makefile.py"]) #파일 생성하기
# subprocess.run(["python",'exceptdatainput']) #이번주 아닌거 작성시 사용.
subprocess.run(["python", "new.py"]) #파일 생성하기
# subprocess.run(["python", "make order.py"]) #출석율순으로 정렬+ 명단 프린트해주기


subprocess.run(["python", "upload.py"]) #구글 스르페드 시트에 업로드
subprocess.run(["python", "newupload.py"])
subprocess.run(["python", "hongattendance.py"]) #특정 목장을 위해 따로 만들어진 출석부


file_path = r"C:\Users\A\Downloads/2023 초등부 출석표.xlsx" #삭제안하면, 실수할수 있어서 자동삭제.
removingexcel(file_path)
file_path = r"C:\Users\A\Downloads/새친구 관리엑셀표.xlsx"
removingexcel(file_path)

input('사본 만들기?+nocome은 지우기')
