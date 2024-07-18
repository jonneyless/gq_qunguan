import threading
import time

from assist import get_current_time
from lib import db_redis
from handle import approve


thread_num = 32


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.approve_get()
            if item is None:
                print("%s sleep 6，%s" % (threadName, get_current_time()))
                time.sleep(6)
            else:
                group_tg_id = int(item["group_tg_id"])
                user_tg_id = int(item["user_tg_id"])
                group = item["group"]
                user = item["user"]
                
                approve.index(group_tg_id, user_tg_id, group, user)
                
def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleApprove...")
    main()
    
    