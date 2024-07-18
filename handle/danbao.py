import time
import re
import assist
import helpp
import net
from lib import db
from lib import db_redis
import template


def index(group_tg_id, user_tg_id, msg_tg_id, text, group, created_at_timestamp):
    title = group["title"]
    group_flag = int(group["flag"])
    business_detail_type = int(group["business_detail_type"])
    group_num = group["group_num"]

    # if int(group_tg_id) != -1001846199438:
    #     return

    if group_flag != 2:
        return

    official = db.official_one(user_tg_id)
    if not official:
        return

    bot_url = helpp.get_bot_url(group_tg_id, 1, True)
    
    if text == "担保开启":
        log = db.danbao_one(group_tg_id)
        if log is not None:
            net.sendMessageOne(bot_url, group_tg_id, "当前公群存在开启中的担保记录", msg_tg_id)
            return
        
        admins = db.group_admin_one_all(group_tg_id)
        db.danbao_save(group, admins)
        
        net.sendMessageOne(bot_url, group_tg_id, "担保开启成功", msg_tg_id)
        
        return
    
    if text == "担保刷新":
        log = db.danbao_one(group_tg_id)
        if log is None:
            net.sendMessageOne(bot_url, group_tg_id, "当前公群不存在开启中的担保记录", msg_tg_id)
            return
        
        admins = db.group_admin_one_all(group_tg_id)
        db.danbao_update(log, group, admins)
        
        net.sendMessageOne(bot_url, group_tg_id, "担保刷新成功", msg_tg_id)
        
        return
    
    if text.find("改月费") == 0:
        text_temp = text.lower()
        text_temp = text_temp.replace("改月费", "")

        try:
            if assist.is_number(text_temp) and float(text_temp) > 0:
                log = db.danbao_one(group_tg_id)
                if log is None:
                    net.sendMessageOne(bot_url, group_tg_id, "当前公群不存在开启中的担保记录", msg_tg_id)
                    return
                
                db.danbao_update_yuefei(log["id"], text_temp)
                db.log_danbao_change_yuefei_save(log["id"], group_tg_id, log["yuefei"], text_temp, user_tg_id)
                
                net.sendMessageOne(bot_url, group_tg_id, "月费修改成功", msg_tg_id)
        except:
            print("error 改月费 %s | %s" % (text_temp, text))
            
        return
    
    if text.find("#群号") >= 0 and text.find("#下押") >= 0 and text.find("#地址") >= 0:
        log = db.danbao_one(group_tg_id)
        if log is None:
            return
        
        yuefei = int(log["yuefei"])
        yuefei_day = int(log["yuefei_day"])
        
        if yuefei <= 0 or yuefei_day <= 0:
            # net.sendMessageOne(bot_url, group_tg_id, "", msg_tg_id)
            pass

        flag, text_yue_no_arr, text_yue_have_arr, remark = helpp.has_yuefei(log)  
        
        text_show = "担保开始时间：%s\n" % log["created_at"]
        text_show += "月费金额：%s\n" % log["yuefei"]
        text_show += "月费收取日：每月%s日\n" % log["yuefei_day"]
        if remark > 0:
            text_show += "免除%s月月费\n" % remark
            
        text_show += "\n"
        
        if len(text_yue_have_arr) > 0:
            text_show += "以下月费已收取\n"
            for yue in text_yue_have_arr:
                text_show += "%s月," % yue
            
            text_show += "\n"
        
        if len(text_yue_no_arr) > 0:
            text_show += "以下月费还未结清\n"
            for yue in text_yue_no_arr:
                text_show += "%s月," % yue
            
            text_show += "\n"
        
        net.sendMessageOne(bot_url, group_tg_id, text_show, msg_tg_id)
                
        return
        
    if text == "担保关闭":
        log = db.danbao_one(group_tg_id)
        if log is None:
            net.sendMessageOne(bot_url, group_tg_id, "当前公群不存在开启中的担保记录", msg_tg_id)
            return

        db.danbao_over(log["id"])
        db.danbao_yuefei_over(log["num"])
        
        title_temp = title.upper()
        title_new = "公群%s 已退押" % group_num 
        if title_temp.find("VIP") >= 0:
            title_new = "VIP公群%s 已退押" % group_num 
        
        flag_title = net.setChatTitle(bot_url, group_tg_id, title_new)
        if flag_title:
            db_redis.checkPinMessage_set({
                "type": "change_title",
                "chat_id": group_tg_id,
                "new_chat_title": title_new,
                "old_chat_title": title,
            })
            
        flag_desc = net.setChatDescription(bot_url, group_tg_id, "")
        
        flag_admin = True
        admins = db.get_group_not_official_admin(group_tg_id)
        
        admins_empty_num = 0
        admins_empty_num_ok = 0
        
        for admin_item in admins:
            admins_empty_num = admins_empty_num + 1 
            
            flag = net.remove_admin(bot_url, group_tg_id, admin_item["user_id"])
            if flag:
                admins_empty_num_ok = admins_empty_num_ok + 1
            
        if admins_empty_num != admins_empty_num_ok:
            flag_admin = False

        flag_jz = net.removeNotOfficialAdmin(group_tg_id)
        
        db.group_trade_report_del(group_tg_id)
        
        flag_unpin = net.unpinAllChatMessages(bot_url, group_tg_id)
        
        text_show = "担保关闭成功\n\n"
        
        if flag_title:
            text_show += "群名修改成功\n"
        else:
            text_show += "群名修改失败\n"
        
        if flag_desc:
            text_show += "简介删除成功\n"
        else:
            text_show += "简介删除失败\n"
            
        if flag_admin:
            text_show += "删除非官方管理成功\n"
        else:
            text_show += "删除非官方管理失败\n"
        
        if flag_jz:
            text_show += "清理记账机器人jz99bot操作人成功\n"
        else:
            text_show += "清理记账机器人jz99bot操作人失败\n"
            
        text_show += "清理报备数据成功\n"
        
        if flag_unpin:
            text_show += "所有置顶信息取消成功\n"
        else:
            text_show += "所有置顶信息取消失败\n"
        
        net.sendMessageOne(bot_url, group_tg_id, text_show, msg_tg_id)
        
        text_show1 = "更多公群关注公群导航 @hwgq，您想找的公群这里都有，群列表每天更新！如您需要资源对接，请联系 @hwdb 选择资源对接窗口。"
        message_id = net.sendMessageOne(bot_url, group_tg_id, text_show1)
        if int(message_id) > 0:
            net.pinChatMessage(bot_url, group_tg_id, message_id)
        
        text_show2 = """尊敬的客户，本群已完成退押办理
    ✨  感恩相遇，不负信任✨
若日后有需要再开群，请联系在线客服 @hwdb 
若需要其他资源对接，请联系资源小赵 @hwdb 
 汇旺担保祝您：财源广进💰好运连连
           期待下次为您服务"""
        net.sendMessageOne(bot_url, group_tg_id, text_show2)
        
