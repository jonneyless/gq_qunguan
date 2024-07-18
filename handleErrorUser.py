import threading
import time

from assist import get_current_time
from lib import db_redis
from lib import db
import helpp


thread_num = 1


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.errorUser_get()
            if item is None:
                print("%s sleep 300，%s" % (threadName, get_current_time()))
                time.sleep(300)
            else:
                if "user_tg_id" not in item and "reason" not in item and "typee" not in item:
                    continue
                    # return
                
                user_tg_id = item["user_tg_id"]
                typee = item["typee"]
                reason = item["reason"]
                
                group_tg_ids = []
                if typee == "ban":
                    group_tg_ids = db.user_group_new_to_ban(user_tg_id)
                else:
                    group_tg_ids = db.user_group_new_to_restrict(user_tg_id)
                
                print("group_tg_id_len %s, %s %s %s" % (len(group_tg_ids), user_tg_id, typee, reason))
                
                for group_tg_id in group_tg_ids:
                    ope_flag = helpp.can_ope(group_tg_id, user_tg_id)
                    if ope_flag:
                        # 可以操作
                        db_redis.tgData_error_set({
                            "typee": typee,
                            "group_tg_id": group_tg_id,
                            "user_tg_id": user_tg_id,
                            "reason": reason,
                        })
            

def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleErrorUser...")
    main()
    
    