import helpp
from lib import db
from lib import db_redis
from assist import get_current_timestamp, time2timestamp, handle_text
from config import qunguan_bot_url, qunguan_back_bot_url, limit_time, limit_num, vip_group_tg_id, svip_group_tg_id, official_channels
import config
import httpp
import net
import re
import assist

now = assist.get_current_timestamp()
print(assist.timestamp2time(now - 60 * 10))



print("test...")

# config_xianjing_time = helpp.get_config_xianjing_time()

# now = assist.get_current_timestamp()
# created_at = assist.timestamp2time(now - config_xianjing_time * 3600)

# print(created_at)

# print(helpp.get_config_xianjing_num())

# print("aaa")

# print(helpp.followDbAll("1890717643"))


# def get_btns():
#     btns_temp = [
#         [
#             {
#                 "text": "关注频道",
#                 "url": "https://t.me/gongqiu",
#             },
#             {
#                 "text": "解除禁言",
#                 "callback_data": "jiechujinyan",
#             },
#         ]
#     ]
    
#     btn = {
#         "inline_keyboard": btns_temp
#     }
    
#     return btn


# db_redis.tgData_set({
#     "typee": "sendSpecialWelcome",
#     "group_tg_id": "-1001919593910",
#     "user_tg_id": -1,
#     "text": "关注 @gongqiu 后，点击下方按钮自动解除禁言",
#     "btns": get_btns()
# })


# group_tg_id = "-1001885709812"
# bot_url = helpp.get_bot_url(group_tg_id, 1, True)
# print(bot_url)

# official = db.official_one("1473353726")
# print(official)


# groups = helpp.get_groups_all()
# for group in groups:
#     print(group)
#     continue

# title_old = "公群 50001 已押1U"
# pattern = re.compile("公群(\d*)")
# result = re.search(pattern, title_old)
# if result is not None:
#     print(result.group(1))
#     num_old = int(result.group(1))
#     print(num_old)
    

# flag_jz = net.removeNotOfficialAdmin("-1001846199438")
# print(flag_jz)



# def get_bot_url_default():
#     return qunguan_bot_url
    
    
# def get_bot_url_default_back():
#     return qunguan_back_bot_url
    

# group_tg_id = -1001859025094	
# typee = 4

# bot_url = helpp.get_bot_url(group_tg_id, 1, True)
# print(bot_url)

# bot_url = db_redis.bot_url_get(group_tg_id, typee)

# print(bot_url)

# if bot_url is None:
#     bot_url = get_bot_url_default()

    
#     bot = db.bot_one(group_tg_id, typee)
#     if bot is None:
#         pass
#         # return bot_url
        
#     token = bot["token"]
#     bot_url = "https://api.telegram.org/bot%s/" % token
    
#     print(bot_url)
    
#     db_redis.bot_url_set(group_tg_id, typee, bot_url)



    

# bot = db.bot_one(chat_id, 4)
# print(bot)

# print(helpp.get_bot_url(chat_id, 2))

# limit_no_vip_restrict_time = helpp.get_config_limit_no_vip_restrict_time()
# limit_no_vip_num = helpp.get_config_limit_no_vip_num()
# limit_no_vip_type = helpp.get_config_limit_no_vip_type()
# limit_no_vip_time = helpp.get_config_limit_no_vip_time()

# print("limit_no_vip_time %s" % limit_no_vip_restrict_time)
# print("limit_no_vip_num %s" % limit_no_vip_num)
# print("limit_no_vip_type %s" % limit_no_vip_type)
# print("limit_no_vip_time %s" % limit_no_vip_time)
