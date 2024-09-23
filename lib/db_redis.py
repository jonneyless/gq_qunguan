import datetime
import json
import time

import redis

from config import redisInfo
from lib import db

pool = redis.ConnectionPool(host=redisInfo["host"], port=redisInfo["port"], db=10)
pool2 = redis.ConnectionPool(host=redisInfo["host"], port=redisInfo["port"], db=2)

prefix = "qunguan_test"
prefix_handleUser = "handleUserqq"


# ======================================================================================================================

def get_conn():
    return redis.Redis(connection_pool=pool)


def get_conn2():
    return redis.Redis(connection_pool=pool2)
    
    
# ----------------------------------------------------------------------------------------------------------------------

def db_log_set(data):
    key = prefix + "db_log_qq"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def db_log_get():
    key = prefix + "db_log_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def callback_get():
    key = "saveCallback_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        

def tgData_error_set(data):
    key = prefix + "TgData_error_qq"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def tgData_error_get():
    key = prefix + "TgData_error_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        

def test_tgData_set(data):
    key = prefix + "TgData_qq_test"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def test_tgData_get():
    key = prefix + "TgData_qq_test"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def tgData_old_set(data):
    key = prefix + "TgData_qq_new"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def tgData_old_get():
    key = prefix + "TgData_qq_new"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def tgData_set(data):
    # key = prefix + "TgData_qq_new"
    key = prefix + "TgData_qq"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def tgData_get():
    key = prefix + "TgData_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def user_get():
    key = "changeUserNew_qq"

    conn = get_conn()
    
    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)


def user_special_get():
    key = "changeUserNewSpecial_qq"

    conn = get_conn()
    
    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def user_in_set(data):
    key = prefix + "user_in_qq"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def user_in_get():
    key = prefix + "user_in_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def user_group_get():
    key = "changeUserGroupNew_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def msg48_get():
    key = "saveMsg48_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def msg_get():
    key = "saveMsg_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def sj_msg_set(data):
    key = "saveSjMsg_qq"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
    
    
def sj_msg_get():
    key = "saveSjMsg_qq"

    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def test_msg_get():
    key = "test_saveMsg_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def approve_get():
    key = "saveApprove_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)


def bio_get(userTgId):
    key = "user:bio:" + str(userTgId)

    conn = get_conn()

    data = conn.get(key)
    if data is None:
        return None
    else:
        return json.loads(data)

def bio_set(userTgId, bio):
    key = "user:bio:" + str(userTgId)

    conn = get_conn()

    conn.set(key, json.dumps(bio), ex=600)
        
        
def errorUser_get():
    key = "qunguanErrorUser"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def errorUser_set(data):
    key = "qunguanErrorUser"

    conn = get_conn()

    conn.rpush(key, json.dumps(data))
        
        
def command_get():
    key = "saveCommand_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def danbao_get():
    key = "saveDanbao_qq"
    
    conn = get_conn()

    data = conn.lpop(key)
    if data is None:
        return None
    else:
        return json.loads(data)
        
        
def data_len(key):
    conn = get_conn()
    
    return conn.llen(key)
    
    
# ----------------------------------------------------------------------------------------------------------------------

# 用户基本信息
# fullname
# username

def user_info_get(user_tg_id):
    key = prefix_handleUser + "user_info" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def user_info_set(user_tg_id, info):
    key = prefix_handleUser + "user_info" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(info), 60 * 60 * 12)  # 12个小时
    
# ----------------------------------------------------------------------------------------------------------------------
    
# 用于判断公群是否存在, 包含基础信息：id, flag, business_detail_type
    
def group_id_get(group_tg_id):
    key = prefix + "group_id_s" + str(group_tg_id)
    
    conn = get_conn()
    
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def group_id_set(group_tg_id, val):
    key = prefix + "group_id_s" + str(group_tg_id)
    
    conn = get_conn()

    conn.set(key, json.dumps(val), 300)  # 5分钟

    
# ======================================================================================================================

# 生成缓存相关

def cheat_one_get(user_tg_id):
    key = prefix + "cheat_one" + str(user_tg_id)
    
    conn = get_conn()
    
    val = conn.get(key)
    if val is None:
        return None
    else:
        return val


def cheat_one_set(user_tg_id):
    key = prefix + "cheat_one" + str(user_tg_id)

    conn = get_conn()

    conn.set(key, 9, 60 * 6)  # 6分钟


def cheat_special_one_get(user_tg_id):
    key = prefix + "cheat_special_one" + str(user_tg_id)
    
    conn = get_conn()
    
    val = conn.get(key)
    if val is None:
        return None
    else:
        return val


def cheat_special_one_set(user_tg_id):
    key = prefix + "cheat_special_one" + str(user_tg_id)

    conn = get_conn()

    conn.set(key, 9, 60 * 6)  # 6分钟


def official_one_get(user_tg_id):
    key = prefix + "official_one" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return 9


def official_one_set(user_tg_id):
    key = prefix + "official_one" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, 9, 300)  # 5分钟


def white_one_get(user_tg_id):
    key = prefix + "white_one" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return 9


def white_one_set(user_tg_id):
    key = prefix + "white_one" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, 9, 300)  # 5分钟
    
    
def group_admin_one_get(group_tg_id, user_tg_id):
    key = prefix + "group_admin_one" + str(group_tg_id) + str(user_tg_id)
    
    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return 9


def group_admin_one_set(group_tg_id, user_tg_id):
    key = prefix + "group_admin_one" + str(group_tg_id) + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, 9, 300)  # 5分钟
    
    
# ======================================================================================================================

def user_in_group_first_time_get(user_tg_id):
    key = prefix + "user_in_group_first_time" + str(user_tg_id)
    
    conn = get_conn()
    
    val = conn.get(key)
    if val is None:
        return None
    else:
        return int(val)


def user_in_group_first_time_set(user_tg_id, created_at_timestamp):
    key = prefix + "user_in_group_first_time" + str(user_tg_id)

    conn = get_conn()

    conn.set(key, created_at_timestamp, 86400)  # 1天


# ----------------------------------------------------------------------------------------------------------------------

def msg_user_set(user_tg_id, data):
    key = prefix + "msg_user" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(data), 60 * 60 * 1)  # 3个小时


def msg_user_get(user_tg_id):
    key = prefix + "msg_user" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def msg_user_del(user_tg_id):
    key = prefix + "msg_user" + str(user_tg_id)
    
    conn = get_conn()
    
    conn.delete(key)

    
# ----------------------------------------------------------------------------------------------------------------------

def msg_single_user_set(group_tg_id, user_tg_id, data):
    key = prefix + "msg_single_user" + str(group_tg_id) + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(data), 60 * 60 * 1)  # 3个小时


def msg_single_user_get(group_tg_id, user_tg_id):
    key = prefix + "msg_single_user" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)
        
        
# ----------------------------------------------------------------------------------------------------------------------

def at_official_set(group_tg_id, user_tg_id, data):
    key = prefix + "at_official" + str(group_tg_id) + str(user_tg_id)
    
    conn = get_conn()
    
    conn.set(key, json.dumps(data), 60 * 60 * 1)  # 3个小时


def at_official_get(group_tg_id, user_tg_id):
    key = prefix + "at_official" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)
        
# ----------------------------------------------------------------------------------------------------------------------
    
def config_get(key):
    key = prefix + key
    
    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def config_set(key, val):
    key = prefix + key

    conn = get_conn()

    conn.set(key, json.dumps(val), 300)  # 5分钟


def config_one_get(key):
    key = prefix + key
    
    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return str(val, encoding="utf-8")


def config_one_set(key, val):
    key = prefix + key

    conn = get_conn()

    conn.set(key, val, 300)  # 5分钟
    
    
# ----------------------------------------------------------------------------------------------------------------------

def bot_url_get(group_tg_id, typee):
    key = prefix + "bot_url" + str(group_tg_id) + str(typee)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return str(val, encoding="utf-8")


def bot_url_set(group_tg_id, typee, bot_url):
    key = prefix + "bot_url" + str(group_tg_id) + str(typee)
    
    conn = get_conn()
    
    conn.set(key, bot_url, 300)  # 5分钟
    
    
# ----------------------------------------------------------------------------------------------------------------------

def restrict_word_get(type_str):
    key = prefix + "restrict_word_" + str(type_str)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def restrict_word_set(type_str, val):
    key = prefix + "restrict_word_" + str(type_str)

    conn = get_conn()

    conn.set(key, json.dumps(val), 3600)  # 1小时
    
    
def restrict_word_temp_get():
    key = prefix + "restrict_word_temp"

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def restrict_word_temp_set(val):
    key = prefix + "restrict_word_temp"

    conn = get_conn()

    conn.set(key, json.dumps(val), 3)  # 1小时
    
    
# ----------------------------------------------------------------------------------------------------------------------

def last_message_id_get(group_tg_id, key_short="m"):
    key = prefix + key_short + str(group_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return int(conn.get(key))


def last_message_id_set(group_tg_id, message_id, key_short="m"):
    key = prefix + key_short + str(group_tg_id)
    
    conn = get_conn()

    conn.set(key, message_id, 86400)  # 一天


# ----------------------------------------------------------------------------------------------------------------------

def reply_text_get():
    key = prefix + "reply_text"
    
    conn = get_conn()
    
    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def reply_text_set(val):
    key = prefix + "reply_text"
    
    conn = get_conn()
    
    conn.set(key, json.dumps(val), 180)  # 5分钟
    
    
# ----------------------------------------------------------------------------------------------------------------------

def user_reply_text_get(group_tg_id, user_tg_id):
    key = prefix + "user_reply_text" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def user_reply_text_set(group_tg_id, user_tg_id):
    key = prefix + "user_reply_text" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()
    
    conn.set(key, 9, 1800)
    
    
# ======================================================================================================================

def checkPinMessage_set(data):
    key = "checkPinMessage"

    conn = get_conn2()

    conn.rpush(key, json.dumps(data))


# ======================================================================================================================

def cheat_bank_get():
    key = prefix + "cheat_bank"

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def cheat_bank_set(val):
    key = prefix + "cheat_bank"

    conn = get_conn()

    conn.set(key, json.dumps(val), 300)  # 5分钟


# ----------------------------------------------------------------------------------------------------------------------

def cheat_coin_get():
    key = prefix + "cheat_coin"

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def cheat_coin_set(val):
    key = prefix + "cheat_coin"

    conn = get_conn()

    conn.set(key, json.dumps(val), 300)  # 5分钟


# ----------------------------------------------------------------------------------------------------------------------

def group_admin_get(group_tg_id):
    key = prefix + "group_admin444" + str(group_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return json.loads(val)


def group_admin_set(group_tg_id, val):
    key = prefix + "group_admin444" + str(group_tg_id)

    conn = get_conn()

    conn.set(key, json.dumps(val), 300)  # 5分钟

# ----------------------------------------------------------------------------------------------------------------------

def temp_restrict_user_get(group_tg_id, user_tg_id):
    key = prefix + "temp_restrict_user" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return False
    else:
        return True
        
        
def temp_restrict_user_set(group_tg_id, user_tg_id):
    key = prefix + "temp_restrict_user" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    conn.set(key, 1, 10)  # 10秒
    
    
# ----------------------------------------------------------------------------------------------------------------------

def temp_user_group_get(group_tg_id, user_tg_id):
    key = prefix + "temp_user_group" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return str(val, encoding="utf-8")
        
        
def temp_user_group_set(group_tg_id, user_tg_id, temp):
    key = prefix + "temp_user_group" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    conn.set(key, temp, 3600)  # 1小时
    
# ----------------------------------------------------------------------------------------------------------------------

def check_follow_get(user_tg_id):
    key = prefix + "check_follow" + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return None
    else:
        return int(conn.get(key))


def check_follow_set(user_tg_id, val):
    key = prefix + "check_follow" + str(user_tg_id)
    
    conn = get_conn()

    conn.set(key, val, 60)  # 1分钟
    

# ----------------------------------------------------------------------------------------------------------------------

def special_welcome_get(group_tg_id):
    key = prefix + "special_welcome" + str(group_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return False
    else:
        return True


def special_welcome_set(group_tg_id, val=1):
    key = prefix + "special_welcome" + str(group_tg_id)
    
    conn = get_conn()

    conn.set(key, val, 1)  # 5分钟
    

# ----------------------------------------------------------------------------------------------------------------------

def msg10_status_get(group_tg_id, user_tg_id):
    key = prefix + "msg10_status" + str(group_tg_id) + str(user_tg_id)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return False
    else:
        return True


def msg10_status_set(group_tg_id, user_tg_id):
    key = prefix + "msg10_status" + str(group_tg_id) + str(user_tg_id)
    
    conn = get_conn()

    conn.set(key, 1, 60 * 5)  # 5分钟


def todayUserJoinGroupCount(user_tg_id, plus=False):
    key = prefix + ":user:" + str(user_tg_id) + ":groups:" + time.strftime('%Y%m%d', time.localtime())

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        val = 0
    else:
        val = int(val)

    if plus:
        val = val + 1
        exat = int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=1)), '%Y-%m-%d')))
        conn.set(key, val, exat=exat)

    return val


def get_keyword_replies():
    key = prefix + ":keyword:replies"

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        replies = db.getKeywordReplies()
        data = {}
        for reply in replies:
            data[reply['keyword']] = reply

        conn.set(key, json.dumps(data), 600)
    else:
        data = json.loads(val)

    return data



def reply_repeat_check(chatId, keyword):
    key = prefix + ":keyword:reply:" + str(chatId) + ":" + str(keyword)

    conn = get_conn()

    val = conn.get(key)
    if val is None:
        return False
    else:
        return True


def set_reply_repeat(chatId, keyword):
    key = prefix + ":keyword:reply:" + str(chatId) + ":" + str(keyword)

    conn = get_conn()

    conn.set(key, 1, 180)
