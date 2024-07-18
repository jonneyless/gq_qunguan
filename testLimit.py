import helpp
from lib import db_redis
import helpp
import assist


def check(user_tg_id, fullname_is_en, group_tg_id_one=False):
    current_timestamp = assist.get_current_timestamp()
    
    limit_time = helpp.get_config_limit_time() # 秒
    limit_num = helpp.get_config_limit_num()
        
    config_limit = helpp.get_config_limit()
    limit_all_time = helpp.get_config_limit_all_time()
    limit_all_group_num = helpp.get_config_limit_all_group_num()
    limit_cancel_restrict = helpp.get_config_limit_cancel_restrict()
    
    photo_limit_type_num = helpp.get_config_photo_limit_type_num()
    photo_limit_time = helpp.get_config_photo_limit_time()
    photo_limit_day = helpp.get_config_photo_limit_day()
    
    user_in_group_first_time = helpp.get_user_in_group_first_time(user_tg_id)
    
    current_timestamp = assist.get_current_timestamp()
    
    until_date = -1
    
    flag_restrict = False
    save_cheat = True
    reason = ""
    group_tg_ids = []
    
    one_day = config_limit["one_day"]
    one_minute = config_limit["one_minute"]
    one_type = config_limit["one_type"]
    
    two_day = config_limit["two_day"]
    two_minute = config_limit["two_minute"]
    two_type = config_limit["two_type"]
    two_num = config_limit["two_num"]
    
    three_day = config_limit["three_day"]
    three_minute = config_limit["three_minute"]
    three_type = config_limit["three_type"]
    three_num = config_limit["three_num"]
    
    four_day = config_limit["four_day"]
    four_minute = config_limit["four_minute"]
    four_type = config_limit["four_type"]
    four_num = config_limit["four_num"]
    
    msgs = db_redis.msg_user_get(user_tg_id)
    
    flag_restrict = False

    if not flag_restrict:
        group_tg_ids = []
        if user_in_group_first_time > current_timestamp - 86400 * one_day:
            # 达到第一个处理条件
            types = []
            for msg in msgs:
                if int(msg["created_at_timestamp"]) > current_timestamp - 60 * one_minute:
                    types.append(msg["business_detail_type"])
                    group_tg_ids.append(msg["group_tg_id"])
            types = set(types)
            
            if len(types) > one_type:
                flag_restrict = True
                reason = "进群时间%s天内的用户，%s分钟内在%s种以上类型的群，发送信息" % (one_day, one_minute, one_type)
                
    if not flag_restrict:
        group_tg_ids = []
        if user_in_group_first_time > current_timestamp - 86400 * two_day:
            # 达到第二个处理条件
            types = []
            num = 0
            for msg in msgs:
                if int(msg["has_at"]) == 1:
                    if int(msg["created_at_timestamp"]) > current_timestamp - 60 * two_minute:
                        types.append(msg["business_detail_type"])
                        group_tg_ids.append(msg["group_tg_id"])
                        num = num + 1
            types = set(types)
            
            if len(types) >= two_type and num > two_num:
                flag_restrict = True
                reason = "进群时间%s天内的用户，%s分钟内在%s种或以上类型的群发送了%s条以上包含@的信息" % (two_day, two_minute, two_type, two_num)
    
    if fullname_is_en == 1:
        if not flag_restrict:
            group_tg_ids = []
            if user_in_group_first_time > current_timestamp - 86400 * three_day:
                # 达到第三个处理条件
                
                types = []
                num = 0
                for msg in msgs:
                    if int(msg["created_at_timestamp"]) > current_timestamp - 60 * three_minute:
                        types.append(msg["business_detail_type"])
                        group_tg_ids.append(msg["group_tg_id"])
                        num = num + 1
                types = set(types)
                
                if len(types) >= three_type and num > three_num:
                    flag_restrict = True
                    reason = "进群时间%s天内的用户，%s分钟内在%s种或以上类型的群发送了%s条以上信息且昵称为全英文" % (three_day, three_minute, three_type, three_num)
        
        if not flag_restrict:
            group_tg_ids = []
            if user_in_group_first_time > current_timestamp - 86400 * four_day:
                # 达到第四个处理条件
                
                types = []
                num = 0
                for msg in msgs:
                    if int(msg["has_at"]) == 1:
                        if int(msg["created_at_timestamp"]) > current_timestamp - 60 * four_minute:
                            types.append(msg["business_detail_type"])
                            group_tg_ids.append(msg["group_tg_id"])
                            num = num + 1
                types = set(types)
                
                if len(types) >= four_type and num > four_num:
                    flag_restrict = True
                    reason = "进群时间%s天内的用户，%s分钟内在%s种或以上类型的群发送了%s条以上包含@的信息且昵称为全英文" % (four_day, four_minute, four_type, four_num)
    
    if not flag_restrict:
        group_tg_ids = []
        types = []
        for msg in msgs:
            if int(msg["created_at_timestamp"]) > current_timestamp - 60 * 5:
                types.append(msg["business_detail_type"])
                group_tg_ids.append(msg["group_tg_id"])
                
        types = set(types)
        group_tg_ids = set(group_tg_ids)
        if len(types) > 2 and len(group_tg_ids) > 9:
            if not helpp.is_vip_svip(user_tg_id):
                flag_restrict = True
                save_cheat = False
                reason = "5分钟内发言群数 %s 大于9个，群组类型 %s 大于2种 %s " % (len(group_tg_ids), len(types), user_tg_id)
                # print(reason)
    
    if not flag_restrict:
        if user_in_group_first_time > current_timestamp - 86400 * 10:
            # 10天进群的用户
            types = []
            group_tg_ids = []
            for msg in msgs:
                if "is_photo" in msg and int(msg["is_photo"]) == 1 and int(msg["created_at_timestamp"]) > current_timestamp - 60 * photo_limit_time:
                    types.append(msg["business_detail_type"])
                    group_tg_ids.append(msg["group_tg_id"])
            
            types = set(types)
            if len(types) > photo_limit_type_num:
                reason = "进群时间10天内，%s 分钟内在 %s 个类型的群内发送图片，超过 %s，%s" % (photo_limit_time, len(types), photo_limit_type_num, user_tg_id)
                flag_restrict = True
    
    if not flag_restrict:
        # 120秒内，发送3个1M大小的视频，禁言1天
        group_tg_ids = []
        num = 0
        for msg in msgs:
            if "is_video" in msg and int(msg["is_video"]) == 1 and int(msg["created_at_timestamp"]) > current_timestamp - 60 * 2:
                group_tg_ids.append(msg["group_tg_id"])
                num = num + 1
        
        if num > 3:
            reason = "2 分钟内发送 %s 个视频，超过 %s，%s" % (num, 3, user_tg_id)
            until_date = assist.get_restrict_time(1) # 禁言1天
            flag_restrict = True
            save_cheat = False
    
    for msg in msgs:
        print("group_tg_id %s，business_detail_type %s，created_at %s，has_at %s，is_photo %s，is_video %s" % (msg["group_tg_id"], msg["business_detail_type"], assist.timestamp2time(msg["created_at_timestamp"]), msg["has_at"], msg["is_photo"], msg["is_video"]))
    
    if group_tg_id_one:
        msgs = db_redis.msg_single_user_get(group_tg_id_one, user_tg_id)
        num = 0
        current_timestamp = assist.get_current_timestamp()
        for msg_created_at_timestamp in msgs:
            if int(msg_created_at_timestamp) > current_timestamp - limit_time:
                num = num + 1
        
        print("单个群 %s 秒内发送 %s，限制 %s" % (limit_time, num, limit_num))
    
    print(assist.timestamp2time(user_in_group_first_time))
    print(flag_restrict)
    print(reason)
    
check("6790521919", 2, -1001942356253)

