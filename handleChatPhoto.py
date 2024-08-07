import queue
import threading

import helpp
from lib import db

thread_num = 100


def Worker():
    while True:
        data = q.get()
        if data is None:
            break

        if not helpp.updateChatPhoto(data['groupId']):
            if data['retry'] < 3:
                # 上传失败就丢队列尾部重试
                data['retry'] = data['retry'] + 1
                print(str(data['groupId']) + " retry " + str(data['retry']))
                q.put(data)
            else:
                print(str(data['groupId']) + " failure ")

        q.task_done()


if __name__ == '__main__':
    q = queue.Queue()

    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=Worker)
        t.start()
        threads.append(t)

    groupIds = db.getGroupIds()
    for groupId in groupIds:
        q.put({'groupId': groupId, 'retry': 0})

    q.join()

    for i in range(thread_num):
        q.put(None)
    for t in threads:
        t.join()

    print("头像更新完毕")
