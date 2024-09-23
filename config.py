from environs import Env

env = Env()
env.read_env()

official_bot_tg_ids = [
    2094467068, # qunguan
    5928074822, # 报备
    6245957008, # qunguan备用
]

# ----------------------------------------------------------------------------------------------------------------------

mysqlInfo = {
    "host": env.str("DB_HOST", "127.0.0.1"),
    "db": env.str("DB_DATABASE", "welcome"),
    "user": env.str("DB_USER", "root"),
    "passwd": env.str("DB_PASS", "7a89afd87c0cd015"),
    "port": env.int("DB_PORT", 3306),
}

redisInfo = {
    "host": env.str("REDIS_HOST", "127.0.0.1"),
    "port": env.int("REDIS_PORT", 6379),
}

# ----------------------------------------------------------------------------------------------------------------------

qunguan_bot_url = "https://api.telegram.org/bot"+env.str("QG_BOT_TOKEN", "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")+"/"
qunguan_tg_id = env.int("QG_BOT_TG_ID", 5759299188)

qunguan_back_bot_url = "https://api.telegram.org/bot"+env.str("QG_BACK_BOT_TOKEN", "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")+"/"
qunguan_back_tg_id = env.int("QG_BACK_BOT_TG_ID", 5759299188)

chat_photo_path = env.str("CHAT_PHOTO_PATH", "chat_photo.jpg")
admin_url = env.str("ADMIN_URL", "http://jony.fsa2.xyz/")

# ----------------------------------------------------------------------------------------------------------------------

limit_time = 1
limit_num = 20

# ----------------------------------------------------------------------------------------------------------------------

vip_group_tg_id = -1001753191368
svip_group_tg_id = -1001601629727
boss_group_tg_id = -1001620186906
ad_group_tg_id = -1001660660101

# ----------------------------------------------------------------------------------------------------------------------

official_channels = [
    "-1001624139937", # hwgq
    "-1001082308171", # gongqiu
    "-1001559203927", # daqun
    "-1001015370323", # kefu
    
    "-1001734975520", # hwgq789
    "-1001423653727", # gongqiu8
    "-1001176689162", # biz
]

# ----------------------------------------------------------------------------------------------------------------------

business_detail_types_no_limit = [
    # vip公群、待定默认、资源群
    700, # vip小公群
    701, # VIP代收类
    702, # VIP承兑类
    703, # VIP收u代付类
    1, # 待定默认
    1000, # 资源群
]

# ----------------------------------------------------------------------------------------------------------------------

limit_all_time = 60
limit_all_group_num = 10
limit_cancel_restrict = 365  # 天

# ----------------------------------------------------------------------------------------------------------------------

limit_text_len = 120
limit_text_len_bank = 400

# ----------------------------------------------------------------------------------------------------------------------

photo_limit_type_num = 3
photo_limit_time = 20
photo_limit_day = 10


limit_no_vip_restrict_time = 7
limit_no_vip_num = 20
limit_no_vip_type = 3
limit_no_vip_time = 300

threadNumMaps = {
    'approve': env.int("THREAD_NUM_APPROVE", 32),
    'callback': env.int("THREAD_NUM_CALLBACK", 4),
    'command': env.int("THREAD_NUM_COMMAND", 1),
    'danbao': env.int("THREAD_NUM_DANBAO", 1),
    'errorUser': env.int("THREAD_NUM_ERROR_USER", 1),
    'msg': env.int("THREAD_NUM_MSG", 1),
    'msg48': env.int("THREAD_NUM_MSG48", 2),
    'sj': env.int("THREAD_NUM_SJ", 1),
    'sql': env.int("THREAD_NUM_SQL", 1),
    'tg': env.int("THREAD_NUM_TG", 2),
    'tgError': env.int("THREAD_NUM_TG_ERROR", 2),
    'tgOld': env.int("THREAD_NUM_TG_OLD", 128),
    'tgTest': env.int("THREAD_NUM_TG_TEST", 1),
    'user': env.int("THREAD_NUM_USER", 1),
    'userGroup': env.int("THREAD_NUM_USER_GROUP", 16),
    'userIn': env.int("THREAD_NUM_USER_IN", 8),
    'userSpecial': env.int("THREAD_NUM_USER_SPECIAL", 1),
    'forewarning': env.int("THREAD_NUM_FOREWARNING", 1),
    'keyword': env.int("THREAD_KEYWORD", 1),
}
