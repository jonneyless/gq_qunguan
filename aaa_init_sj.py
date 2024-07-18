import threading
import time

from lib import db
import net
import helpp
from assist import get_current_time
import assist


def main():
    created_at = assist.get_current_time()
    created_at_timestamp = assist.get_current_timestamp()
    
    start_at, end_at = assist.get_start_end(created_at_timestamp)
    
    print("start_at %s, end_at %s" % (start_at, end_at))

    groups = helpp.get_groups_all()
    for group in groups:
        group_tg_id = group["chat_id"]
        title_new = group["title"]
        business_detail_type = group["business_detail_type"]
        
        if not assist.has_yajin(title_new):
            print("%s, title_new %s no yajin" % (group_tg_id, title_new))
            continue
        
        obj = db.sj_group_yajin_one(group_tg_id, start_at, end_at)
        if obj is None:
            print("%s, new %s" % (group_tg_id, title_new))
            db.sj_group_yajin_save(group_tg_id, title_new, title_new, created_at, business_detail_type)
        else:
            if title_new != obj["title_new"]:
                print("%s, title_old %s, title_new %s" % (group_tg_id, obj["title_new"], title_new))
                db.sj_group_yajin_update(obj["id"], obj["title_new"], title_new, created_at, business_detail_type)
            else:
                pass
                # print("%s, same title %s" % (group_tg_id, title_new))
        

if __name__ == '__main__':
    start = assist.get_current_timestamp()
    
    main()
    
    end = assist.get_current_timestamp()
    
    print("spend %s" % (end - start))
    
    