import threading

import assist
import helpp
from lib import db
from lib import db_redis


def index(group_tg_id, user_tg_id, message_tg_id, text):
    flag_continue = True
    
    # type_str
    # 1msg, 9username, 4fullname
    # 1一级限制词 2三级限制词 4二级限制词
    # 其实二级限制词4限制最大, 只有msg有二级限制词

    msg_restrict_word = helpp.has_msg_restrict_word(text)
    if msg_restrict_word is not None:
        name = msg_restrict_word["name"]
        level = int(msg_restrict_word["level"])
        
        reason = "发言内容 %s 中包含违禁词：%s" % (text[0:10], name)
        reason_temp = "%s %s %s" % (reason, group_tg_id, user_tg_id)
        print(reason_temp)
        
        if level == 1:
            db_redis.tgData_set({
                "typee": "delete",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": reason,
            })
        elif level == 4:
            db.cheat_save(user_tg_id, reason)
            
            db_redis.tgData_set({
                "typee": "deleteAll",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": reason,
            })
            db_redis.tgData_set({
                "typee": "restrict",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            flag_continue = False
        elif level == 2:
            db_redis.tgData_set({
                "typee": "deleteAll",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": reason,
            })
            db_redis.tgData_set({
                "typee": "restrict",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            flag_continue = False

    if flag_continue:
        msg_restrict_word_temp = helpp.has_msg_restrict_word_temp(text)
        if msg_restrict_word_temp is not None:
            name = msg_restrict_word_temp["name"]
    
            reason = "发言内容 %s 中包含(临时)违禁词：%s" % (text[0:10], name)
            reason_temp = "%s %s %s" % (reason, group_tg_id, user_tg_id)
            print(reason_temp)
            
            db.cheat_save(user_tg_id, reason)
            
            db_redis.tgData_set({
                "typee": "deleteAll",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": reason,
            })
            db_redis.tgData_set({
                "typee": "restrict",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            flag_continue = False
            
            db_redis.errorUser_set({
                "typee": "restrict",
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            
            

    return flag_continue
    
    