import time

from lib import db
from net import sendMessage

url = "https://api.telegram.org/bot6606856940:AAETBE50vrOjRutFm2E87J9bEguDrLT-Ejc/"


def check():
    groupNums = db.getActiveDanbaoGroupNums()
    groups = db.getGroupsByNums(groupNums)

    existsGroupNums = {}
    for group in groups:
        num = group['group_num']
        if num not in existsGroupNums:
            existsGroupNums[num] = 1
        else:
            existsGroupNums[num] += 1

    NotExistsGroupNums = []
    MoreCountGroupNums = []
    for num in groupNums:
        if num not in existsGroupNums:
            NotExistsGroupNums.append(str(num))
        elif existsGroupNums[num] > 1:
            MoreCountGroupNums.append(str(num))

    if len(NotExistsGroupNums) > 0:
        sendMessage(url, -1002377514396, "这些群编号不存在：" + ', '.join(NotExistsGroupNums))

    if len(MoreCountGroupNums) > 0:
        sendMessage(url, -1002377514396, "这些群编号存在多个群：" + ', '.join(MoreCountGroupNums))


if __name__ == '__main__':
    while True:
        check()
        time.sleep(1)
