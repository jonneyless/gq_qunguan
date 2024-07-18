import threading
import time

from assist import get_current_time
from lib import db
from lib import db_redis


thread_num = 16


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.user_group_get()
            if item is None:
                print("%s sleep 3，%s" % (threadName, get_current_time()))
                time.sleep(3)
            else:
                # 处理用户状态的变化
                # 包含：进群，离群，禁言，踢出，上下管理，加入移除黑名单...
                try:
                    # print("group_tg_id %s user_tg_id %s, created_at %s updated_at %s, is_admin %s status_in %s status_restrict %s status_ban %s" % (item["group_tg_id"], item["user_tg_id"], item["created_at"], item["updated_at"], item["is_admin"], item["status_in"], item["status_restrict"], item["status_ban"]))
    
                    # group = db.group_id_one(item["group_tg_id"])
                    # if group is None:
                    #     print("%s not exist" % item["group_tg_id"])
                    #     continue
    
                    db.user_group_new_save(item["group_tg_id"], item["user_tg_id"], item["created_at"], item["updated_at"], item["is_admin"], item["status_in"], item["status_restrict"], item["status_ban"])

                except Exception as e:
                    print(item)
                    print(e)
                

def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleUserGroup...")
    main()
    
    