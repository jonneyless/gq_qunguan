import threading
import time

from assist import get_current_time
from lib import db
from lib import db_redis
import helpp
from config import official_bot_tg_ids, threadNumMaps
import net


thread_num = threadNumMaps['userIn']


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.user_in_get()
            if item is None:
                print("%s sleep 3，%s" % (threadName, get_current_time()))
                time.sleep(3)
            else:
                group_tg_id = item["group_tg_id"]
                user_tg_id = item["user_tg_id"]
                username = item["username"]
                fullname = item["fullname"]
                
                # handleUser 里已判断过是否能操作了
                
                # 非骗子，非黑名单，昵称用户名正常的客服
                # 检测是否关注了 hwgq, gongqiu, kefu
                
                flag = helpp.followDbAll(user_tg_id)
                
                print("%s %s %s %s, followDbAll %s\n\n" % (group_tg_id, user_tg_id, username, fullname, flag))
                
                if not flag:
                    db_redis.tgData_set({
                        "typee": "restrict",
                        "group_tg_id": group_tg_id,
                        "user_tg_id": user_tg_id,
                        "reason": "新用户进群，没有关注所有：hwgq, gongqiu, kefu",
                        "until_date": -1,
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
    print("handleUserIn...")
    main()
    
    