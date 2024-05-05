import os
import sys

import django
import schedule
import time
import subprocess

def updateTables():
    # Django 쉘에 입력할 내용을 정의합니다.
    process = subprocess.Popen(['python', 'manage.py', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # updatetables() 함수를 호출하는 스크립트를 정의합니다.
    script = """
    from functions.GetContentFromUrl import updateTables
    updateTables()
    """
    # 스크립트를 장고 쉘에 전달하여 실행합니다.
    print(f'{script}를 장고 쉘에 전달하여 스크립트를 실행합니다...')
    output, errors = process.communicate(input=script)
    print('전달 완료, 실행중....')
    # 반환 코드를 가져옵니다.
    return_code = process.wait()

    # 반환 코드를 확인하여 스크립트가 성공적으로 종료되었는지 확인합니다.
    if return_code == 0:
        print("스크립트가 성공적으로 실행되었습니다.")
        sys.exit(0)  # 성공적으로 실행된 경우 종료합니다.
    else:
        print("스크립트 실행 중 오류가 발생했습니다.")
        sys.exit(0)
if __name__ == '__main__':
    # 매 시간의 55분에 작업을 실행하도록 스케줄을 설정합니다.
    schedule.every().hour.at(":07").do(updateTables)
    while True:
        # 스케줄에 등록된 작업이 실행되어야 할 시간인지 확인하고, 실행합니다.
        schedule.run_pending()
        # 1분마다 스케줄을 확인합니다.
        time.sleep(60)
