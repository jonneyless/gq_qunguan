import time

import helpp
import net
from lib import db
from lib import db_redis


def index(group_tg_id, user_tg_id, group, user):
    status_approve_one = int(group["status_approve_one"])
    status_approve_two = int(group["status_approve_two"])
    status_approve_three = int(group["status_approve_three"])
    status_approve_four = int(group["status_approve_four"])
    status_approve_five = int(group["status_approve_five"])
    status_approve_vip = int(group["status_approve_vip"])
    
    fullname = user["fullname"]
    username = user["username"]
    hasChinese = int(user["hasChinese"])

    bot_url = helpp.get_bot_url(group_tg_id, 1, True)

    # // status = 1 成功
    # // status = 2 等待中
    # // status = 3 失败

    # // reason = 5 官方账号或白名单
    # // reason = 4 骗子库黑名单用户
    # // reason = 1 含中文且已经进了两个公群
    # // reason = 2 名字含中文的自动审核通过
    # // reason = 3 名字不含中文的自动拒绝
    # // reason = 6 vip自动通过
    # // reason = 7 触发进群限制词的自动拒绝，触发二级进群限制词的，同时加入骗子库
    # // reason = 8 后台手动拒绝
    # // reason = 9 3天以前的自动拒绝
    # // reason = 10 后台手动通过
    # // reason = 11 疑似协议号短时间大量申请进群
    # // reason = 12 第一个群进群时间大于两个月的账号每天进的前5个群自动审核通过！
    # // reason = 100 广告互换群，群老板自动通过
    
    log_id = db.log_approve_save(group_tg_id, user_tg_id, user, 2)
    if log_id is None:
        return

    firstTime = helpp.get_user_in_group_first_time(user_tg_id)
    if firstTime < int(time.time()) + 3600 * 24 * 60:
        todayGroupCount = db_redis.todayUserJoinGroupCount(user_tg_id)
        if todayGroupCount < 5:
            bot_url = helpp.get_bot_url(group_tg_id, 3)

            flag, description = net.approveChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
            if flag:
                db.log_approve_update(log_id, 1, 12)
                db_redis.todayUserJoinGroupCount(user_tg_id, True)

            print("old_user_auto %s %s %s %s %s %s" % (group_tg_id, user_tg_id, username, fullname, flag, description))

            return

    if status_approve_five == 1:
        if helpp.is_official_white(user_tg_id):
            bot_url = helpp.get_bot_url(group_tg_id, 3)
            
            flag, description = net.approveChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
            if flag:
                db.log_approve_update(log_id, 1, 5)
                
            print("is_official_white %s %s %s %s %s %s" % (group_tg_id, user_tg_id, username, fullname, flag, description))
            
            return
    
    if status_approve_vip == 1:
        if helpp.is_vip_svip(user_tg_id):
            bot_url = helpp.get_bot_url(group_tg_id, 3)
            
            flag, description = net.approveChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
            if flag:
                db.log_approve_update(log_id, 1, 6)
            
            print("is_vip_svip %s %s %s %s %s %s" % (group_tg_id, user_tg_id, username, fullname, flag, description))
            
            return
    
    if status_approve_four == 1:
        if db.cheats_special_one(user_tg_id) or db.cheat_one(user_tg_id):
            bot_url = helpp.get_bot_url(group_tg_id, 3)
            
            flag, description = net.declineChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
            if flag:
                db.log_approve_update(log_id, 3, 4)
            
            print("cheats_special_one %s %s %s %s %s %s" % (group_tg_id, user_tg_id, username, fullname, flag, description))
            
            return
    
    fullname_restrict_word = helpp.has_fullname_restrict_word(fullname)
    if fullname_restrict_word is not None:
        name = fullname_restrict_word["name"]
        reason = "昵称中包含敏感词：%s" % name
        
        db.cheat_save(user_tg_id, reason)
        
        bot_url = helpp.get_bot_url(group_tg_id, 3)
        
        flag, description = net.declineChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
        if flag:
            db.log_approve_update(log_id, 3, 7)
        
        print("fullname_restrict_word %s %s %s %s %s %s，%s" % (group_tg_id, user_tg_id, username, fullname, flag, description, name))
        
        return
    
    username_restrict_word = helpp.has_username_restrict_word(username)
    if username_restrict_word is not None:
        name = username_restrict_word["name"]
        reason = "用户名中包含敏感词：%s" % name
        
        db.cheat_save(user_tg_id, reason)
        
        bot_url = helpp.get_bot_url(group_tg_id, 3)
        
        flag, description = net.declineChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
        if flag:
            db.log_approve_update(log_id, 3, 7)
            
        print("username_restrict_word %s %s %s %s %s %s，%s" % (group_tg_id, user_tg_id, username, fullname, flag, description, name))

        return

    intro = net.getBio(bot_url, user_tg_id)
    intro_restrict_word = helpp.has_intro_restrict_word(intro)
    if intro_restrict_word is not None:
        name = intro_restrict_word["name"]
        reason = "用户简介中包含敏感词：%s" % name

        db.cheat_save(user_tg_id, reason)

        bot_url = helpp.get_bot_url(group_tg_id, 3)

        flag, description = net.declineChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
        if flag:
            db.log_approve_update(log_id, 3, 7)

        print("intro_restrict_word %s %s %s %s %s %s，%s" % (group_tg_id, user_tg_id, username, fullname, flag, description, name))

        return
    
    if status_approve_one == 1 and hasChinese == 1:
        group_tg_ids = db.log_invite_link_success_not_auto(user_tg_id)
        if len(group_tg_ids) >= 2:
            bot_url = helpp.get_bot_url(group_tg_id, 3)
            
            flag, description = net.approveChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
            if flag:
                db.log_approve_update(log_id, 1, 1)
                
            print("One approve %s %s %s %s %s %s，%s" % (group_tg_id, user_tg_id, username, fullname, flag, description, len(group_tg_ids)))
            
            return
        
    if status_approve_two == 1 and hasChinese == 1:
        bot_url = helpp.get_bot_url(group_tg_id, 3)
        
        flag, description = net.approveChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
        if flag:
            db.log_approve_update(log_id, 1, 2)
        
        print("Two approve %s %s %s %s %s %s" % (group_tg_id, user_tg_id, username, fullname, flag, description))
        
        return
    
    if status_approve_three == 1 and hasChinese == 2:
        bot_url = helpp.get_bot_url(group_tg_id, 3)
        
        flag, description = net.declineChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
        if flag:
            db.log_approve_update(log_id, 3, 3)
            
        print("Three decline %s %s %s %s %s %s" % (group_tg_id, user_tg_id, username, fullname, flag, description))
        
        return
    
    group_tg_ids30 = db.user_group_new30(user_tg_id)
    # 判断过了：2个以上的业务类型群
    if len(group_tg_ids30) > 2:
        if helpp.is_session_user(user_tg_id):
            bot_url = helpp.get_bot_url(group_tg_id, 3)
            
            flag, description = net.declineChatJoinRequestWrap(bot_url, group_tg_id, user_tg_id)
            if flag:
                db.log_approve_update(log_id, 3, 11)
            
            print("%s %s %s session，%s" % (user_tg_id, fullname, username, len(group_tg_ids30)))

            for group_tg_id30 in group_tg_ids30:
                reason = "疑似协议号短时间大量申请进群"
                print("%s %s %s %s，%s" % (group_tg_id30, user_tg_id, fullname, username, reason))
                
                db_redis.tgData_set({
                    "typee": "restrict",
                    "group_tg_id": group_tg_id30,
                    "user_tg_id": user_tg_id,
                    "reason": reason,
                })
            
            return
        else:
            print("%s %s %s not session" % (user_tg_id, fullname, username))
            
    print("wait %s %s %s %s" % (group_tg_id, user_tg_id, fullname, username))

