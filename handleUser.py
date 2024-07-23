import threading
import time

from assist import get_current_time
from lib import db
from lib import db_redis
import helpp
from config import official_bot_tg_ids, threadNumMaps
from handle import check_user, check_new_bot, xianjing


thread_num = threadNumMaps['user']


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.user_get()
            if item is None:
                # print("%s sleep 3，%s" % (threadName, get_current_time()))
                time.sleep(3)
            else:
                # print(item)
                
                group_tg_id = item["group_tg_id"]
                user_tg_id = item["user_tg_id"]
                
                group = None
                if "group" in item:
                    group = item["group"]
                
                if int(user_tg_id) in official_bot_tg_ids:
                    print("hwdb %s" % user_tg_id)
                    continue
                
                # if "invite_link" in item:
                #     # 有链接肯定是进群，但是没有链接的有进群的，直接拉进群
                #     invite_link = item["invite_link"]
                    
                #     oper = None
                #     if "oper" in item:
                #         oper = item["oper"]
                        
                #     db.log_invite_link_save(group_tg_id, user_tg_id, invite_link, oper)
                # else:
                #     print("no invite_link %s" % item)
                
                group_flag = int(item["group_flag"])
                
                if "newer_is_bot" in item and "oper" in item:
                    check_new_bot.index(group_flag, group_tg_id, user_tg_id, item["oper"])
                    
                ope_flag = helpp.can_ope(group_tg_id, user_tg_id, True)
                if ope_flag:
                    if "in" in item:
                        xianjing.index(group_tg_id, user_tg_id, item)
                    
                    if group_flag == 2 and "in" in item:
                        flag_continue = check_user.index(group_tg_id, user_tg_id, item, False)
                else:
                    print("no ope %s %s" % (group_tg_id, user_tg_id))
                
                db.user_save(user_tg_id, item["username"], item["fullname"], item["firstname"], item["lastname"])
                
                
def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleUser...")
    main()
    
    