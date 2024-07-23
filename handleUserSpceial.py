import threading
import time

from assist import get_current_time
from config import threadNumMaps
from lib import db
from lib import db_redis
import helpp
import net


thread_num = threadNumMaps['userSpecial']


def get_btns():
    btns_temp = [
        [
            {
                "text": "关注频道",
                "url": "https://t.me/gongqiu",
            },
            {
                "text": "解除禁言",
                "callback_data": "jiechujinyan",
            },
        ]
    ]
    
    btn = {
        "inline_keyboard": btns_temp
    }
    
    return btn
    

class MyThread(threading.Thread):
    def __init__(self, threadName):
        super(MyThread, self).__init__()
        self.threadName = threadName

    def run(self):
        threadName = self.threadName

        while True:
            item = db_redis.user_special_get()
            if item is None:
                pass
            else:
                print(item)
                
                group_tg_id = item["group_tg_id"]
                user = item["from"]
                is_new = int(item["is_new"])
                
                user_tg_id = user["tg_id"]
                username = user["username"]
                fullname = user["fullname"]
                
                ope_flag = helpp.can_ope(group_tg_id, user_tg_id, True)
                
                print("%s %s" % (user_tg_id, ope_flag))
                
                if ope_flag:
                    if is_new == 1:
                        print("sendSpecialWelcome %s" % db_redis.special_welcome_get(group_tg_id))
                        
                        if not db_redis.special_welcome_get(group_tg_id):
                            db_redis.special_welcome_set(group_tg_id)
                            db_redis.tgData_set({
                                "typee": "sendSpecialWelcome",
                                "group_tg_id": group_tg_id,
                                "user_tg_id": user_tg_id,
                                "text": "关注 @gongqiu 后，点击下方按钮自动解除禁言",
                                "btns": get_btns()
                            })
                        
                        flag = helpp.followGongqiu(user_tg_id)
                        
                        print("in %s %s %s" % (group_tg_id, user_tg_id, flag))
                        
                        if flag:
                            continue
                        else:
                            db_redis.tgData_set({
                                "typee": "restrict",
                                "group_tg_id": group_tg_id,
                                "user_tg_id": user_tg_id,
                                "reason": "特殊群组未关注 @gongqiu频道。",
                                "until_date": -1,
                            })
                    else:
                        # flag_redis = db_redis.check_follow_get(user_tg_id)
                        # if flag_redis is not None:
                        #     if flag_redis == 1:
                        #         continue
                            
                        flag = helpp.followGongqiu(user_tg_id)
                        
                        print("say %s %s %s" % (group_tg_id, user_tg_id, flag))
                        
                        if flag:
                            db_redis.check_follow_set(user_tg_id, 1)
                        else:
                            db_redis.check_follow_set(user_tg_id, 2)
                            
                            db_redis.tgData_set({
                                "typee": "restrict",
                                "group_tg_id": group_tg_id,
                                "user_tg_id": user_tg_id,
                                "reason": "特殊群组未关注 @gongqiu频道。",
                                "until_date": -1,
                            })
                else:
                    print("%s ..." % user_tg_id)
                        
                        
def main():
    threads = []
    for i in range(thread_num):
        threads.append(MyThread("thread %s" % i))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("handleUserSpecial...")
    main()
    
    