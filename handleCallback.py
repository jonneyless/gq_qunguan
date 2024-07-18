import threading
import time

import helpp
from assist import get_current_time
from lib import db_redis
from lib import db
from handle import callback

thread_num = 4


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.callback_get()
            if item is None:
                print("%s sleep 5，%s" % (threadName, get_current_time()))
                time.sleep(5)
            else:
                # if "group_id" not in item:
                #     continue
                
                callback_query_id = item["callback_query_id"]
                group_id = item["group_id"]
                group_tg_id = item["group_tg_id"]
                user_tg_id = item["user_tg_id"]
                btn_message_id = item["btn_message_id"]
                info = item["info"]
                args = item["args"]
                
                ope_flag = helpp.can_ope(group_tg_id, user_tg_id, True)
                if ope_flag:
                    callback.index(callback_query_id, group_id, group_tg_id, user_tg_id, btn_message_id, info, args)
                

def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleCallback...")
    main()
    
    