import os
import sys
import django
import schedule
from time import *
import subprocess

def updateTables():
    # Django 쉘에 입력할 내용을 정의합니다.
    process = subprocess.Popen(['python', 'manage.py', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, universal_newlines=True)
    script = """
from functions.GetContentFromUrl import updateTables
updateTables()
    """

    print(f'{script}를 장고 쉘에 전달하여 스크립트를 실행합니다...')

    output, errors = process.communicate(input=script)
    print(output)
    print(errors)

if __name__ == '__main__':
    schedule.every().hour.at(":00").do(updateTables)

    while True:
        schedule.run_pending()
        print(gmtime(time() + 32400))
        sleep(60)
