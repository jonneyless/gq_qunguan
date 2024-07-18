from lib import db
from lib import db_redis
import assist 


# ==========================================================================================================================================

def init():
    start = assist.get_current_timestamp()
    
    cheats = db.cheats_all()
    cheats_len = len(cheats)
    print("cheats len %s" % cheats_len)
    num = 0
    for item in cheats:
        # print("cheats %s / %s" % (num, cheats_len))
        num = num + 1
        user_tg_id = item["tgid"]
        if assist.is_number(user_tg_id):
            db_redis.cheat_one_set(user_tg_id)
        
    cheats_special = db.cheats_special_all()
    cheats_special_len = len(cheats_special)
    print("cheats_special len %s" % cheats_special_len)
    num = 0
    for item in cheats_special:
        # print("cheats_special %s / %s" % (num, cheats_special_len))
        num = num + 1
        user_tg_id = item["tgid"]
        if assist.is_number(user_tg_id):
            db_redis.cheat_special_one_set(user_tg_id)
    
    end = assist.get_current_timestamp()
    
    print("spend %s" % (end - start))
        
        
if __name__ == '__main__':
    init()
