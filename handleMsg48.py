import threading
import time

from assist import get_current_time
from config import threadNumMaps
from lib import db
from lib import db_redis
import helpp
from handle import msg_freq_limit, msg_freq_limit_single


thread_num = threadNumMaps['msg48']


class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

# 录入数据 msg msg48
# 监测频率相关
# 信息监测相关
# 用户名昵称相关

# 这里因为有线程锁相关的操作，为了加快速度，只做频率相关的内容，删除的时候只通知删除，

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.msg48_get()
            if item is None:
                # print("%s sleep 1，%s" % (threadName, get_current_time()))
                time.sleep(1)
            else:
                user_tg_id = item["user_tg_id"]
                
                flag = -1
                if "flag" in item:
                    flag = item["flag"]
                business_detail_type = -1
                if "business_detail_type" in item:
                    business_detail_type = item["business_detail_type"]
                has_at = 2
                if "has_at" in item:
                    has_at = item["has_at"]
                fullname_is_en = 2
                if "fullname_is_en" in item:
                    fullname_is_en = item["fullname_is_en"]
                    
                is_photo = 2
                is_video = 2
                if "is_photo" in item:
                    is_photo = int(item["is_photo"])
                if "is_video" in item:
                    is_video = int(item["is_video"])
            
                group_tg_id = item["group_tg_id"]
                msg_tg_id = item["msg_tg_id"]
                created_at = item["created_at"]
                created_at_timestamp = item["created_at_timestamp"]
                    
                # db.log_msg48_save(group_tg_id, user_tg_id, msg_tg_id, created_at)
                
                is_cheat = db.cheat_one(user_tg_id)
                if is_cheat:
                    print("==>黑名单用户不参与频率判断，在handleMsg里直接禁言+删除全部，%s %s" % (group_tg_id, user_tg_id))
                    continue
                
                ope_flag = helpp.can_ope(group_tg_id, user_tg_id, True)
                if not ope_flag:
                    # print("%s %s can't ope" % (group_tg_id, user_tg_id))
                    continue
                
                text = ""
                if "text" in item:
                    text = item["text"]
                
                flag_continue = msg_freq_limit_single.index(group_tg_id, user_tg_id, msg_tg_id, flag, created_at_timestamp, text)
                flag_continue = msg_freq_limit.index(group_tg_id, user_tg_id, flag, business_detail_type, created_at_timestamp, has_at, fullname_is_en, is_photo, is_video)
                
                # try:

                    
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
    print("handleMsg48...")
    main()
    
    