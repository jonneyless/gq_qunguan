import assist
from assist import get_current_time, user_same, is_number, get_current_timestamp, timestamp2time, unique_list
from config import qunguan_tg_id, business_detail_types_no_limit
from lib import db_redis
from lib import dbpool

OPMysql = dbpool.OPMysql


# ======================================================================================================================

def user_save(user_tg_id, username, fullname, firstname, lastname):
    flag_insert = False
    flag_update = False
    flag_same = False
    text_insert = ""
    text_change = ""

    user_info = db_redis.user_info_get(user_tg_id)
    if user_info is None:
        user_info = {
            "fullname": fullname,
            "username": username
        }

        obj = user_one(user_tg_id)
        if obj is None:
            flag_insert = True
            text_insert = "insert %s %s %s" % (user_tg_id, username, fullname)
        else:
            flag = user_same(obj, user_info)
            if not flag:
                flag_update = True
                text_change = "db, %s from %s %s to %s %s" % (user_tg_id, obj["username"], obj["fullname"], username, fullname)
    else:
        user_info_new = {
            "fullname": fullname,
            "username": username,
        }
        flag = user_same(user_info_new, user_info)
        if not flag:
            flag_update = True
            text_change = "db_redis, %s from %s %s to %s %s" % (user_tg_id, user_info["username"], user_info["fullname"], username, fullname)
            
    db_redis.user_info_set(user_tg_id, user_info)
        
    if flag_insert:
        print(text_insert)
        user_insert(user_tg_id, username, fullname, firstname, lastname)
        return
    
    if flag_update:
        print(text_change)
        user_update(user_tg_id, username, fullname, firstname, lastname)
        
    # print("same %s" % user_tg_id)
    
    
def user_one_by_username(username):
    opm = OPMysql()

    sql = "select tg_id from users_new where username = '%s'" % username

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def user_one(user_tg_id):
    opm = OPMysql()

    sql = "select id, fullname, username, has_private, has_private_hwdb, has_chat_zhuan from users_new where tg_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def user_insert(user_tg_id, username, fullname, firstname, lastname):
    opm = OPMysql()

    sql = "insert into users_new(tg_id, username, fullname, firstname, lastname) values('%s', '%s', '%s', '%s', '%s')" % (user_tg_id, username, fullname, firstname, lastname)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    

def user_update(user_tg_id, username, fullname, firstname, lastname):
    opm = OPMysql()

    sql = "update users_new set username = '%s', fullname = '%s', firstname = '%s', lastname = '%s' where tg_id = '%s'" % (username, fullname, firstname, lastname, user_tg_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result

# ----------------------------------------------------------------------------------------------------------------------

def group_id_one(group_tg_id):
    group = db_redis.group_id_get(group_tg_id)
    if group is not None:
        return group
    else:
        opm = OPMysql()

        sql = "select id, flag, business_detail_type from groups where chat_id = '%s' and status_in = 1 and (flag = 2 or flag = 4)" % group_tg_id

        result = opm.op_select_one(sql)

        opm.dispose()

        if result is not None:
            db_redis.group_id_set(group_tg_id, result)

        return result


def group_set_open_status(group, open_status=1):
    data_id = group["id"]
    title = group["title"]
    title = title.lower()
    search_sort = int(group["search_sort"])
    
    if title.find("vip公群") >= 0:
        # vip公群
        if search_sort == 999 or search_sort == 1000:
            if open_status == 1:
                search_sort = 999
            elif open_status == 2:
                search_sort = 1000
    else:
        if search_sort == 99 or search_sort == 100:
            if open_status == 1:
                search_sort = 99
            elif open_status == 2:
                search_sort = 100
    
    opm = OPMysql()

    sql = "update groups set open_status = '%s', search_sort = %s where id = %s" % (open_status, search_sort, data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
def group_set_welcome_info(data_id, welcome_info):
    opm = OPMysql()

    sql = "update groups set welcome_info = '%s', welcome_status = 1 where id = %s" % (welcome_info, data_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
def group_close_welcome_info(data_id):
    opm = OPMysql()

    sql = "update groups set welcome_status = 2 where id = %s" % data_id

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
def group_set_xianjing_status(chat_id, xianjing_status):
    opm = OPMysql()

    sql = "update groups set xianjing_status = %s where chat_id = '%s'" % (xianjing_status, chat_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ----------------------------------------------------------------------------------------------------------------------

def log_invite_link_success_not_auto(user_tg_id):
    # 手动审核通过的非游戏群

    opm = OPMysql()

    sql = "select group_tg_id from log_invite_link where user_tg_id = '%s' and creates_join_request = 1 and ope_user_tg_id != '%s'" % (user_tg_id, qunguan_tg_id)
    
    result = opm.op_select_all(sql)

    opm.dispose()
    
    group_tg_ids = []
    if result is not None:
        for item in result:
            group_tg_id = item["group_tg_id"]
            group = group_id_one(group_tg_id)
            if group is not None and int(group["flag"]) == 2:
                group_tg_ids.append(item["group_tg_id"])
                
    return unique_list(group_tg_ids)
    

def log_invite_link_save(group_tg_id, user_tg_id, obj, oper=None):
    creator = obj["creator"]
    
    opm = OPMysql()

    sql = "insert into log_invite_link(group_tg_id, user_tg_id, name, invite_link, creator_tg_id, creator_username, creator_fullname, creates_join_request, pending_join_request_count, is_primary, is_revoked, expire_date, member_limit, created_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, obj["name"], obj["invite_link"], creator["tg_id"], creator["username"], creator["fullname"], obj["creates_join_request"], obj["pending_join_request_count"], obj["is_primary"], obj["is_revoked"], obj["expire_date"], obj["member_limit"], obj["created_at"])
    
    if oper is not None:
        sql = "insert into log_invite_link(group_tg_id, user_tg_id, name, invite_link, creator_tg_id, creator_username, creator_fullname, creates_join_request, pending_join_request_count, is_primary, is_revoked, expire_date, member_limit, created_at, ope_user_tg_id, ope_username, ope_fullname) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, obj["name"], obj["invite_link"], creator["tg_id"], creator["username"], creator["fullname"], obj["creates_join_request"], obj["pending_join_request_count"], obj["is_primary"], obj["is_revoked"], obj["expire_date"], obj["member_limit"], obj["created_at"], oper["user_tg_id"], oper["username"], oper["fullname"])

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        pass
        # print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
# ----------------------------------------------------------------------------------------------------------------------

def user_group_new30(user_tg_id):
    now = get_current_timestamp()
    min30 = timestamp2time(now - 60 * 30)
    
    group_tg_ids = []
    
    opm = OPMysql()

    sql = "select group_tg_id from user_group_new where user_tg_id = '%s' and created_at >= '%s'" % (user_tg_id, min30)

    result = opm.op_select_all(sql)

    opm.dispose()
    
    business_detail_types = []
    if result is not None:
        for item in result:
            group_tg_id = item["group_tg_id"]
            group = group_id_one(group_tg_id)
            if group is not None and int(group["flag"]) == 2 and int(group["business_detail_type"]) not in business_detail_types_no_limit:
                business_detail_types.append(group["business_detail_type"])
                group_tg_ids.append(group_tg_id)
    
    business_detail_types = unique_list(business_detail_types)
    if len(business_detail_types) > 2:
        return group_tg_ids
    else:
        return []
    

def user_group_new_for_restrict(user_tg_id):
    group_tg_ids = []
    
    opm = OPMysql()

    sql = "select group_tg_id from user_group_new where user_tg_id = '%s' and status_in = 1" % user_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()
    
    if result is not None:
        for item in result:
            group_tg_ids.append(item["group_tg_id"])
    
    return group_tg_ids
    
    
def user_group_new_to_restrict(user_tg_id):
    group_tg_ids = []
    
    opm = OPMysql()

    sql = "select group_tg_id from user_group_new where user_tg_id = '%s' and status_in = 1 and status_restrict = 1" % user_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()
    
    if result is not None:
        for item in result:
            group_tg_ids.append(item["group_tg_id"])
    
    return group_tg_ids
    
    
def user_group_new_to_ban(user_tg_id):
    group_tg_ids = []
    
    opm = OPMysql()

    sql = "select group_tg_id from user_group_new where user_tg_id = '%s' and status_in = 1" % user_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()
    
    if result is not None:
        for item in result:
            group_tg_ids.append(item["group_tg_id"])
    
    return group_tg_ids
    
    
def user_group_new_single(user_tg_id):
    opm = OPMysql()

    sql = "select id, created_at from user_group_new where user_tg_id = '%s' order by created_at asc" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def user_group_new_one(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "select id, created_at from user_group_new where group_tg_id = '%s' and user_tg_id = '%s'" % (group_tg_id, user_tg_id)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


def user_group_new_save(group_tg_id, user_tg_id, created_at, updated_at, is_admin=-1, status_in=-1, status_restrict=-1, status_ban=-1):
    
    val_new = "%s_%s_%s_%s" % (is_admin, status_in, status_restrict, status_ban)
    val_old = db_redis.temp_user_group_get(group_tg_id, user_tg_id)
    
    if val_old is None:
        obj = user_group_new_one(group_tg_id, user_tg_id)
        if obj is None:
            opm = OPMysql()
        
            sql = "insert into user_group_new(group_tg_id, user_tg_id, is_admin, status_in, status_restrict, status_ban, created_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                group_tg_id, user_tg_id, is_admin, status_in, status_restrict, status_ban, created_at)
        
            result = None
            try:
                result = opm.op_update(sql)
            except Exception as e:
                print("sql %s %s" % (sql, e))
        
            opm.dispose()
            
            db_redis.temp_user_group_set(group_tg_id, user_tg_id, val_new)
            
            return
    
    if val_new != val_old:
        print("%s %s, %s %s" % (group_tg_id, user_tg_id, val_new, val_old))
        db_redis.temp_user_group_set(group_tg_id, user_tg_id, val_new)
        user_group_new_update_new(group_tg_id, user_tg_id, updated_at, is_admin, status_in, status_restrict, status_ban)
    else:
        print("same %s %s %s" % (group_tg_id, user_tg_id, val_new))

    # return result


def user_group_new_update(data_id, updated_at, is_admin=-1, status_in=-1, status_restrict=-1, status_ban=-1):
    opm = OPMysql()

    sql = "update user_group_new set updated_at = '%s', is_admin = %s, status_in = %s, status_restrict = %s, status_ban = %s where id = %s" % (updated_at, is_admin, status_in, status_restrict, status_ban, data_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result


def user_group_new_update_new(group_tg_id, user_tg_id, updated_at, is_admin=-1, status_in=-1, status_restrict=-1, status_ban=-1):
    opm = OPMysql()

    sql = "update user_group_new set updated_at = '%s', is_admin = %s, status_in = %s, status_restrict = %s, status_ban = %s where group_tg_id = '%s' and user_tg_id = '%s'" % (updated_at, is_admin, status_in, status_restrict, status_ban, group_tg_id, user_tg_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
# ----------------------------------------------------------------------------------------------------------------------

def message_save(group_tg_id, user_tg_id, message_tg_id, info, created_at):
    opm = OPMysql()

    sql = "insert into msg(chat_id, user_id, message_id, info, created_at) values('%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, user_tg_id, message_tg_id, info, created_at)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result


def message_delete(group_tg_id, message_tg_id):
    pass
    # opm = OPMysql()

    # sql = "update msg set flag = 2 where chat_id = '%s' and message_id = '%s'" % (group_tg_id, message_tg_id)

    # result = None
    # try:
    #     result = opm.op_update(sql)
    # except Exception as e:
    #     print("sql %s %s" % (sql, e))

    # opm.dispose()

    # return result


# msg       存储信息
# log_msg48 用于获取msg_tg_id来删除信息


def msg48_get(group_tg_id, user_tg_id):
    ids = []
    
    opm = OPMysql()

    sql = "select msg_tg_id from log_msg48 where group_tg_id = '%s' and user_tg_id = '%s' order by id desc" % (group_tg_id, user_tg_id)

    result = opm.op_select_all(sql)

    opm.dispose()
    
    if result is not None:
        for item in result:
            ids.append(int(item["msg_tg_id"]))
    
    return ids
    

def log_msg48_save(group_tg_id, user_tg_id, msg_tg_id, created_at):
    opm = OPMysql()

    sql = "insert into log_msg48(group_tg_id, user_tg_id, msg_tg_id, created_at) values('%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, msg_tg_id, created_at)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
def log_msg_address_save(title, group_tg_id, user_tg_id, username, fullname, msg_tg_id, info, created_at):
    opm = OPMysql()

    sql = "insert into log_msg_address(title, group_tg_id, user_tg_id, username, fullname, msg_tg_id, info, created_at) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (title, group_tg_id, user_tg_id, username, fullname, msg_tg_id, info, created_at)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result

    
# ======================================================================================================================

# 生成缓存相关

def cheats_all():
    opm = OPMysql()

    sql = "select tgid from cheats order by id desc"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
def cheats_special_all():
    opm = OPMysql()

    sql = "select tgid from cheats_special order by id desc"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


def official_all():
    opm = OPMysql()

    sql = "select tg_id from offical_user order by id desc"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


def white_all():
    opm = OPMysql()

    sql = "select tg_id from white_user order by id desc"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
def group_admin_all():
    opm = OPMysql()

    sql = "select chat_id, user_id from group_admin order by id desc"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    

# ======================================================================================================================

def cheat_save(user_tg_id, reason):
    opm = OPMysql()

    sql = "insert into cheats(tgid, reason, created_at) values('%s', '%s', '%s')" % (user_tg_id, reason, get_current_time())

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()
    
    if result is not None:
        if is_number(user_tg_id):
            db_redis.cheat_one_set(user_tg_id)
    
    return result
    
    
# ----------------------------------------------------------------------------------------------------------------------

def config_limit_get():
    opm = OPMysql()

    sql = "select * from config where description = 'limit'"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


def config_one_get(key):
    opm = OPMysql()

    sql = "select val from config where `key` = '%s' limit 1" % key

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
# ----------------------------------------------------------------------------------------------------------------------

def cheat_one(user_tg_id):
    # flag = db_redis.cheat_one_get(user_tg_id)
    # if flag is not None:
    #     return True
    # else:
    opm = OPMysql()

    sql = "select tgid from cheats where tgid = '%s' limit 1" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    if result is not None:
        db_redis.cheat_one_set(user_tg_id)
        return True
            
    return False
    
    
def cheats_special_one(user_tg_id):
    flag = db_redis.cheat_special_one_get(user_tg_id)
    if flag is not None:
        return True
    else:
        opm = OPMysql()
    
        sql = "select tgid from cheats_special where tgid = '%s' limit 1" % user_tg_id

        result = opm.op_select_one(sql)
    
        opm.dispose()

        if result is not None:
            db_redis.cheat_special_one_set(user_tg_id)
            return True
            
    return False  


def official_one(user_tg_id):
    flag = db_redis.official_one_get(user_tg_id)
    if flag is not None:
        return True
    else:
        opm = OPMysql()
    
        sql = "select id from offical_user where tg_id = '%s' limit 1" % user_tg_id

        result = opm.op_select_one(sql)
    
        opm.dispose()

        if result is not None:
            db_redis.official_one_set(user_tg_id)
            return True
            
    return False


def white_one(user_tg_id):
    flag = db_redis.white_one_get(user_tg_id)
    if flag is not None:
        return True
    else:
        opm = OPMysql()
    
        sql = "select id from white_user where tg_id = '%s' limit 1" % user_tg_id

        result = opm.op_select_one(sql)
    
        opm.dispose()

        if result is not None:
            db_redis.white_one_set(user_tg_id)
            return True
            
    return False
    
    
def group_admin_one(group_tg_id, user_tg_id):
    flag = db_redis.group_admin_one_get(group_tg_id, user_tg_id)
    
    if flag is not None:
        return True
    else:
        opm = OPMysql()
    
        sql = "select id from group_admin where chat_id = '%s' and user_id = '%s'" % (group_tg_id, user_tg_id)
    
        result = opm.op_select_one(sql)
    
        opm.dispose()
    
        if result is not None:
            db_redis.group_admin_one_set(group_tg_id, user_tg_id)
            return True
            
    return False
    
    
def group_admin_title_one(group_tg_id, flag=1):
    title = "本公群老板，小心骗子假冒"
    if flag == 2:
        title == "本公群业务员，小心骗子假冒"
    
    opm = OPMysql()

    sql = "select id from group_admin where chat_id = '%s' and custom_title = '%s'" % (group_tg_id, title)

    result = opm.op_select_one(sql)

    opm.dispose()
    
    return result
    
    
def group_admin_single(user_tg_id):
    opm = OPMysql()

    sql = "select id from group_admin where user_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()
    
    if result is not None:
        return True
            
    return False


def group_admin_one_all(group_tg_id):
    opm = OPMysql()

    sql = "select chat_id, user_id, fullname, username, custom_title, status from group_admin where chat_id = '%s'" % group_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()
    
    return result


def jiaoyi_one(group_tg_id):
    opm = OPMysql()

    selectSql = "select user_id, username, fullname from group_admin where chat_id = '%s' and CONCAT(firstname, lastname) like '%%交易员%%'" % group_tg_id

    result = opm.op_select_one(selectSql)

    opm.dispose()

    return result
    

def shenji_one(group_tg_id):
    opm = OPMysql()

    selectSql = "select user_id, username, fullname from group_admin where chat_id = '%s' and CONCAT(firstname, lastname) like '%%审计%%'" % group_tg_id

    result = opm.op_select_one(selectSql)

    opm.dispose()

    return result
    
    
# ----------------------------------------------------------------------------------------------------------------------

def bot_one(group_tg_id, typee):
    typee = int(typee)
    
    opm = OPMysql()

    sql = "select bots.* from bot_group join bots on bot_group.user_tg_id = bots.tg_id where bot_group.group_tg_id = '%s' and bots.type = %s" % (group_tg_id, typee)
    if typee == 4:
        # 定时推送，不需要管理
        sql = "select bots.* from bot_group join bots on bot_group.user_tg_id = bots.tg_id where bot_group.group_tg_id = '%s' and bots.type = %s" % (group_tg_id, typee)
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result


def white_user_bot_one(tg_id):
    opm = OPMysql()

    sql = "select id from white_user_bot where tg_id = '%s'" % tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
# ----------------------------------------------------------------------------------------------------------------------

def restrict_word_get(type_str, flag=False):
    type_str = int(type_str)
    
    restrict_words = db_redis.restrict_word_get(type_str)
    if restrict_words is None or flag:
        restrict_words = []
        
        opm = OPMysql()
    
        sql = "select name, level from words where type = %s" % type_str
        
        result = opm.op_select_all(sql)
    
        opm.dispose()

        for item in result:
            restrict_words.append(item)
            
        if flag:
            print("%s %s" % (sql, len(restrict_words)))
            
        db_redis.restrict_word_set(type_str, restrict_words)
        
    return restrict_words
    
    
def restrict_word_temp_get(flag=False):
    restrict_words = db_redis.restrict_word_temp_get()
    if restrict_words is None or flag:
        restrict_words = []
        
        opm = OPMysql()
    
        sql = "select name from words_temp"
        
        result = opm.op_select_all(sql)
    
        opm.dispose()

        for item in result:
            restrict_words.append(item)
            
        if flag:
            print("%s %s" % (sql, len(restrict_words)))
            
        db_redis.restrict_word_temp_set(restrict_words)
        
    return restrict_words
    
    
# ======================================================================================================================

def log_delete_save(group_tg_id, user_tg_id, message_tg_id, reason, admin_id=-1):
    pass
    # opm = OPMysql()

    # sql = "insert into log_delete_message(group_tg_id, user_tg_id, message_tg_id, reason, created_at, admin_id) values('%s', '%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, message_tg_id, reason, get_current_time(), admin_id)

    # result = None
    # try:
    #     result = opm.op_update(sql)
    # except Exception as e:
    #     print("sql %s %s" % (sql, e))

    # opm.dispose()

    # return result
    
    
def log_kick_save(group_tg_id, user_tg_id, reason, admin_id=-1):
    opm = OPMysql()

    sql = "insert into log_ban_user(group_tg_id, user_tg_id, reason, created_at, admin_id) values('%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, reason, get_current_time(), admin_id)
    
    db_redis.db_log_set({
        "sql": sql,
    })

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))
    
    opm.dispose()
    
    return result


def log_restrict_save(group_tg_id, user_tg_id, until_data, reason, admin_id=-1):
    opm = OPMysql()

    sql = "insert into log_restrict_user(group_tg_id, user_tg_id, until_data, reason, created_at, admin_id) values('%s', '%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, until_data, reason, get_current_time(), admin_id)

    db_redis.db_log_set({
        "sql": sql,
    })

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))
    
    opm.dispose()
    
    return result
    
    
def log_save(sql):
    opm = OPMysql()

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))
    
    opm.dispose()
    
    return result

    
# ======================================================================================================================

def log_approve_save(group_tg_id, user_tg_id, user, status=2):
    opm = OPMysql()

    sql = "insert into log_approve(group_tg_id, user_tg_id, status, created_at, username, fullname, firstname, lastname) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, status, get_current_time(), user["username"], user["fullname"], user["firstname"], user["lastname"])

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))
    
    opm.dispose()
    
    return result


def log_approve_update(data_id, status, reason):
    opm = OPMysql()

    sql = "update log_approve set status = '%s', reason = '%s', updated_at = '%s' where id = '%s'" % (status, reason, get_current_time(), data_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result


# ======================================================================================================================

def group_admin_get_cache(group_tg_id):
    data = db_redis.group_admin_get(group_tg_id)
    if data is not None:
        return data
    else:
        data = group_admin_get(group_tg_id)
        db_redis.group_admin_set(group_tg_id, data)

        return data
    
    
def group_admin_get(group_tg_id, is_bot=2):
    opm = OPMysql()

    sql = "select chat_id, user_id, firstname, lastname, username from group_admin where chat_id = '%s' " % group_tg_id

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
    
def get_group_not_official_admin(group_tg_id):
    admins = group_admin_get(group_tg_id)
    arr = []
    for admin in admins:
        if not official_one(admin["user_id"]):
            arr.append(admin)
            
    return arr
    
    
def official_one_by_username(username):
    opm = OPMysql()

    sql = "select id from offical_user where username ='%s'" % username

    result = opm.op_select_one(sql)

    opm.dispose()

    return result

    
def reply_text_get():
    data = db_redis.reply_text_get()
    if data is not None:
        return data
    else:
        opm = OPMysql()
        
        sql = "select keyy, val from config_text where name = 'reply' limit 1"

        result = opm.op_select_one(sql)

        opm.dispose()

        data = None

        if result is not None:
            data = {
                "keyy": result["keyy"],
                "val": result["val"],
            }
            
            db_redis.reply_text_set(data)

        return data
        
        
# ======================================================================================================================

def cheat_bank_get():
    opm = OPMysql()

    sql = "select num from cheat_bank"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


def cheat_coin_get():
    opm = OPMysql()

    sql = "select address from cheat_coin"

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    
# ======================================================================================================================

def group_admin_title_update(group_tg_id, user_tg_id, custom_title=""):
    opm = OPMysql()

    sql = "update group_admin set custom_title = '%s' where chat_id = '%s' and user_id = '%s'" % (custom_title, group_tg_id, user_tg_id)
    
    print(sql)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
def group_admin_save(group_tg_id, user_tg_id, custom_title=""):
    username = ""
    fullname = ""
    firstname = ""
    lastname = ""
    
    user = user_one(user_tg_id)
    if user is not None:
        username = user["username"]
        fullname = user["fullname"]
        firstname = fullname
    
    opm = OPMysql()

    sql = "insert into group_admin(chat_id, user_id, status, created_at, custom_title, username, fullname, firstname) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
        group_tg_id, user_tg_id, "administrator", get_current_time(), custom_title, username, fullname, firstname)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        # group_admin_title_update(group_tg_id, user_tg_id, custom_title)
        print("sql %s %s" % (sql, e))

    opm.dispose()
    
    if result is not None:
        db_redis.group_admin_one_set(group_tg_id, user_tg_id)

    return result
    
    
# ======================================================================================================================

def sj_group_yajin_over(data_id, is_active, has_trade, trade_type, jiaoyi = '', shenji = '', active_level=1, status=1):
    opm = OPMysql()

    sql = "update sj_group_yajin set is_active = %s, has_trade = %s, trade_type = %s, status = %s, updated_at = '%s', jiaoyi = '%s', shenji = '%s', active_level = %s where id = %s" % (is_active, has_trade, trade_type, status, assist.get_current_time(), jiaoyi, shenji, active_level, data_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    

def sj_group_yajin_all(start_at, end_at):
    opm = OPMysql()

    sql = "select * from sj_group_yajin where created_at >= '%s' and created_at < '%s'" % (start_at, end_at)

    result = opm.op_select_all(sql)

    opm.dispose()

    return result
    

def sj_user_say_one(group_tg_id, start_at, end_at):
    opm = OPMysql()

    sql = "select * from sj_user_say where group_tg_id = '%s' and created_at >= '%s' and created_at < '%s' " % (group_tg_id, start_at, end_at)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def sj_user_say_save(group_tg_id, user_tg_id, created_at):
    opm = OPMysql()

    sql = "insert into sj_user_say(group_tg_id, user_tg_id, created_at) values('%s', '%s', '%s')" % (group_tg_id, user_tg_id, created_at)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
def sj_official_say_one(group_tg_id, start_at, end_at):
    opm = OPMysql()

    sql = "select * from sj_official_say where group_tg_id = '%s' and created_at >= '%s' and created_at < '%s' " % (group_tg_id, start_at, end_at)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def sj_official_say_save(group_tg_id, user_tg_id, created_at):
    opm = OPMysql()

    sql = "insert into sj_official_say(group_tg_id, user_tg_id, created_at) values('%s', '%s', '%s')" % (group_tg_id, user_tg_id, created_at)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    

def sj_group_yajin_one(group_tg_id, start_at, end_at):
    opm = OPMysql()

    sql = "select * from sj_group_yajin where group_tg_id = '%s' and created_at >= '%s' and created_at < '%s' " % (group_tg_id, start_at, end_at)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def sj_group_yajin_save(group_tg_id, title_old, title_new, created_at, business_detail_type):
    opm = OPMysql()

    sql = "insert into sj_group_yajin(group_tg_id, title_old, title_new, created_at, business_detail_type) values('%s', '%s', '%s', '%s', '%s')" % (group_tg_id, title_old, title_new, created_at, business_detail_type)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
def sj_group_yajin_update(data_id, title_old, title_new, created_at, business_detail_type):
    opm = OPMysql()

    sql = "update sj_group_yajin set title_old = '%s', title_new = '%s', created_at = '%s', business_detail_type = %s where id = %s" % (title_old, title_new, created_at, business_detail_type, data_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
# ======================================================================================================================

def get_danbao_admins(admins):
    info_creator = ""
    info_jiaoyiyuan = ""
    info_boss = ""
    info_yewuyuan = ""
    
    for admin in admins:
        if admin["username"] is None:
            admin["username"] = ""  
        if admin["fullname"] is None:
            admin["fullname"] = ""
        if admin["custom_title"] is None:
            admin["custom_title"] = ""

        info_admin = "%s,%s,%s" % (admin["user_id"], admin["fullname"], admin["username"])
        if admin["status"] == "creator":
            info_creator = info_admin
            
        if admin["fullname"].find("交易员") >= 0:
            if official_one(admin["user_id"]):
                info_jiaoyiyuan += info_admin
                info_jiaoyiyuan += "\n"
        if admin["custom_title"].find("本公群老板") >= 0:
            info_boss += info_admin
            info_boss += "\n"
        if admin["custom_title"].find("本公群业务员") >= 0:
            info_yewuyuan += info_admin
            info_yewuyuan += "\n"
        
    return info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan
    
    
def danbao_one(group_tg_id, status = 1):
    opm = OPMysql()

    sql = "select * from log_danbao where group_tg_id = '%s' and status = %s" % (group_tg_id, status)

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def danbao_save(group, admins):
    info_creator = ""
    info_jiaoyiyuan = ""
    info_boss = ""
    info_yewuyuan = ""
    
    info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan = get_danbao_admins(admins)
    now = assist.get_current_time()
    yuefei_day = assist.get_day_int()
        
    opm = OPMysql()

    sql = "insert into log_danbao(group_tg_id, title, num, info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, business_detail_type, created_at, yuefei_day) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (group["tg_id"], group["title"], group["group_num"], info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, group["business_detail_type"], now, yuefei_day)

    result = opm.op_update(sql)

    opm.dispose()

    return result
    

def danbao_update(log_danbao, group, admins):
    data_id = log_danbao["id"]

    opm = OPMysql()

    info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan = get_danbao_admins(admins)

    sql_update = "update log_danbao set title = '%s', num = '%s', info_creator = '%s', info_jiaoyiyuan = '%s', info_boss = '%s', info_yewuyuan = '%s', business_detail_type = '%s' where id = %s" % (group["title"], group["group_num"], info_creator, info_jiaoyiyuan, info_boss, info_yewuyuan, group["business_detail_type"], data_id)
    
    result = opm.op_update(sql_update)

    opm.dispose()

    return result
    

def danbao_over(data_id):
    opm = OPMysql()

    sql_update = "update log_danbao set status = 2, ended_at = '%s' where id = %s" % (assist.get_current_time(), data_id)
    
    result = opm.op_update(sql_update)
    
    opm.dispose()

    return result
    
    
def danbao_update_yuefei(data_id, yuefei):
    opm = OPMysql()

    sql_update = "update log_danbao set yuefei = %s where id = %s" % (yuefei, data_id)
    
    result = opm.op_update(sql_update)
    
    opm.dispose()

    return result
    
    
def log_danbao_change_yuefei_save(data_id, group_tg_id, yuefei_old, yuefei_new, user_tg_id=-1):
    opm = OPMysql()

    sql = "insert into log_danbao_change_yuefei(data_id, group_tg_id, yuefei_old, yuefei_new, created_at, user_tg_id) values('%s', '%s', '%s', '%s', '%s', '%s')" % (data_id, group_tg_id, yuefei_old, yuefei_new, assist.get_current_time(), user_tg_id)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
def danbao_yuefei_one(data_id, group_num, month, created_at):
    opm = OPMysql()

    sql = "select * from log_danbao_yuefei where title = '%s' and month = '%s' and status = 2 and created_at >= '%s'" % (group_num, month, created_at)
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result
    
    
def danbao_yuefei_over(group_num):
    opm = OPMysql()

    sql = "update log_danbao_yuefei set status = 1 where title = '%s' and status = 2" % group_num
    
    result = opm.op_select_one(sql)

    opm.dispose()

    return result

    
def group_trade_report_del(group_tg_id):
    opm = OPMysql()

    sql = "update group_trade_report set status_del = 2 where group_tg_id = '%s'" % group_tg_id

    result = opm.op_update(sql)

    opm.dispose()

    return result
    
    
# ======================================================================================================================

def groups_get1000(max_id=-1):
    opm = OPMysql()

    sql = "select id, chat_id, title, business_detail_type from groups where flag = 2 and status_in = 1 and title like '%%已押%%' and id > %s order by id asc limit 1000" % max_id
    
    print(sql)

    result = opm.op_select_all(sql)

    opm.dispose()

    return result


def getGroupIds():
    opm = OPMysql()

    sql = "select chat_id from `groups` where flag=2 and deleted = 2 and opened = 1"

    result = opm.op_select_all(sql)

    opm.dispose()

    ids = []
    for group in result:
        ids.append(group['chat_id'])

    return ids
    
# ======================================================================================================================

def msg_get(group_tg_id, start_at, end_at):
    opm = OPMysql()

    selectSql = "select id, user_id from msg where chat_id = '%s' and created_at >= '%s' and created_at < '%s'" % (group_tg_id, start_at, end_at)

    result = opm.op_select_all(selectSql)

    opm.dispose()

    return result
    

# ======================================================================================================================

def log_xianjing_in_save(group_tg_id, user_tg_id):
    opm = OPMysql()

    sql = "insert into log_xianjing_in(group_tg_id, user_tg_id, created_at) values('%s', '%s', '%s')" % (group_tg_id, user_tg_id, assist.get_current_time())

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result
    
    
def log_xianjing_in_num(user_tg_id, created_at):
    opm = OPMysql()

    selectSql = "select count(id) as num from log_xianjing_in where user_tg_id = '%s' and created_at >= '%s'" % (user_tg_id, created_at)
    
    print(selectSql)

    result = opm.op_select_one(selectSql)

    opm.dispose()
    
    num = 0
    if result is not None:
        num = int(result["num"])

    return num
    

# ======================================================================================================================

def log_msg10_same_num(group_tg_id, user_tg_id, info):
    now = assist.get_current_timestamp()
    created_at_timestamp = now - 60 * 10

    opm = OPMysql()

    sql = "select count(id) as temp from log_msg10 where group_tg_id = '%s' and user_tg_id = '%s' and info = '%s' and created_at_timestamp >= %s" % (group_tg_id, user_tg_id, info, created_at_timestamp)

    result = opm.op_select_one(sql)

    opm.dispose()
    
    if result is not None:
        return result["temp"]
    else:
        return 0 
    

def log_msg10_save(group_tg_id, user_tg_id, msg_tg_id, info, created_at_timestamp):
    opm = OPMysql()

    sql = "insert into log_msg10(group_tg_id, user_tg_id, msg_tg_id, info, created_at_timestamp) values('%s', '%s', '%s', '%s', '%s')" % (group_tg_id, user_tg_id, msg_tg_id, info, created_at_timestamp)

    result = None
    try:
        result = opm.op_update(sql)
    except Exception as e:
        print("sql %s %s" % (sql, e))

    opm.dispose()

    return result


def official_get_firstname(user_tg_id):
    opm = OPMysql()

    sql = "select firstname from offical_user where tg_id ='%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    if result is None:
        return ""

    return result['firstname']


def filterOfficialUserNames(usernames):
    opm = OPMysql()

    sql = opm.cur.mogrify("select * from `official_username` where 1 = %s and username in %s", (1, usernames))

    result = opm.op_select_all(sql)

    opm.dispose()

    items = []
    for item in result:
        items.append(item['username'])

    return items
