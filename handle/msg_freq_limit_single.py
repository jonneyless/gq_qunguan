import threading

import assist
import helpp
from lib import db
from lib import db_redis

lock = threading.Lock()


def index(group_tg_id, user_tg_id, msg_tg_id, flag, created_at_timestamp, text=""):
    flag_continue = True

    if int(flag) == 2:
        current_timestamp = assist.get_current_timestamp()
        
        limit_time = helpp.get_config_limit_time() # 秒
        limit_num = helpp.get_config_limit_num()
        
        num = 0
        with lock:
            if len(text) > 0 :
                db.log_msg10_save(group_tg_id, user_tg_id, msg_tg_id, text, created_at_timestamp)
                
                msg10_status = db_redis.msg10_status_get(group_tg_id, user_tg_id)
                if msg10_status:
                    same_num = db.log_msg10_same_num(group_tg_id, user_tg_id, text)
                    print("%s %s same_num %s" % (group_tg_id, user_tg_id, same_num))
                    
                    if same_num >= 4:
                        if db_redis.temp_restrict_user_get(group_tg_id, user_tg_id):
                             print("==>10秒内禁言过这个群 %s %s" % (group_tg_id, user_tg_id))
                        else:
                            db_redis.temp_restrict_user_set(group_tg_id, user_tg_id)
                            
                            db_redis.tgData_set({
                                "typee": "restrict",
                                "group_tg_id": group_tg_id,
                                "user_tg_id": user_tg_id,
                                "reason": "10分钟内相同信息发送了 %s 次，大于等于4" % same_num,
                            })
                        
                # 只要有信息就要重新录入，重制时间的
                db_redis.msg10_status_set(group_tg_id, user_tg_id)
            

            msgs = helpp.msg_single_user_set_get(group_tg_id, user_tg_id, created_at_timestamp)
            
            for msg_created_at_timestamp in msgs:
                if int(msg_created_at_timestamp) > current_timestamp - limit_time:
                    num = num + 1
        
        if num >= limit_num:
            reason = "单个群发送信息频率限制"
            reason_temp = "%s %s %s" % (reason, group_tg_id, user_tg_id)
            print(reason_temp)
            
            db_redis.tgData_set({
                "typee": "deleteAll",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            
            if db_redis.temp_restrict_user_get(group_tg_id, user_tg_id):
                 print("==>10秒内禁言过这个群 %s %s" % (group_tg_id, user_tg_id))
            else:
                db_redis.temp_restrict_user_set(group_tg_id, user_tg_id)
                
                db_redis.tgData_set({
                    "typee": "restrict",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })
        
    return flag_continue
            