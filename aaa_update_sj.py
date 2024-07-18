import threading
import time

from lib import db
import net
import helpp
from assist import get_current_time
import assist
import math


thread_num = 8


def get_has_trade(group_tg_id, title, start_at, end_at):
    status = net.checkJzHaveData(group_tg_id, start_at, end_at)
    if status == 0:
        return 2, 6
    elif status == 1:
        return 1, 101
    elif status == 2:
        return 1, 100
    elif status == 9:
        return 1, 300
        
    return 2, 5
    
    
def get_is_active(group_tg_id, title, start_at, end_at):
    obj = db.sj_user_say_one(group_tg_id, start_at, end_at)
    if obj is not None:
        return 1
        
    return 2


def get_active_level(group_tg_id, start_at, end_at):
    active_level = 1
    
    msgs = db.msg_get(group_tg_id, start_at, end_at)
    
    if len(msgs) > 20:
        active_level = 3
    else:
        active_level = 2
        
    return active_level
    
    
class MyThread(threading.Thread):
    def __init__(self, threadName, groups, start_at, end_at):
        super(MyThread, self).__init__()
        self.threadName = threadName
        self.groups = groups
        self.start_at = start_at
        self.end_at = end_at

    def run(self):
        threadName = self.threadName
        groups = self.groups
        start_at = self.start_at
        end_at = self.end_at
        
        num = 0
        groups_len = len(groups)
        for group in groups:
            num = num + 1
            print("%s / %s" % (num, groups_len))
            
            data_id = group["id"]
            group_tg_id = group["group_tg_id"]
            title = group["title_new"]
            
            has_trade, trade_type = get_has_trade(group_tg_id, title, start_at, end_at)
            is_active = get_is_active(group_tg_id, title, start_at, end_at)
            
            jiaoyi_obj = db.jiaoyi_one(group_tg_id)
            shenji_obj = db.shenji_one(group_tg_id)
            
            jiaoyi_text = ""
            shenji_text = ""
            
            if jiaoyi_obj is not None:
                jiaoyi_text = "%s %s" % (jiaoyi_obj["fullname"], jiaoyi_obj["username"])
            
            if shenji_obj is not None:
                shenji_text = "%s %s" % (shenji_obj["fullname"], shenji_obj["username"])
            
            active_level = 1
            if is_active == 1:
                active_level = get_active_level(group_tg_id, start_at, end_at)
            
            db.sj_group_yajin_over(data_id, is_active, has_trade, trade_type, jiaoyi_text, shenji_text, active_level)
            
            print("%s %s %s, %s, active_level %s" % (title, has_trade, is_active, trade_type, active_level))
            

def main(groups, start_at, end_at):
    groups_len = len(groups)
    single_len = math.ceil(groups_len / thread_num)
    
    arr = []
    arr_temp = []
    
    for group in groups:
        if len(arr_temp) < single_len:
            arr_temp.append(group)
        else:
            arr.append(arr_temp)

            arr_temp = []
            arr_temp.append(group)
            
    if len(arr_temp) > 0:
        arr.append(arr_temp)

    arr_len = len(arr)
    
    print("thread_num %s" % arr_len)
    print("------------------------------")
    
    threads = []
    for i in range(arr_len):
        threads.append(MyThread("thread %s" % i, arr[i], start_at, end_at))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("over...")
    
    
if __name__ == '__main__':
    start = assist.get_current_timestamp()
    
    start_at = assist.get_yesterday_time6()
    end_at = assist.get_today_time6()

    groups = db.sj_group_yajin_all(start_at, end_at)
    
    main(groups, start_at, end_at)
    
    end = assist.get_current_timestamp()
    
    print("spend %s" % (end - start))
    
    