import threading

import assist
import helpp
from lib import db
from lib import db_redis
import template
import net


def index(group_flag, group_tg_id, bot_tg_id, oper):
    oper_tg_id = oper["tg_id"]
    
    official = db.official_one(oper_tg_id)
    if official:
        print("official => group_flag %s，group_tg_id %s，bot %s, oper_tg_id %s" % (group_flag, group_tg_id, bot_tg_id, oper_tg_id))
        return
        
    official = db.official_one(bot_tg_id)
    if official:
        print("botOfficial => group_flag %s，group_tg_id %s，bot %s, oper_tg_id %s" % (group_flag, group_tg_id, bot_tg_id, oper_tg_id))
        return

    flag = False
    reason = ""
    if int(group_flag) == 2:
        white_bot = db.white_user_bot_one(bot_tg_id)
        if not white_bot:
            reason = "真公群 %s，非官方 %s 拉非白名单机器人 %s 进群" % (group_tg_id, oper_tg_id, bot_tg_id)
            flag = True
    else:
        admin = db.group_admin_one(group_tg_id, oper_tg_id)
        if not admin:
            flag = True
            reason = "游戏群 %s，非管理员 %s 拉机器人 %s 进群" % (group_tg_id, oper_tg_id, bot_tg_id)
    
    if flag:
        print("group_flag %s，group_tg_id %s，bot %s, oper_tg_id %s | %s" % (group_flag, group_tg_id, bot_tg_id, oper_tg_id, reason))
        
        db_redis.tgData_set({
            "typee": "restrict",
            "group_tg_id": group_tg_id,
            "bot_tg_id": bot_tg_id,
            "user_tg_id": bot_tg_id,
            "reason": reason,
            "until_date": -1,
        })
        db_redis.tgData_set({
            "typee": "ban",
            "group_tg_id": group_tg_id,
            "bot_tg_id": bot_tg_id,
            "user_tg_id": bot_tg_id,
            "reason": reason,
        })
    else:
        print("group_flag %s，group_tg_id %s，bot %s, oper_tg_id %s | okkk" % (group_flag, group_tg_id, bot_tg_id, oper_tg_id))
        
    
    
    