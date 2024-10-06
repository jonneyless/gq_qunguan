import time

from lib import db
from net import sendMessage

url = "https://api.telegram.org/bot6606856940:AAETBE50vrOjRutFm2E87J9bEguDrLT-Ejc/"


def check():
    groups = db.getGroupsNeedHiddenMember()

if __name__ == '__main__':
    while True:
        check()
        time.sleep(1800)
