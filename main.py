import subprocess
import time
import os
import sys
import making


print('최신껄로 다운로드 후 진행할것+nocome텍스트파일 확인하기')
subprocess.Popen([sys.executable, "beforecheck.py"]).communicate() #명단 제대로 인식되는지 누락여부 먼저 체크
subprocess.Popen([sys.executable, "makefile.py"]).communicate() #파일 생성하기 이번주 아닌거 작성시에는 코드 N입력 코드 수정해서쓰기
subprocess.Popen([sys.executable, "new.py"]).communicate()  #파일 생성하기



# subprocess.Popen([sys.executable, "upload.py"]).communicate() #구글 스르페드 시트에 업로드
# subprocess.Popen([sys.executable, "extrafileupload.py"]).communicate() #새친구, 새신자 전용 파일, 특정목장 업로드

subprocess.Popen([sys.executable, "make order.py"]).communicate() #전체 명단 확보하기

# file_path = r'C:\Users\User\Downloads\{}.xlsx'.format(making.ThisYearAttendnce) #삭제안하면, 실수할수 있어서 자동삭제.
# making.removingexcel(file_path)
# file_path = r'C:\Users\User\Downloads\{}.xlsx'.format(making.Newmembers)
# making.removingexcel(file_path)

input('사본 만들기, 구글폼 행숨기기하기, 구글폼 명단 개정해주기, 오래된 백업파일 삭제하기')