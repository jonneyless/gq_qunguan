from lib import db
from lib import db_redis
import assist 


# ==========================================================================================================================================

def init():
    start = assist.get_current_timestamp()
    
    # type_str
    # 1msg, 9username, 4fullname
    db.restrict_word_get(1, True)
    db.restrict_word_get(4, True)
    db.restrict_word_get(9, True)
    
    officials = db.official_all()
    officials_len = len(officials)
    print("officials len %s" % officials_len)
    num = 0
    for item in officials:
        # print("officials %s / %s" % (num, officials_len))
        num = num + 1
        user_tg_id = item["tg_id"]
        if assist.is_number(user_tg_id):
            db_redis.official_one_set(user_tg_id)
    
    whites = db.white_all()
    whites_len = len(whites)
    print("whites len %s" % whites_len)
    num = 0
    for item in whites:
        # print("whites %s / %s" % (num, whites_len))
        num = num + 1
        user_tg_id = item["tg_id"]
        if assist.is_number(user_tg_id):
            db_redis.white_one_get(user_tg_id)
    
    admins = db.group_admin_all()
    admins_len = len(admins)
    print("admins len %s" % admins_len)
    num = 0
    for item in admins:
        # print("admins %s / %s" % (num, admins_len))
        num = num + 1
        group_tg_id = item["chat_id"]
        user_tg_id = item["user_id"]
        if assist.is_number(group_tg_id) and assist.is_number(user_tg_id):
            db_redis.group_admin_one_set(group_tg_id, user_tg_id)
    
    end = assist.get_current_timestamp()
    
    print("spend %s" % (end - start))
        
        
if __name__ == '__main__':
    init()
