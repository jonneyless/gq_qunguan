import time
import re
import assist
import helpp
import net
from lib import db
from lib import db_redis
import template
import httpp


def index(group_tg_id, user_tg_id, msg_tg_id, text, group, reply_message_tg_id, reply_user_tg_id, reply_text, entity_usernames, entity_user_tg_ids, created_at_timestamp):
    title = group["title"]
    group_flag = int(group["flag"])
    search_sort = group["search_sort"]
    
    reply_message_tg_id = int(reply_message_tg_id)

    if group_flag == 4:
        if text == "开启权限":
            official = db.official_one(user_tg_id)
            if official:
                bot_url = helpp.get_bot_url(group_tg_id, 1, True)
                
                flag = net.promote_admin(bot_url, group_tg_id, user_tg_id, False)
                if flag:
                    db.group_admin_save(group_tg_id, user_tg_id)
                    
                    message_id = net.sendMessageOne(bot_url, group_tg_id, "开启成功")
            return
    
        if int(reply_user_tg_id) > 0 and text.find("设置管理") == 0:
            custom_title = text.replace("设置管理", "")
                
            official = db.official_one(user_tg_id)
            if official:
                bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
                # bot_url, chat_id, user_id, title, short=True
                flag = net.game_promote_admin_title(bot_url, group_tg_id, reply_user_tg_id, custom_title, True)
                if flag:
                    db.group_admin_save(group_tg_id, reply_user_tg_id, custom_title)
                    net.sendMessageOne(bot_url, group_tg_id, template.msg_ok())
                else:
                    net.sendMessageOne(bot_url, group_tg_id, template.msg_error())
        
        
        if int(reply_user_tg_id) > 0 and text.find("设置媒体管理") == 0:
            custom_title = text.replace("设置媒体管理", "")
                
            official = db.official_one(user_tg_id)
            if official:
                bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
                # bot_url, chat_id, user_id, title, short=True
                flag = net.game_promote_admin_title(bot_url, group_tg_id, reply_user_tg_id, custom_title, False)
                if flag:
                    db.group_admin_save(group_tg_id, reply_user_tg_id, custom_title)
                    net.sendMessageOne(bot_url, group_tg_id, template.msg_ok())
                else:
                    net.sendMessageOne(bot_url, group_tg_id, template.msg_error())

        # if text == "验群" or text == "验证":
        #     bot_url = helpp.get_bot_url(group_tg_id, 1, True)
        #     if bot_url is None:
        #         return
            
        #     net.send_and_delete_last(bot_url, group_tg_id, template.msg_notice_game_group_true(), "gameYanzheng")
    
        return


    if text == "删除" and reply_message_tg_id > 0:
        ope_flag = False
        official = db.official_one(user_tg_id)
        if official:
            ope_flag = True
        else:
            is_admin = db.group_admin_one(group_tg_id, user_tg_id)
            if is_admin:
                ope_flag = True
        
        if ope_flag:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            net.deleteMessageOne(bot_url, group_tg_id, reply_message_tg_id)
            net.deleteMessageOne(bot_url, group_tg_id, msg_tg_id)
            
        return
        
        
    if text == "已退押":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            db.group_set_xianjing_status(group_tg_id, 1)
            m_id = net.sendMessageOne(bot_url, group_tg_id, "已开启")
            httpp.flushGroup(group_tg_id)
            time.sleep(2)
            net.deleteMessageOne(bot_url, group_tg_id, m_id)
        return
        
    if text == "已开群":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            db.group_set_xianjing_status(group_tg_id, 2)
            m_id= net.sendMessageOne(bot_url, group_tg_id, "已关闭")
            httpp.flushGroup(group_tg_id)
            time.sleep(2)
            net.deleteMessageOne(bot_url, group_tg_id, m_id)
        return
            
    if text[0:2] == "禁言":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            if len(entity_user_tg_ids) > 0:
                for entity_user_tg_id in entity_user_tg_ids:
                    flag, description = net.restrictChatMemberWrap(bot_url, group_tg_id, entity_user_tg_id)
                    if flag:
                        db.user_group_new_update(group_tg_id, entity_user_tg_id, 2, 1, 2, 1)
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                    else:
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
            elif len(entity_usernames) > 0:
                for entity_username in entity_usernames:
                    user = db.user_one_by_username(entity_username)
                    if user is not None:
                        o = db.official_one(user["tg_id"])
                        if o:
                            info = "%s 是官方账号无法操作" % entity_username
                            net.sendMessageOne(bot_url, group_tg_id, info, msg_tg_id)
                            return
                        flag, description = net.restrictChatMemberWrap(bot_url, group_tg_id, user["tg_id"])
                        if flag:
                            db.user_group_new_update(group_tg_id, user["tg_id"], 2, 1, 2, 1)
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                        else:
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
                            
        return
    
    if text[0:2] == "解禁":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            if len(entity_user_tg_ids) > 0:
                for entity_user_tg_id in entity_user_tg_ids:
                    flag, description = net.cancelRestrictChatMemberWrap(bot_url, group_tg_id, entity_user_tg_id)
                    if flag:
                        db.user_group_new_update(group_tg_id, entity_user_tg_id, 2, 1, 1, 1)
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                    else:
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
            elif len(entity_usernames) > 0:
                for entity_username in entity_usernames:
                    user = db.user_one_by_username(entity_username)
                    if user is not None:
                        o = db.official_one(user["tg_id"])
                        if o:
                            info = "%s 是官方账号无法操作" % entity_username
                            net.sendMessageOne(bot_url, group_tg_id, info, msg_tg_id)
                            return
                        flag, description = net.cancelRestrictChatMemberWrap(bot_url, group_tg_id, user["tg_id"])
                        if flag:
                            db.user_group_new_update(group_tg_id, user["tg_id"], 2, 1, 1, 1)
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                        else:
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
                            
        return
    
    if text[0:2] == "踢出":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            if len(entity_user_tg_ids) > 0:
                for entity_user_tg_id in entity_user_tg_ids:
                    flag, description = net.banChatMemberWrap(bot_url, group_tg_id, entity_user_tg_id)
                    if flag:
                        db.user_group_new_update(group_tg_id, entity_user_tg_id, 2, 2, 1, 2)
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                    else:
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
            elif len(entity_usernames) > 0:
                for entity_username in entity_usernames:
                    user = db.user_one_by_username(entity_username)
                    if user is not None:
                        o = db.official_one(user["tg_id"])
                        if o:
                            info = "%s 是官方账号无法操作" % entity_username
                            net.sendMessageOne(bot_url, group_tg_id, info, msg_tg_id)
                            return
                        flag, description = net.banChatMemberWrap(bot_url, group_tg_id, user["tg_id"])
                        if flag:
                            db.user_group_new_update(group_tg_id, user["tg_id"], 2, 2, 1, 2)
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                        else:
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
                            
        return
    
    if text[0:2] == "解封":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 2, True)
            
            if len(entity_user_tg_ids) > 0:
                for entity_user_tg_id in entity_user_tg_ids:
                    flag, description = net.unbanChatMemberWrap(bot_url, group_tg_id, entity_user_tg_id)
                    if flag:
                        db.user_group_new_update(group_tg_id, entity_user_tg_id, 2, 2, 1, 1)
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                    else:
                        net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
            elif len(entity_usernames) > 0:
                for entity_username in entity_usernames:
                    user = db.user_one_by_username(entity_username)
                    if user is not None:
                        o = db.official_one(user["tg_id"])
                        if o:
                            info = "%s 是官方账号无法操作" % entity_username
                            net.sendMessageOne(bot_url, group_tg_id, info, msg_tg_id)
                            return
                        flag, description = net.unbanChatMemberWrap(bot_url, group_tg_id, user["tg_id"])
                        if flag:
                            db.user_group_new_update(group_tg_id, user["tg_id"], 2, 2, 1, 1)
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), msg_tg_id)
                        else:
                            net.sendMessageOne(bot_url, group_tg_id, template.msg_error(), msg_tg_id)
                            
        return
    
    if text.find("设置公群群名") >= 0:
        text_temp = text
        text_temp = text_temp.replace("设置公群群名", "")
        text_temp = text_temp.replace("\n", "")
        
        title_old = title
        title_new = text_temp
        
        num_old = -1
        num_new = -1

        try:
            pattern = re.compile("公群(\d*)")
            title_old_temp = title_old.replace(" ", "")
            result = re.search(pattern, title_old_temp)
            if result is not None:
                num_old = int(result.group(1))
                
            pattern = re.compile("公群(\d*)")
            title_new_temp = title_new.replace(" ", "")
            result = re.search(pattern, title_new_temp)
            if result is not None:
                num_new = int(result.group(1))
        except Exception as e:
            pass
    
        if num_old < 0 or num_new < 0:
            return
        
        official = db.official_one(user_tg_id)
        if not official:
            return
        
        bot_url = helpp.get_bot_url(group_tg_id, 1, True)
        
        if num_old == num_new and num_new > 0:
            flag = net.setChatTitle(bot_url, group_tg_id, title_new)
            if flag:
                net.sendMessageOne(bot_url, group_tg_id, "修改成功")
                db_redis.checkPinMessage_set({
                    "type": "change_title",
                    "chat_id": group_tg_id,
                    "new_chat_title": title_new,
                    "old_chat_title": title_old,
                })
                
                print("sj change_title %s %s" % (group_tg_id, title_new))
                
                db_redis.sj_msg_set({
                    "group_tg_id": group_tg_id,
                    "created_at_timestamp": assist.get_current_timestamp(),
                    "created_at": assist.get_current_time(),
                    "title_new": title_new,
                })
            else:
                net.sendMessageOne(bot_url, group_tg_id, "修改失败，请稍后重试")
        else:
            net.sendMessageOne(bot_url, group_tg_id, "前后群编号不同，请在后台修改")
            
        return
    
    if text == "显示公群群名":
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            net.sendMessageOne(bot_url, group_tg_id, title, msg_tg_id)
            
        return
    
    if reply_message_tg_id > 0:
        if text == "置顶" or text == "取消置顶" or text == "设置简介":
            official = db.official_one(user_tg_id)
            if official:
                bot_url = helpp.get_bot_url(group_tg_id, 1, True)
                
                if text == "置顶":
                    net.pinChatMessage(bot_url, group_tg_id, reply_message_tg_id)
                    db_redis.checkPinMessage_set({
                        "chat_id": group_tg_id,
                        "text": reply_text,
                    })
                if text == "取消置顶":
                    net.unpinChatMessage(bot_url, group_tg_id, reply_message_tg_id)
                if text == "设置简介":
                    net.setChatDescription(bot_url, group_tg_id, reply_text)
                    net.sendMessageOne(bot_url, group_tg_id, template.msg_ok(), reply_message_tg_id)
        
            return
    
    # entity_usernames = assist.unique_list(entity_usernames)
    # if len(entity_usernames) > 0:
    #     official_num = 0
        
    #     for entity_username in entity_usernames:
    #         user = db.official_one_by_username(entity_username)
    #         if user is not None:
    #             official_num = official_num + 1
                
    #     if official_num > 0:
    #         current_timestamp = assist.get_current_timestamp()
            
    #         num = 0
    #         msgs = helpp.at_official_set_get(group_tg_id, user_tg_id, created_at_timestamp)
    #         for msg_created_at_timestamp in msgs:
    #             if int(msg_created_at_timestamp) > current_timestamp - 180:
    #                 num = num + 1
                    
    #         if num > 3:
    #             bot_url = helpp.get_bot_url(group_tg_id, 1)
                
    #             net.send_and_delete_last(bot_url, group_tg_id, "小二正在火速赶来，请客官稍安勿躁，不要短时间连续@。", "at_official_180_3")
        
    #     if official_num >= 2:
    #         bot_url = helpp.get_bot_url(group_tg_id, 1)
            
    #         net.send_and_delete_last(bot_url, group_tg_id, "请只@一位负责处理该事务的工作人员，不要同时@多个工作人员，以免多个工作人员都前来围观，造成资源浪费111。", "at_official_2")
        
    if text == "恢复权限":
        # 给非官方管理，4个权限
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            admins = db.get_group_not_official_admin(group_tg_id)
            admins_empty_num = 0
            admins_empty_num_ok = 0
            
            for admin_item in admins:
                admins_empty_num = admins_empty_num + 1 
                
                flag = net.recover_admin(bot_url, group_tg_id, admin_item["user_id"])
                if flag:
                    admins_empty_num_ok = admins_empty_num_ok + 1
                
            info = "成功"
            if admins_empty_num != admins_empty_num_ok:
                info = "部分管理操作失败，请重试"
                
            m_id = net.sendMessageOne(bot_url, group_tg_id, info)
            # time.sleep(3)
            # net.deleteMessageOne(bot_url, group_tg_id, m_id)
            
        return
    
    if text == "回收权限":
        # 给非官方管理，空管理
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            admins = db.get_group_not_official_admin(group_tg_id)

            admins_empty_num = 0
            admins_empty_num_ok = 0
            
            for admin_item in admins:
                admins_empty_num = admins_empty_num + 1 
                
                flag = net.promote_empty_admin(bot_url, group_tg_id, admin_item["user_id"])
                if flag:
                    admins_empty_num_ok = admins_empty_num_ok + 1
                
            info = "成功"
            if admins_empty_num != admins_empty_num_ok:
                info = "部分管理操作失败，请重试"
                
            m_id = net.sendMessageOne(bot_url, group_tg_id, info)
            # time.sleep(3)
            # net.deleteMessageOne(bot_url, group_tg_id, m_id)
            
        return
    
    if text == "回收管理":
        # 移除非官方 管理
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            admins = db.get_group_not_official_admin(group_tg_id)
            admins_empty_num = 0
            admins_empty_num_ok = 0
            
            for admin_item in admins:
                admins_empty_num = admins_empty_num + 1 
                
                flag = net.remove_admin(bot_url, group_tg_id, admin_item["user_id"])
                if flag:
                    admins_empty_num_ok = admins_empty_num_ok + 1
                
            info = "成功"
            if admins_empty_num != admins_empty_num_ok:
                info = "部分管理操作失败，请重试"
                
            m_id = net.sendMessageOne(bot_url, group_tg_id, info)
            # time.sleep(3)
            # net.deleteMessageOne(bot_url, group_tg_id, m_id)
            
        return
    
    if text == "设置群老板" and int(reply_user_tg_id) > 0:
        custom_title = "本公群老板，小心骗子假冒"
        
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
        
            group_admin_title = db.group_admin_title_one(group_tg_id, 1)
            if group_admin_title is not None:
                net.sendMessageOne(bot_url, group_tg_id, "设置失败，群内已有群老板")
                return
        
            flag = net.promote_admin_title(bot_url, group_tg_id, reply_user_tg_id, custom_title)
            if flag:
                db.group_admin_save(group_tg_id, reply_user_tg_id, custom_title)
                net.sendMessageOne(bot_url, group_tg_id, template.msg_ok())
            else:
                net.sendMessageOne(bot_url, group_tg_id, template.msg_error())
                            
        return

    if text == "设置业务员" and int(reply_user_tg_id) > 0:
        custom_title = "本公群业务员，小心骗子假冒"
        
        official = db.official_one(user_tg_id)
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
        
            flag = net.promote_admin_title(bot_url, group_tg_id, reply_user_tg_id, custom_title)
            if flag:
                db.group_admin_save(group_tg_id, reply_user_tg_id, custom_title)
                net.sendMessageOne(bot_url, group_tg_id, template.msg_ok())
            else:
                net.sendMessageOne(bot_url, group_tg_id, template.msg_error())
                            
        return
        
    if text == "开启权限":
        official = db.official_one(user_tg_id)
        
        if official:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            flag = net.promote_admin(bot_url, group_tg_id, user_tg_id, False)
            if flag:
                db.group_admin_save(group_tg_id, user_tg_id)
                
                message_id = net.sendMessageOne(bot_url, group_tg_id, "开启成功")
                
                # time.sleep(3)
                
                # net.deleteMessageOne(bot_url, group_tg_id, msg_tg_id)
                # net.deleteMessageOne(bot_url, group_tg_id, message_id)
                
        return
    
    if text == "上课" or text == "开群":
        admin = db.group_admin_one(group_tg_id, user_tg_id)
        if admin:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            if title.find("暂停") > 0 or title.find("纠纷") > 0 or title.find("退押") > 0 or title.find("转押") > 0 or title.find("业务变更中") > 0:
                net.send_and_delete_last(bot_url, group_tg_id, "当前公群处于暂停交易状态，擅自交易后果自负，请群老板或业务员处理完相关事务后再重新开群", "shangke")
            else:
                flag = net.setChatPermissions(bot_url, group_tg_id, True)
                if flag:
                    db.group_set_open_status(group, 1)
                    net.sendMessageOne(bot_url, group_tg_id, template.msg_group_open())
                else:
                    message_id = net.sendMessageOne(bot_url, group_tg_id, template.msg_error())
                    # time.sleep(1)
                    # net.deleteMessageOne(bot_url, group_tg_id, message_id)
                    
        return
        
    if text == "下课" or text == "关群":
        admin = db.group_admin_one(group_tg_id, user_tg_id)
        if admin:
            bot_url = helpp.get_bot_url(group_tg_id, 1, True)
            
            flag = net.setChatPermissions(bot_url, group_tg_id, False)
            if flag:
                db.group_set_open_status(group, 2)
                net.sendMessageOne(bot_url, group_tg_id, template.msg_group_close())
            else:
                message_id = net.sendMessageOne(bot_url, group_tg_id, template.msg_error())
                # time.sleep(1)
                # net.deleteMessageOne(bot_url, group_tg_id, message_id)
                
        return
    
    # if text[0:5] == "设置进群语":
    #     info = text[5:]
    #     if len(info) > 0:
    #         official = db.official_one(user_tg_id)
    #         if official:
    #             bot_url = helpp.get_bot_url(group_tg_id, 1)
                
    #             db.group_set_welcome_info(group["id"], info)
    #             net.sendMessageOne(bot_url, group_tg_id, template.msg_group_set_welcome_info(group["title"], info))
                
    #     return

    # if text == "显示进群语":
    #     official = db.official_one(user_tg_id)
    #     if official:
    #         bot_url = helpp.get_bot_url(group_tg_id, 1)
            
    #         net.sendMessageOne(bot_url, group_tg_id, template.msg_group_show_welcome_info(group["title"], group["welcome_info"]))
    #     return

    # if text == "关闭进群语":
    #     official = db.official_one(user_tg_id)
    #     if official:
    #         db.group_close_welcome_info(group["id"])
            
    #         bot_url = helpp.get_bot_url(group_tg_id, 1, True)

    #         net.sendMessageOne(bot_url, group_tg_id, template.msg_group_close_welcome_info())
            
    #     return
    
    # if text == "真假公群":
    #     if group_flag == 2 or group_flag == 4:
    #         bot_url = helpp.get_bot_url(group_tg_id, 1)
            
    #         net.sendMessageOne(bot_url, group_tg_id, template.msg_check_group_true(), msg_tg_id)
        
    #     return
    
    # if group_flag == 2 and group["business_type"] == 10:
    #     flag = db_redis.user_reply_text_get(group_tg_id, user_tg_id)
    #     if flag is None:
    #         reply_data = db.reply_text_get()
    #         if reply_data is not None:
    #             reply_data_key = reply_data["keyy"]
    #             reply_data_val = reply_data["val"]
                
    #             reply_data_key = reply_data_key.split(",")
                
    #             for item in reply_data_key:
    #                 if len(item) > 0:
    #                     if text.find(item) >= 0:
    #                         bot_url = helpp.get_bot_url(group_tg_id, 1)
                            
    #                         net.sendMessageOne(bot_url, group_tg_id, reply_data_val, msg_tg_id)
                            
    #                         db_redis.user_reply_text_set(group_tg_id, user_tg_id)
                                
    #                         return

