import threading

import assist
import helpp
from lib import db
from lib import db_redis
import template
import net


def index(group_tg_id, user_tg_id, item):
    group = None
    if "group" in item:
        group = item["group"]
    
    if group is None:
        return
    
    xianjing_status = -1
    if "xianjing_status" in group:
        xianjing_status = int(group["xianjing_status"])
    
    print("%s xianjing_status %s" % (group_tg_id, xianjing_status))
    
    if xianjing_status != 1:
        return
    
    config_xianjing_status = helpp.get_config_xianjing_status()
    
    print("%s config_xianjing_status %s" % (group_tg_id, config_xianjing_status))
    
    if config_xianjing_status != 1:
        return
    
    config_xianjing_time = helpp.get_config_xianjing_time()
    config_xianjing_num = helpp.get_config_xianjing_num()
    
    print("%s %s" % (config_xianjing_time, config_xianjing_num))
    
    db.log_xianjing_in_save(group_tg_id, user_tg_id)
    
    now = assist.get_current_timestamp()
    created_at = assist.timestamp2time(now - config_xianjing_time * 3600)
    created_at_timestamp_15 = now - 86400 * 15
    
    num = db.log_xianjing_in_num(user_tg_id, created_at)
    if num >= config_xianjing_num:
        user_group = db.user_group_new_single(user_tg_id)
        if user_group is not None and user_group["created_at"] is not None:
            created_at = str(user_group["created_at"])
            
            print("%s %s %s" % (group_tg_id, user_tg_id, created_at))
            
            created_at_timestamp = assist.time2timestamp(created_at)
            if created_at_timestamp < created_at_timestamp_15:
                # 入群时间很早，15天以前，不处理了。
                print("%s %s %s old user" % (group_tg_id, user_tg_id, created_at))
                
                return
            
            # 确定异常了
            reason = "陷阱模式：%s 小时内进了 %s 个陷阱群" % (config_xianjing_time, config_xianjing_num)
            
            print(reason)
            
            db_redis.tgData_set({
                "typee": "restrict",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
                "until_date": -1,
            })
            db_redis.errorUser_set({
                "typee": "restrict",
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            
            db.cheat_save(user_tg_id, reason)
            