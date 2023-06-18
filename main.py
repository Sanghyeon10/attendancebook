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



print('최신껄로 다운로드 후 진행할것')
subprocess.run(["python", "makefile.py"])
subprocess.run(["python", "new.py"])
# subprocess.run(["python", "make order.py"])


subprocess.run(["python", "upload.py"])
subprocess.run(["python", "newupload.py"])
subprocess.run(["python", "hongattendance.py"])


file_path = r"C:\Users\A\Downloads/2023 초등부 출석표.xlsx"
removingexcel(file_path)
file_path = r"C:\Users\A\Downloads/새친구 관리엑셀표.xlsx"
removingexcel(file_path)

print('사본 만들기')

