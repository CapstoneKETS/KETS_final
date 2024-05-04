import os
import django
import schedule
import time
from django.core.management import execute_from_command_line

def updateTables():
     # Django 쉘에 입력할 내용을 정의합니다.
    shell_input = """
    from functions.GetContentFromUrl import updateTables
    updateTables()
    """

    # Django 쉘을 실행.
    execute_from_command_line(['', 'shell'])

    # Django 쉘에 입력한 내용을 실행.
    exec(shell_input)

if __name__ == '__main__':
    # Django 설정을 초기화.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    print('초기화 완료...')
    django.setup()

    # 매 시간의 55분에 작업을 실행하도록 스케줄을 설정합니다.
    # schedule.every().hour.at(":55").do(updateTables)
    schedule.every().hour.at(":55").do(updateTables)
    while True:
        # 스케줄에 등록된 작업이 실행되어야 할 시간인지 확인하고, 실행합니다.
        schedule.run_pending()
        # 1분마다 스케줄을 확인합니다.
        time.sleep(60)
