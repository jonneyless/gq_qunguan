import threading
import time

import helpp
from assist import get_current_time
from lib import db_redis
from handle import command, danbao


thread_num = 1


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.command_get()
            if item is None:
                # print("%s sleep 1，%s" % (threadName, get_current_time()))
                time.sleep(1)
            else:
                # print(item)
                
                print("%s %s %s" % (item["group_tg_id"], item["user_tg_id"], item["text"]))
                
                if item["text"] == "担保开启":
                    pass
                    # danbao.index(item["group_tg_id"], item["user_tg_id"], item["msg_tg_id"], item["text"], item["group"], item["created_at_timestamp"])
                else:
                    command.index(item["group_tg_id"], item["user_tg_id"], item["msg_tg_id"], item["text"], item["group"], 
                        item["reply_message_tg_id"], item["reply_user_tg_id"], item["reply_text"],
                        item["entity_usernames"], item["entity_user_tg_ids"],
                        item["created_at_timestamp"]
                    )
                
                
def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleCommand...")
    main()
    
    