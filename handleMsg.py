import threading
import time

import helpp
from assist import get_current_time
from lib import db_redis
from lib import db
from handle import check_msg_word, check_user, msg_other


thread_num = 1


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.msg_get()
            if item is None:
                # print("%s sleep 1，%s" % (threadName, get_current_time()))
                time.sleep(6)
            else:
                
                group_tg_id = item["group_tg_id"]
                user_tg_id = item["user_tg_id"]
                msg_tg_id = item["msg_tg_id"]
                info = item["text"]
                created_at = item["created_at"]
                
                db.log_msg48_save(group_tg_id, user_tg_id, msg_tg_id, created_at)
                db.message_save(group_tg_id, user_tg_id, msg_tg_id, info, created_at)
                
                if len(info) > 20:
                    if info.find("t") >= 0 or info.find("T") >= 0:
                        title = ""
                        username = ""
                        fullname = ""
                        if "title" in item:
                            title = item["title"]
                        if "username" in item:
                            username = item["username"]
                        if "fullname" in item:
                            fullname = item["fullname"]
                        
                        db.log_msg_address_save(title, group_tg_id, user_tg_id, username, fullname, msg_tg_id, info, created_at)

                user = None
                if "user" in item:
                    user = item["user"]

                ope_flag = helpp.can_ope(group_tg_id, user_tg_id, True)
                if not ope_flag:
                    print("%s %s can't ope" % (group_tg_id, user_tg_id))
                    continue
                
                flag_continue = check_user.index(group_tg_id, user_tg_id, user, True, msg_tg_id)
                if flag_continue:
                    flag_continue = check_msg_word.index(group_tg_id, user_tg_id, msg_tg_id, info)
                
                if flag_continue:
                    hasChinese = 2
                    forward_from = 2
                    has_hide_link = 2   
                    
                    if "hasChinese" in item:
                        hasChinese = int(item["hasChinese"])
                    if user is not None:
                        if "hasChinese" in user:
                            hasChinese = int(user["hasChinese"])
                        
                    if "forward_from" in item:
                        forward_from = int(item["forward_from"])    
                    if "has_hide_link" in item:
                        has_hide_link = int(item["has_hide_link"])
                    
                    flag = item["flag"]
                    trade_type = item["trade_type"]
                    
                    msg_other.index(group_tg_id, user_tg_id, msg_tg_id, user, info, hasChinese, forward_from, has_hide_link, flag, trade_type)
                
                # try:
                #     print(item)
                    

                    
                        
                # except Exception as e:
                #     print(item)
                #     print(e)
                

def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleMsg...")
    main()
    
    