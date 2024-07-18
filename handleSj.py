import threading
import time

import helpp
from assist import get_current_time
import assist
from lib import db_redis
from lib import db


thread_num = 1


def get_start_end(created_at_timestamp):
    today = assist.get_today_timestamp()
    
    start_at = assist.get_today_time6()
    end_at = assist.get_tommorrow_time6()
    
    if created_at_timestamp > today:
        if created_at_timestamp - today < 3600 * 6:
            # 0点-6点
            start_at = assist.get_yesterday_time6()
            end_at = assist.get_today_time6()
        else:
            pass
    else:
        # 昨日0点前的数据,
        start_at = assist.get_yesterday_time6()
        end_at = assist.get_today_time6()
        
    return start_at, end_at
    

def handleTitle(item):
    group_tg_id = item["group_tg_id"]
    title_new = item["title_new"]
    created_at = item["created_at"]
    created_at_timestamp = int(item["created_at_timestamp"])
    business_detail_type = -1
    
    if not assist.has_yajin(title_new):
        print("%s, title_new %s no yajin" % (group_tg_id, title_new))
        return
    
    start_at, end_at = get_start_end(created_at_timestamp)
    
    obj = db.sj_group_yajin_one(group_tg_id, start_at, end_at)
    if obj is None:
        print("%s, new %s" % (group_tg_id, title_new))
        db.sj_group_yajin_save(group_tg_id, title_new, title_new, created_at, business_detail_type)
    else:
        if title_new != obj["title_new"]:
            print("%s, title_old %s, title_new %s" % (group_tg_id, obj["title_new"], title_new))
            db.sj_group_yajin_update(obj["id"], obj["title_new"], title_new, created_at, business_detail_type)
        else:
            print("%s, same title %s" % (group_tg_id, title_new))
    
    
def handleMsg(item):
    group_tg_id = item["group_tg_id"]
    user_tg_id = item["user_tg_id"]
    text = item["text"]
    created_at = item["created_at"]
    created_at_timestamp = int(item["created_at_timestamp"])
    
    start_at, end_at = get_start_end(created_at_timestamp)
    
    if db.official_one(user_tg_id):
        pass
    else:
        obj = db.sj_user_say_one(group_tg_id, start_at, end_at)
        if obj is None:
            print("sj_user_say %s %s %s" % (group_tg_id, user_tg_id, created_at))
            db.sj_user_say_save(group_tg_id, user_tg_id, created_at)
        else:
            pass
            # print("sj_user_say has %s" % group_tg_id)
    

class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.sj_msg_get()
            if item is None:
                print("%s sleep 10，%s" % (threadName, get_current_time()))
                time.sleep(10)
            else:
                # print(item)
                
                if "text" in item:
                    handleMsg(item)
                elif "title_new" in item:
                    handleTitle(item)


def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleSj...")
    main()
    
    