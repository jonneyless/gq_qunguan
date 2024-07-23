import threading
import time

import helpp
from assist import get_current_time
from config import threadNumMaps
from lib import db_redis
from handle import danbao


thread_num = threadNumMaps['danbao']


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.danbao_get()
            if item is None:
                # print("%s sleep 3，%s" % (threadName, get_current_time()))
                time.sleep(3)
            else:
                print("%s %s %s" % (item["group_tg_id"], item["user_tg_id"], item["text"]))
                
                danbao.index(item["group_tg_id"], item["user_tg_id"], item["msg_tg_id"], item["text"], item["group"], item["created_at_timestamp"])
                
                
def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleDanbao...")
    main()
    
    