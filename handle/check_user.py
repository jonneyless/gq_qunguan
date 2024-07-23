import assist
import helpp
import net
import template
from lib import db
from lib import db_redis


def index(group_tg_id, user_tg_id, user, say=False, message_tg_id=-1):
    flag_continue = True
    
    username = ""
    fullname = ""
    if user is not None:
        if "username" in user:
            username = user["username"]
        if "fullname" in user:
            fullname = user["fullname"]
    
    is_cheat_special = db.cheats_special_one(user_tg_id)
    if is_cheat_special:
        print("cheat_special %s %s %s %s | %s" % (group_tg_id, user_tg_id, fullname, username, say))
        
        db_redis.tgData_set({
            "typee": "ban",
            "group_tg_id": group_tg_id,
            "user_tg_id": user_tg_id,
            "reason": "骗子库",
        })
        if say:
            db_redis.tgData_set({
                "typee": "deleteAll",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": "骗子库",
            })
            
        flag_continue = False
    
    if flag_continue:
        is_cheat = db.cheat_one(user_tg_id)
        if is_cheat:
            print("cheat %s %s %s %s | %s" % (group_tg_id, user_tg_id, fullname, username, say))
            
            restrict_timestamp = assist.get_restrict_time(180) # 禁言180天
            db_redis.tgData_set({
                "typee": "restrict",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": "黑名单",
                "until_date": restrict_timestamp,
            })
            if say:
                db_redis.tgData_set({
                    "typee": "deleteAll",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "message_tg_id": message_tg_id,
                    "reason": "黑名单",
                })
                
            flag_continue = False
            
    if flag_continue:
        fullname_restrict_word = helpp.has_fullname_restrict_word(fullname)
        if fullname_restrict_word is not None:
            name = fullname_restrict_word["name"]
            level = int(fullname_restrict_word["level"])
            reason = "昵称中包含敏感词：%s" % name
            
            db.cheat_save(user_tg_id, reason)
            
            print("fullname_restrict_word %s %s %s %s,%s | %s" % (group_tg_id, user_tg_id, fullname, name, level, say))
            
            if level == 1:
                restrict_timestamp = assist.get_restrict_time(180) # 禁言180天
                db_redis.tgData_set({
                    "typee": "restrict",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                    "until_date": restrict_timestamp,
                })
            else:
                db_redis.tgData_set({
                    "typee": "ban",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })
                
            if say:
                db_redis.tgData_set({
                    "typee": "deleteAll",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "message_tg_id": message_tg_id,
                    "reason": reason,
                })
                
            flag_continue = False
    
    if flag_continue:
        username_restrict_word = helpp.has_username_restrict_word(username)
        if username_restrict_word is not None:
            name = username_restrict_word["name"]
            level = int(username_restrict_word["level"])
            reason = "用户名中包含敏感词：%s" % name
            
            db.cheat_save(user_tg_id, reason)
            
            print("username_restrict_word %s %s %s %s,%s | %s" % (group_tg_id, user_tg_id, username, name, level, say))
            
            if level == 1:
                restrict_timestamp = assist.get_restrict_time(180) # 禁言180天
                db_redis.tgData_set({
                    "typee": "restrict",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                    "until_date": restrict_timestamp,
                })
            else:
                db_redis.tgData_set({
                    "typee": "ban",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })
                
            if say:
                db_redis.tgData_set({
                    "typee": "deleteAll",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "message_tg_id": message_tg_id,
                    "reason": reason,
                })

            flag_continue = False

    if flag_continue:
        bot_url = helpp.get_bot_url(group_tg_id, 1, True)
        intro = net.getBio(bot_url, user_tg_id)
        intro_restrict_word = helpp.has_intro_restrict_word(intro)
        if intro_restrict_word is not None:
            name = intro_restrict_word["name"]
            level = int(intro_restrict_word["level"])
            reason = "用户简介中包含敏感词：%s" % name

            db.cheat_save(user_tg_id, reason)

            print("intro_restrict_word %s %s %s %s,%s | %s" % (group_tg_id, user_tg_id, username, name, level, say))

            if level == 1:
                restrict_timestamp = assist.get_restrict_time(180)  # 禁言180天
                db_redis.tgData_set({
                    "typee": "restrict",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                    "until_date": restrict_timestamp,
                })
            else:
                db_redis.tgData_set({
                    "typee": "ban",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })

            if say:
                db_redis.tgData_set({
                    "typee": "deleteAll",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "message_tg_id": message_tg_id,
                    "reason": reason,
                })

            flag_continue = False
       
    if flag_continue:
        if fullname.find("汇旺") >= 0:
            reason = "昵称中包含汇旺 %s %s %s" % (group_tg_id, user_tg_id, fullname)
            print(reason)
 
            db_redis.tgData_set({
                "typee": "ban",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            if say:
                db_redis.tgData_set({
                    "typee": "deleteAll",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "message_tg_id": message_tg_id,
                    "reason": reason,
                })

            bot_url = helpp.get_bot_url(group_tg_id, 1)
            
            net.sendMessageOne(bot_url, group_tg_id, template.msg_send_has_huiwang(user))
            
            flag_continue = False
      
    if flag_continue:
        if len(fullname) > 0:
            group_admin_like = helpp.like_admin(group_tg_id, user)
            if group_admin_like:
                reason = "用户昵称 %s 和群内管理员相似，%s %s" % (fullname, group_tg_id, user_tg_id)
                print(reason)
                
                db_redis.tgData_set({
                    "typee": "ban",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })
                if say:
                    db_redis.tgData_set({
                        "typee": "deleteAll",
                        "group_tg_id": group_tg_id,
                        "user_tg_id": user_tg_id,
                        "message_tg_id": message_tg_id,
                        "reason": reason,
                    })
                    
                db.cheat_save(user_tg_id, reason)
                
                flag_continue = False
        
        
    return flag_continue
    
    
    