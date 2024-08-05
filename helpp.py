import math
import re

import config
import httpp
import net
from assist import get_current_timestamp, time2timestamp, handle_text, get_current_time, timestamp2time, get_month
from config import qunguan_bot_url, qunguan_back_bot_url, vip_group_tg_id, svip_group_tg_id, official_channels
from lib import db
from lib import db_redis


# ======================================================================================================================

def get_bot_url(group_tg_id, typee=2, back=False):
    bot_url = db_redis.bot_url_get(group_tg_id, typee)
    if bot_url is None:
        bot_url = get_bot_url_default()
        if back:
            bot_url = get_bot_url_default_back()

        bot = db.bot_one(group_tg_id, typee)
        if bot is None:
            return bot_url

        token = bot["token"]
        bot_url = "https://api.telegram.org/bot%s/" % token

        db_redis.bot_url_set(group_tg_id, typee, bot_url)

    return bot_url


def get_bot_url_default():
    return qunguan_bot_url


def get_bot_url_default_back():
    return qunguan_back_bot_url


# ======================================================================================================================

def get_user_in_group_first_time(user_tg_id):
    # 用户第一次进群时间, int时间戳 

    created_at_timestamp = get_current_timestamp()

    val = db_redis.user_in_group_first_time_get(user_tg_id)
    if val is None:
        user_group = db.user_group_new_single(user_tg_id)
        if user_group is not None:
            if user_group["created_at"] is not None:
                created_at = str(user_group["created_at"])
                created_at_timestamp = time2timestamp(created_at)

            db_redis.user_in_group_first_time_set(user_tg_id, created_at_timestamp)
    else:
        created_at_timestamp = val
        # db_redis.user_in_group_first_time_set(user_tg_id, created_at_timestamp)

    return created_at_timestamp


# ----------------------------------------------------------------------------------------------------------------------

def get_config_limit_time():
    key = "limit_time"

    limit_time = db_redis.config_one_get(key)
    if limit_time is None:
        limit_time = db.config_one_get(key)
        if limit_time is None:
            limit_time = limit_text_len
        else:
            limit_time = limit_time["val"]

        db_redis.config_one_set(key, limit_time)

    return int(limit_time)


def get_config_limit_num():
    key = "limit_num"

    limit_num = db_redis.config_one_get(key)
    if limit_num is None:
        limit_num = db.config_one_get(key)
        if limit_num is None:
            limit_num = limit_num
        else:
            limit_num = limit_num["val"]

        db_redis.config_one_set(key, limit_num)

    return int(limit_num)


def get_config_xianjing_status():
    key = "xianjing_status"

    xianjing_status = db_redis.config_one_get(key)
    if xianjing_status is None:
        xianjing_status = db.config_one_get(key)
        if xianjing_status is None:
            xianjing_status = 2
        else:
            xianjing_status = xianjing_status["val"]

        db_redis.config_one_set(key, xianjing_status)

    return int(xianjing_status)


def get_config_xianjing_time():
    key = "xianjing_time"

    xianjing_time = db_redis.config_one_get(key)
    if xianjing_time is None:
        xianjing_time = db.config_one_get(key)
        if xianjing_time is None:
            xianjing_time = 24
        else:
            xianjing_time = xianjing_time["val"]

        db_redis.config_one_set(key, xianjing_time)

    return int(xianjing_time)


def get_config_xianjing_num():
    key = "xianjing_num"

    xianjing_num = db_redis.config_one_get(key)
    if xianjing_num is None:
        xianjing_num = db.config_one_get(key)
        if xianjing_num is None:
            xianjing_num = 3
        else:
            xianjing_num = xianjing_num["val"]

        db_redis.config_one_set(key, xianjing_num)

    return int(xianjing_num)


def get_config_limit():
    one_day = 7
    one_minute = 10
    one_type = 5

    two_day = 3
    two_minute = 10
    two_type = 2
    two_num = 10

    three_day = 3
    three_minute = 10
    three_type = 3
    three_num = 10

    four_day = 8
    four_minute = 20
    four_type = 2
    four_num = 5

    configs = db_redis.config_get("config_limit")
    if configs is None:
        configs = db.config_limit_get()
        db_redis.config_set("config_limit", configs)

    for config in configs:
        if config["key"] == "one_day":
            one_day = int(config["val"])
        elif config["key"] == "one_minute":
            one_minute = int(config["val"])
        elif config["key"] == "one_type":
            one_type = int(config["val"])

        elif config["key"] == "two_day":
            two_day = int(config["val"])
        elif config["key"] == "two_minute":
            two_minute = int(config["val"])
        elif config["key"] == "two_type":
            two_type = int(config["val"])
        elif config["key"] == "two_num":
            two_num = int(config["val"])

        elif config["key"] == "three_day":
            three_day = int(config["val"])
        elif config["key"] == "three_minute":
            three_minute = int(config["val"])
        elif config["key"] == "three_type":
            three_type = int(config["val"])
        elif config["key"] == "three_num":
            three_num = int(config["val"])

        elif config["key"] == "four_day":
            four_day = int(config["val"])
        elif config["key"] == "four_minute":
            four_minute = int(config["val"])
        elif config["key"] == "four_type":
            four_type = int(config["val"])
        elif config["key"] == "four_num":
            four_num = int(config["val"])

    return {
        "one_day": one_day,
        "one_minute": one_minute,
        "one_type": one_type,

        "two_day": two_day,
        "two_minute": two_minute,
        "two_type": two_type,
        "two_num": two_num,

        "three_day": three_day,
        "three_minute": three_minute,
        "three_type": three_type,
        "three_num": three_num,

        "four_day": four_day,
        "four_minute": four_minute,
        "four_type": four_type,
        "four_num": four_num,
    }


def get_config_limit_all_time():
    key = "limit_all_time"
    # 60秒

    limit_all_time = db_redis.config_one_get(key)
    if limit_all_time is None:
        limit_all_time = db.config_one_get(key)
        if limit_all_time is None:
            limit_all_time = config.limit_all_time
        else:
            limit_all_time = limit_all_time["val"]

        db_redis.config_one_set(key, limit_all_time)

    return int(limit_all_time)


def get_config_limit_all_group_num():
    key = "limit_all_group_num"
    # 20个群

    limit_all_group_num = db_redis.config_one_get(key)
    if limit_all_group_num is None:
        limit_all_group_num = db.config_one_get(key)
        if limit_all_group_num is None:
            limit_all_group_num = config.limit_all_group_num
        else:
            limit_all_group_num = limit_all_group_num["val"]

        db_redis.config_one_set(key, limit_all_group_num)

    return int(limit_all_group_num)


def get_config_limit_cancel_restrict():
    key = "limit_cancel_restrict"
    # 5天

    limit_cancel_restrict = db_redis.config_one_get(key)
    if limit_cancel_restrict is None:
        limit_cancel_restrict = db.config_one_get(key)
        if limit_cancel_restrict is None:
            limit_cancel_restrict = config.limit_cancel_restrict
        else:
            limit_cancel_restrict = limit_cancel_restrict["val"]

        db_redis.config_one_set(key, limit_cancel_restrict)

    return int(limit_cancel_restrict)


def get_config_text_len_limit():
    key = "limit_text_len"

    limit_text_len = db_redis.config_one_get(key)
    if limit_text_len is None:
        limit_text_len = db.config_one_get(key)
        if limit_text_len is None:
            limit_text_len = config.limit_text_len
        else:
            limit_text_len = limit_text_len["val"]

        db_redis.config_one_set(key, limit_text_len)

    return int(limit_text_len)


def get_config_photo_limit_type_num():
    key = "photo_limit_type_num"

    item = db_redis.config_one_get(key)
    if item is None:
        item = db.config_one_get(key)
        if item is None:
            item = config.photo_limit_type_num
        else:
            item = item["val"]

        db_redis.config_one_set(key, item)

    return int(item)


def get_config_photo_limit_time():
    key = "photo_limit_time"

    item = db_redis.config_one_get(key)
    if item is None:
        item = db.config_one_get(key)
        if item is None:
            item = config.photo_limit_time
        else:
            item = item["val"]

        db_redis.config_one_set(key, item)

    return int(item)


def get_config_photo_limit_day():
    key = "photo_limit_day"

    item = db_redis.config_one_get(key)
    if item is None:
        item = db.config_one_get(key)
        if item is None:
            item = config.photo_limit_day
        else:
            item = item["val"]

        db_redis.config_one_set(key, item)

    return item


def get_config_limit_no_vip_restrict_time():
    key = "limit_no_vip_restrict_time"

    limit_no_vip_restrict_time = db_redis.config_one_get(key)
    if limit_no_vip_restrict_time is None:
        limit_no_vip_restrict_time = db.config_one_get(key)
        if limit_no_vip_restrict_time is None:
            limit_no_vip_restrict_time = config.limit_no_vip_restrict_time
        else:
            limit_no_vip_restrict_time = limit_no_vip_restrict_time["val"]

        db_redis.config_one_set(key, limit_no_vip_restrict_time)

    return int(limit_no_vip_restrict_time)


def get_config_limit_no_vip_type():
    key = "limit_no_vip_type"

    limit_no_vip_type = db_redis.config_one_get(key)
    if limit_no_vip_type is None:
        limit_no_vip_type = db.config_one_get(key)
        if limit_no_vip_type is None:
            limit_no_vip_type = config.limit_no_vip_type
        else:
            limit_no_vip_type = limit_no_vip_type["val"]

        db_redis.config_one_set(key, limit_no_vip_type)

    return int(limit_no_vip_type)


def get_config_limit_no_vip_num():
    key = "limit_no_vip_num"

    limit_no_vip_num = db_redis.config_one_get(key)
    if limit_no_vip_num is None:
        limit_no_vip_num = db.config_one_get(key)
        if limit_no_vip_num is None:
            limit_no_vip_num = config.limit_no_vip_num
        else:
            limit_no_vip_num = limit_no_vip_num["val"]

        db_redis.config_one_set(key, limit_no_vip_num)

    return int(limit_no_vip_num)


def get_config_limit_no_vip_time():
    key = "limit_no_vip_time"

    limit_no_vip_time = db_redis.config_one_get(key)
    if limit_no_vip_time is None:
        limit_no_vip_time = db.config_one_get(key)
        if limit_no_vip_time is None:
            limit_no_vip_time = config.limit_no_vip_time
        else:
            limit_no_vip_time = limit_no_vip_time["val"]

        db_redis.config_one_set(key, limit_no_vip_time)

    return int(limit_no_vip_time)


# ----------------------------------------------------------------------------------------------------------------------

def msg_user_set_get(group_tg_id, user_tg_id, business_detail_type, created_at_timestamp, has_at, is_photo, is_video):
    val = db_redis.msg_user_get(user_tg_id)
    if val is None:
        val = []

    val.append({
        "group_tg_id": group_tg_id,
        "business_detail_type": business_detail_type,
        "created_at_timestamp": created_at_timestamp,
        "has_at": has_at,
        "is_photo": is_photo,
        "is_video": is_video,
    })

    db_redis.msg_user_set(user_tg_id, val)

    return db_redis.msg_user_get(user_tg_id)


def msg_single_user_set_get(group_tg_id, user_tg_id, created_at_timestamp):
    # 单个群发言频率限制
    val = db_redis.msg_single_user_get(group_tg_id, user_tg_id)
    if val is None:
        val = []

    val.append(created_at_timestamp)

    db_redis.msg_single_user_set(group_tg_id, user_tg_id, val)

    return db_redis.msg_single_user_get(group_tg_id, user_tg_id)


def at_official_set_get(group_tg_id, user_tg_id, created_at_timestamp):
    # 单个群@官方
    val = db_redis.at_official_get(group_tg_id, user_tg_id)
    if val is None:
        val = []

    val.append(created_at_timestamp)

    db_redis.at_official_set(group_tg_id, user_tg_id, val)

    return db_redis.at_official_get(group_tg_id, user_tg_id)


# ======================================================================================================================

def has_restrict_word(text, type_str):
    if text is None:
        return None

    text = handle_text(text)

    restrict_words = db.restrict_word_get(type_str)

    pattern_name = "(.+)\(\.\*\)(.+)"

    # type_str
    # 1msg, 9username, 4fullname
    # 1一级限制词 2三级限制词 4二级限制词
    # 其实二级限制词4限制最大, 只有msg有二级限制词

    restrict_word = None
    for item in restrict_words:
        name = item["name"]

        level = int(item["level"])

        replace_flag = False

        result_name = re.match(pattern_name, name)

        if result_name is None:
            name = handle_text(name)

            if text.find(name) >= 0:
                if restrict_word is None:
                    replace_flag = True
                else:
                    if restrict_word["level"] < level:
                        replace_flag = True

            if replace_flag:
                restrict_word = {
                    "name": name,
                    "level": level,
                }

                if int(type_str) == 1:
                    if level == 4:
                        print("%s，%s | msg 4" % (name, text))
                        return restrict_word
                else:
                    if level == 2:
                        print("%s，%s | msg 2" % (name, text))
                        return restrict_word
        else:
            pattern1 = name
            pattern1 = "(.*)" + pattern1
            pattern1 = pattern1 + "(.*)"

            pattern1 = pattern1.lower()

            match_result = None
            try:
                match_result = re.match(pattern1, text)
            except:
                print("%s is error" % name)

            if match_result is not None:

                if restrict_word is None:
                    replace_flag = True
                else:
                    if restrict_word["level"] < level:
                        replace_flag = True
            if replace_flag:
                restrict_word = {
                    "name": item["name"],
                    "level": level,
                }

                if int(type_str) == 1:
                    if level == 4:
                        print("%s，%s | msg 4" % (name, text))
                        return restrict_word
                else:
                    if level == 2:
                        print("%s，%s | msg 2" % (name, text))
                        return restrict_word

    return restrict_word


def has_fullname_restrict_word(fullname):
    type_str = "4"
    return has_restrict_word(fullname, type_str)


def has_username_restrict_word(username):
    type_str = "9"
    return has_restrict_word(username, type_str)


def has_intro_restrict_word(intro):
    type_str = "10"
    return has_restrict_word(intro, type_str)


def has_msg_restrict_word(text):
    type_str = "1"
    return has_restrict_word(text, type_str)


def has_msg_restrict_word_temp(text):
    # text = handle_text(text)

    restrict_words = db.restrict_word_temp_get()

    for item in restrict_words:
        name = item["name"]

        # name = handle_text(name)

        if text.find(name) >= 0:
            return item

    return None


# ======================================================================================================================

def can_ope(group_tg_id, user_tg_id, check_white=True):
    flag = False

    # official_one
    # group_admin_one
    # 返回的是 true 或 false

    official = db.official_one(user_tg_id)
    if not official:
        admin = db.group_admin_one(group_tg_id, user_tg_id)
        if not admin:
            if check_white:
                whilee = db.white_one(user_tg_id)
                if not whilee:
                    flag = True
                else:
                    # print("white %s" % user_tg_id)
                    pass
            else:
                flag = True
        else:
            # print("group_admin %s %s" % (group_tg_id, user_tg_id))
            pass
    else:
        # print("official %s" % user_tg_id)
        pass

    return flag


def is_official_white(user_tg_id):
    official = db.official_one(user_tg_id)
    if official:
        return True
    else:
        whilee = db.white_one(user_tg_id)
        if whilee:
            return True

    return False


def is_vip_svip(user_tg_id):
    vip = db.user_group_new_one(vip_group_tg_id, user_tg_id)
    if vip is not None:
        return True
    else:
        svip = db.user_group_new_one(svip_group_tg_id, user_tg_id)
        if svip is not None:
            return True

    return False


# ======================================================================================================================

def follow_official_channel(user_tg_id):
    token = "5113047489:AAH37xq5dOh6YIZFSz-xImjQJYjFvB_QmVg"

    for group_tg_id in official_channels:
        flag = httpp.getChatMemberWithToken(group_tg_id, user_tg_id, token)
        if flag:
            return True

    return False


def is_session_user(user_tg_id):
    user = db.user_one(user_tg_id)
    if user is None:
        return False

    if user["has_private"] == 1:
        return False

    if user["has_private_hwdb"] == 1:
        return False

    if user["has_chat_zhuan"] == 1:
        return False

    has_private_hwdb = httpp.hwdb_hasChat(user_tg_id)
    if has_private_hwdb:
        return False

    has_chat_zhuan = httpp.zhuan_hasChat(user_tg_id)
    if has_chat_zhuan:
        return False

    if follow_official_channel(user_tg_id):
        return False

    return True


# ======================================================================================================================   

def has_cheat_bank(text):
    cheat_banks = db_redis.cheat_bank_get()
    if cheat_banks is None:
        cheat_banks_data = db.cheat_bank_get()
        cheat_banks = []
        for item in cheat_banks_data:
            cheat_banks.append(item["num"])

        db_redis.cheat_bank_set(cheat_banks)

    cheat_bank = None
    for item in cheat_banks:
        if text.find(item) >= 0:
            cheat_bank = item
            break

    return cheat_bank


def has_cheat_coin(text):
    cheat_coins = db_redis.cheat_coin_get()
    if cheat_coins is None:
        cheat_coins_data = db.cheat_coin_get()
        cheat_coins = []
        for item in cheat_coins_data:
            cheat_coins.append(item["address"])

        db_redis.cheat_coin_set(cheat_coins)

    cheat_coin = None
    for item in cheat_coins:
        if text.find(item) >= 0:
            cheat_coin = item
            break

    return cheat_coin


def like_admin(group_tg_id, sender):
    group_admins = db.group_admin_get_cache(group_tg_id)

    group_admin_like = False
    for group_admin in group_admins:
        if (sender["firstname"] == group_admin["firstname"]) and (sender["lastname"] == group_admin["lastname"]):
            if (int(sender["user_id"]) != int(group_admin["user_id"])) and sender["username"] != group_admin["username"]:
                group_admin_like = True
                break

    return group_admin_like


def has_yuefei(log_danbao):
    data_id = log_danbao["id"]
    group_tg_id = log_danbao["group_tg_id"]
    created_at = str(log_danbao['created_at'])
    yuefei_day = int(log_danbao['yuefei_day'])
    business_detail_type = int(log_danbao["business_detail_type"])
    group_num = log_danbao["num"]
    now = get_current_time()

    created_at_timestamp = time2timestamp(created_at)
    now_timestamp = get_current_timestamp()
    month_num = math.ceil((now_timestamp - created_at_timestamp) / (86400 * 30))

    text_yue_no_arr = []
    text_yue_have_arr = []
    remark = -1
    flag = True  # 月费已全部结清

    for i in range(month_num + 1):
        start_timestamp = created_at_timestamp + 86400 * i * 30
        end_timestamp = start_timestamp + 86400 * 30

        start_at = timestamp2time(start_timestamp)
        end_at = timestamp2time(end_timestamp)

        if business_detail_type != 300 and i == 0:
            # 卡商中介
            remark = get_month(start_at)
            continue

        if start_timestamp > now_timestamp:
            break

        log_yuefei = db.danbao_yuefei_one(data_id, group_num, get_month(start_at), log_danbao["created_at"])
        if log_yuefei is None:
            text_yue_no_arr.append(get_month(start_at))

            flag = False
        else:
            text_yue_have_arr.append(get_month(start_at))

    return flag, text_yue_no_arr, text_yue_have_arr, remark


# ====================================================================================================================== 

def get_groups_all():
    data = []

    max_id = -1
    flag = True
    while flag:
        groups = db.groups_get1000(max_id)
        for group in groups:
            data.append(group)
            if int(group["id"]) > max_id:
                max_id = group["id"]

        if len(groups) < 1000:
            flag = False

    return data


# ====================================================================================================================== 

def followDbAll(user_id):
    pass
    # chat_id_hwgq = -1001624139937 # hwgq
    # chat_id_gongqiu = -1001082308171 # gongqiu
    # chat_id_kefu = -1001015370323 # kefu

    # base_url_hwgq = "https://api.telegram.org/bot5113047489:AAH37xq5dOh6YIZFSz-xImjQJYjFvB_QmVg/"

    # flag, description = net.getChatMemberIn(base_url_hwgq, chat_id_hwgq, user_id)
    # if not flag:
    #     return False
    # else:
    #     flag, description = net.getChatMemberIn(base_url_hwgq, chat_id_gongqiu, user_id)
    #     if not flag:
    #         return False
    #     else:
    #         flag, description = net.getChatMemberIn(base_url_hwgq, chat_id_kefu, user_id)

    # return flag


def followGongqiu(user_id):
    chat_id_gongqiu = -1001082308171  # gongqiu

    base_url_hwgq = "https://api.telegram.org/bot5113047489:AAH37xq5dOh6YIZFSz-xImjQJYjFvB_QmVg/"

    flag, description, ok = net.getChatMemberIn(base_url_hwgq, chat_id_gongqiu, user_id)
    if ok == 1:
        return flag

    return True
