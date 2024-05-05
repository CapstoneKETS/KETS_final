from GetContentFromUrl import *
import schedule
from time import *


if __name__ == '__main__':
    # schedule.every().hour.at(":01").do(updateTables)
    schedule.every().minute.do(updateTables)

    while True:
        schedule.run_pending()
        print(gmtime(time()+32400))
        sleep(60)

    print(kwHistory.objects.all(), kwRank.objects.all(), "remain.")