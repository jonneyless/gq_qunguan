import threading

import assist
import helpp
from lib import db
from lib import db_redis
from config import business_detail_types_no_limit

lock = threading.Lock()


def index(group_tg_id, user_tg_id, flag, business_detail_type, created_at_timestamp, has_at, fullname_is_en, is_photo, is_video):
    # flag_continue 除了踢出都继续判断
    flag_continue = True
    
    if int(flag) == 2 and (int(business_detail_type) not in business_detail_types_no_limit):
        limit_no_vip_restrict_time = helpp.get_config_limit_no_vip_restrict_time()
        limit_no_vip_num = helpp.get_config_limit_no_vip_num()
        limit_no_vip_type = helpp.get_config_limit_no_vip_type()
        limit_no_vip_time = helpp.get_config_limit_no_vip_time()
        
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
        with lock:
            # 检测是否超出限制
            msgs = helpp.msg_user_set_get(group_tg_id, user_tg_id, business_detail_type, created_at_timestamp, has_at, is_photo, is_video)
            
            if not flag_restrict:
                group_tg_ids = []
                for msg in msgs:
                    if int(msg["created_at_timestamp"]) > current_timestamp - limit_all_time:
                        group_tg_ids.append(msg["group_tg_id"])
                        
                group_tg_ids = set(group_tg_ids)
                if len(group_tg_ids) > limit_all_group_num:
                    flag_restrict = True
                    reason = "%s 秒内在 %s 个群发送信息，超过 %s，禁言 %s 天，%s" % (limit_all_time, len(group_tg_ids), limit_all_group_num, limit_cancel_restrict, user_tg_id)
                    # print(reason)
            
                    until_date = assist.get_restrict_time(limit_cancel_restrict) # 禁言几天
                    save_cheat = True
    
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
                    # if int(msg["created_at_timestamp"]) > current_timestamp - 60 * 5:
                    if int(msg["created_at_timestamp"]) > current_timestamp - limit_no_vip_time:
                        types.append(msg["business_detail_type"])
                        group_tg_ids.append(msg["group_tg_id"])
                        
                types = set(types)
                group_tg_ids = set(group_tg_ids)
                
                # if len(types) > 3 and len(group_tg_ids) > 20:
                if len(types) > limit_no_vip_type and len(group_tg_ids) > limit_no_vip_num:
                    if not helpp.is_vip_svip(user_tg_id):
                        flag_restrict = True
                        save_cheat = False
                        reason = "%s秒内发言群数 %s 大于 %s 个，群组类型 %s 大于 %s 种 %s " % (limit_no_vip_time, len(group_tg_ids), limit_no_vip_num, len(types), limit_no_vip_type, user_tg_id)
                        until_date = assist.get_restrict_time(limit_no_vip_restrict_time) # 禁言7天
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
                    # save_cheat = False
        
        if flag_restrict:
            flag_continue = True
            # db_redis.msg_user_del(user_tg_id)
            
            # 删除所有信息，禁言，加入黑名单
            # if save_cheat or True:
            if save_cheat:
                db.cheat_save(user_tg_id, reason)
            
            group_tg_ids = list(set(group_tg_ids))
            # group_tg_ids = db.user_group_new_for_restrict(user_tg_id)
            
            # print({
            #     "user_in_group_first_time": assist.timestamp2time(user_in_group_first_time),
            #     "group_tg_id": group_tg_ids,
            #     "user_tg_id": user_tg_id,
            #     "reason": reason,
            # })
            
            print("%s，进群时间 %s，群数 %s，%s" % (user_tg_id, assist.timestamp2time(user_in_group_first_time), len(group_tg_ids), reason))
                        
            for group_tg_id_temp in group_tg_ids:
                db_redis.tgData_set({
                    "typee": "deleteAll",
                    "group_tg_id": group_tg_id_temp,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })
                
                if db_redis.temp_restrict_user_get(group_tg_id_temp, user_tg_id):
                    print("==>10秒内禁言过这个群 %s %s" % (group_tg_id_temp, user_tg_id))
                else:
                    db_redis.temp_restrict_user_set(group_tg_id_temp, user_tg_id)
                    
                    db_redis.tgData_set({
                        "typee": "restrict",
                        "group_tg_id": group_tg_id_temp,
                        "user_tg_id": user_tg_id,
                        "reason": reason,
                        "until_date": until_date,
                    })
        
    return flag_continue
            