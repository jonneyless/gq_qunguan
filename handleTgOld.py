import threading
import time

from lib import db
from lib import db_redis
import net
import helpp
import math
from assist import get_current_time
from config import vip_group_tg_id, svip_group_tg_id, boss_group_tg_id, ad_group_tg_id


thread_num = 128


def delete_one(bot_url, group_tg_id, user_tg_id, message_tg_id, reason="", ope_user_tg_id=""):
    msg_tg_ids100 = []
    msg_tg_ids100.append(message_tg_id)
    
    flag, description = net.deleteMessagesWrap(bot_url, group_tg_id, msg_tg_ids100)
    for msg_tg_id in msg_tg_ids100:
        if flag:
            db.message_delete(group_tg_id, msg_tg_id)
        db.log_delete_save(group_tg_id, user_tg_id, msg_tg_id, reason, ope_user_tg_id)
            
            
def delete_all(bot_url, group_tg_id, user_tg_id, reason="", ope_user_tg_id=""):
    msg_tg_ids = db.msg48_get(group_tg_id, user_tg_id)
    msg_tg_ids_len = len(msg_tg_ids)
    if msg_tg_ids_len > 0:
        temp = 1
        temp_max = math.ceil(msg_tg_ids_len / 100)
        
        while temp <= temp_max:
            start = (temp - 1) * 100
            
            if temp < temp_max:
                msg_tg_ids100 = msg_tg_ids[start:100]
            else:
                msg_tg_ids100 = msg_tg_ids[start:]
                
            temp = temp + 1
            
            flag, description = net.deleteMessagesWrap(bot_url, group_tg_id, msg_tg_ids100)
            for msg_tg_id in msg_tg_ids100:
                if flag:
                    db.message_delete(group_tg_id, msg_tg_id)
                db.log_delete_save(group_tg_id, user_tg_id, msg_tg_id, reason, ope_user_tg_id)
    

class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            # 多监测一遍
            # 官方, 管理 不处理
            # 白名单根据情况检测
            
            data = db_redis.tgData_old_get()
            if data is None:
                # print("%s sleep 1，%s" % (threadName, get_current_time()))
                time.sleep(1)
            else:
                print(data)
                if ("typee" not in data) or ("group_tg_id" not in data) or ("user_tg_id" not in data):
                    continue
                
                typee = data["typee"]
                group_tg_id = int(data["group_tg_id"])
                user_tg_id = data["user_tg_id"]
                
                if group_tg_id == vip_group_tg_id or group_tg_id == svip_group_tg_id or group_tg_id == boss_group_tg_id or group_tg_id == ad_group_tg_id:
                    print("vip_group_tg_id don't ope")
                    continue
                
                check_white = True
                if "check_white" in data:
                    check_white = data["check_white"]
                
                ope_flag = helpp.can_ope(group_tg_id, user_tg_id, check_white)
                if not ope_flag:
                    print("%s %s can't ope" % (group_tg_id, user_tg_id))
                    continue
                
                reason = ""
                if "reason" in data:
                    reason = data["reason"]
                    
                ope_user_tg_id = -1
                if "ope_user_tg_id" in data:
                    ope_user_tg_id = data["ope_user_tg_id"]
                
                bot_url = helpp.get_bot_url(group_tg_id, 2)
                
                if typee == "ban":
                    flag, description = net.banChatMemberWrap(bot_url, group_tg_id, user_tg_id)
                    db.log_kick_save(group_tg_id, user_tg_id, reason, ope_user_tg_id)
                    if flag:
                        db.user_group_new_update(group_tg_id, user_tg_id, 2, 2, 1, 2)
                    
                elif typee == "restrict":
                    until_date = -1
                    if "until_date" in data:
                        until_date = data["until_date"]
                    db.log_restrict_save(group_tg_id, user_tg_id, until_date, reason, ope_user_tg_id)
                    flag, description = net.restrictChatMemberWrap(bot_url, group_tg_id, user_tg_id, until_date)
                    if flag:
                        db.user_group_new_update(group_tg_id, user_tg_id, 2, 1, 2, 1)
                    
                elif typee == "deleteAll":
                    # 删除所有信息
                    delete_all(bot_url, group_tg_id, user_tg_id, reason, ope_user_tg_id)
                    
                elif typee == "delete":
                    if "message_tg_id" not in data:
                        print("%s delete not message_tg_id" % group_tg_id)
                        continue
                    message_tg_id = data["message_tg_id"]
                    delete_one(bot_url, group_tg_id, user_tg_id, message_tg_id, reason, ope_user_tg_id)
                    
                    
def main():
    print("thread_num %s" % thread_num)
    print("------------------------------")
    
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("over...")


if __name__ == '__main__':
    main()
    
    