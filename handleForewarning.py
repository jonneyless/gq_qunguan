import math
import re
import threading

import helpp
import net
from config import threadNumMaps
from lib import db

thread_num = threadNumMaps['forewarning']


class MyThread(threading.Thread):
    def __init__(self, threadName, groupIds):
        super(MyThread, self).__init__()
        self.threadName = threadName
        self.groupIds = groupIds

    def run(self):
        threadName = self.threadName

        for groupId in self.groupIds:
            botApiUrl = helpp.get_bot_url(groupId)
            data = net.getChatInfo(botApiUrl, groupId)
            if data is None:
                continue

            if not data:
                continue

            title = data['title']

            if 'has_visible_history' not in data or data['has_visible_history'] == False:
                net.sendMessage(botApiUrl, -1002172704826, buildMsg(groupId, title, "历史可见被关闭"))
                continue

            if 'pinned_message' not in data or not data['pinned_message']['text'].startswith("本公群规则"):
                net.sendMessage(botApiUrl, -1002172704826, buildMsg(groupId, title, "公群规则不是最新置顶"))
                continue

            content = data['pinned_message']['text']
            if "bio" in data:
                content += " " + data["bio"]
            if "description" in data:
                content += " " + data["description"]

            patten = re.compile(r"@([a-zA-Z0-9_-]+)")
            usernames = re.findall(patten, content)
            if len(usernames) > 0:
                officialNames = db.filterOfficialUserNames(usernames)
                admins = net.getChatAdmins(botApiUrl, groupId)
                for username in usernames:
                    if username not in admins and username not in officialNames:
                        net.sendMessage(botApiUrl, -1002172704826, buildMsg(groupId, title, "公群规则和简介中有非管理的用户名"))
                        break


def buildMsg(groupId, title, msg):
    text = "群号：%s\n" % groupId
    text += title + "\n\n"
    text += msg
    return text


def main():
    groupIds = db.getGroupIds()
    groupCount = len(groupIds)

    chunkCapacity = math.ceil(groupCount / thread_num)

    chunk = []
    for i in range(0, groupCount, chunkCapacity):
        chunk.append(groupIds[i:i + chunkCapacity])

    threads = []
    i = 0
    for chunkData in chunk:
        i = i + 1
        threads.append(MyThread("thread %s" % i, chunkData))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleForewarning start...")
    main()
