import threading
import time

import helpp
from assist import get_current_time
import assist
from config import threadNumMaps
from lib import db_redis
from lib import db


thread_num = threadNumMaps['sql']

    
class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.db_log_get()
            if item is None:
                print("%s sleep 10，%s" % (threadName, get_current_time()))
                time.sleep(10)
            else:
                sql = item["sql"]
                print(sql)
                
                db.log_save(sql)
                
                time.sleep(0.5)


def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleSql...")
    main()
    
    