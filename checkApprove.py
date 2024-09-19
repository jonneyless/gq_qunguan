import time

from lib import db
from net import sendMessage

url = "https://api.telegram.org/bot6606856940:AAETBE50vrOjRutFm2E87J9bEguDrLT-Ejc/"


def check():
    data = db.getWaitingApprove()

    groupStat = {}
    groupIds = []
    for datum in data:
        groupId = datum['group_tg_id']
        userId = datum['user_tg_id']
        if groupId not in groupStat:
            groupStat[groupId] = []

        if userId not in groupStat[groupId]:
            groupStat[groupId].append(userId)
            groupIds.append(groupId)

    groups = db.getGroupsByTgIds(groupIds)

    for group in groups:
        sendMessage(url, -1002377514396, "公群：" + str(group['group_num']) + " 未审核用户数：" + str(len(groupStat[str(group['chat_id'])])))


if __name__ == '__main__':
    while True:
        check()
        time.sleep(3600)
