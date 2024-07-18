import threading

import assist
import helpp
import net
from lib import db
from lib import db_redis
import config


def index(callback_query_id, group_id, group_tg_id, user_tg_id, btn_message_id, info, args):
    if info == "jiechujinyan":
        if helpp.followGongqiu(user_tg_id):
            print("jiechujinyan %s %s followHwgq, cancelRestrict" % (group_tg_id, user_tg_id))
            
            db_redis.tgData_set({
                "typee": "cancelRestrict",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": "jiechujinyan",
                "until_date": -1,
            })
        else:
            tip = "点击【关注频道】按钮"
            bot_url = helpp.get_bot_url(group_tg_id, 4)
            
            print("jiechujinyan %s %s no followHwgq" % (group_tg_id, user_tg_id))
            
            net.sendAlert(bot_url, group_tg_id, user_tg_id, callback_query_id, tip)
            
            