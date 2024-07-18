import threading

import assist
import helpp
import net
from lib import db
from lib import db_redis
import config
import template


def index(group_tg_id, user_tg_id, message_tg_id, user, info, hasChinese, forward_from, has_hide_link, flag, trade_type):
    flag_continue = True
    flag_delete = False
    
    if forward_from == 1:
        flag_delete = True
        print("%s %s 转发消息" % (group_tg_id, user_tg_id))
        db_redis.tgData_set({
            "typee": "delete",
            "group_tg_id": group_tg_id,
            "user_tg_id": user_tg_id,
            "message_tg_id": message_tg_id,
            "reason": "转发消息",
        })
    
    if has_hide_link == 1:
        flag_delete = True
        reason = "信息包含隐藏链接"
        print("信息包含隐藏链接 %s %s %s" % (group_tg_id, user_tg_id, info[0:10]))
        
        if not flag_delete:
            db_redis.tgData_set({
                "typee": "delete",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": reason,
            })
        db_redis.tgData_set({
            "typee": "ban",
            "group_tg_id": group_tg_id,
            "user_tg_id": user_tg_id,
            "reason": reason,
        })
    
    info_no_other = info.replace(" ", "")
    info_no_other = info_no_other.replace("\n", "")
    
    info_len = len(info)
    info_no_other_len = len(info_no_other)
    
    if not flag_delete:
        config_text_len_limit = helpp.get_config_text_len_limit()
        if assist.has_bank(info):
            config_text_len_limit = config.limit_text_len_bank
    
        if info_len > config_text_len_limit:
            flag_delete = True
            db_redis.tgData_set({
                "typee": "delete",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": "信息过长",
            })
    
    if not flag_delete:
        emoji_num = assist.get_emoji_num(info_no_other)
        if emoji_num > 3:
            flag_delete = True
            print("信息中超过3个emoji表情 %s %s %s" % (group_tg_id, user_tg_id, info_no_other[0:10]))
            db_redis.tgData_set({
                "typee": "delete",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": "信息中超过3个emoji表情",
            })
        
        if not flag_delete:
            if emoji_num > 0 and emoji_num == info_no_other_len:
                flag_delete = True
                print("信息中只有emoji表情 %s %s %s" % (group_tg_id, user_tg_id, info_no_other[0:10]))
                db_redis.tgData_set({
                    "typee": "delete",
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "message_tg_id": message_tg_id,
                    "reason": "信息中只有emoji表情",
                })
        
    if hasChinese == 2:
        has_other_lang_flag = assist.has_other_lang(info)
        if has_other_lang_flag:
            reason = "文本包含非中英文数字信息 %s %s, %s" % (group_tg_id, user_tg_id, info)
            print(reason)
            
            db_redis.tgData_set({
                "typee": "deleteAll",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": reason,
            })
            db_redis.tgData_set({
                "typee": "ban",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "reason": reason,
            })
            db.cheat_save(user_tg_id, reason)
            
    cheat_bank = helpp.has_cheat_bank(info)
    if cheat_bank is not None:
        bot_url = helpp.get_bot_url(group_tg_id, 1)
        
        message_id = net.sendMessageOne(bot_url, group_tg_id, template.msg_send_cheat_bank(user, cheat_bank))
        print("信息中包含骗子库银行卡：%s %s %s" % (cheat_bank, group_tg_id, user_tg_id))
    
    cheat_coin = helpp.has_cheat_coin(info)
    if cheat_coin is not None:
        reason = "发送信息中包含骗子库虚拟币地址：%s %s %s" % (cheat_coin, group_tg_id, user_tg_id)
        print(reason)
        
        db_redis.tgData_set({
            "typee": "delete",
            "group_tg_id": group_tg_id,
            "user_tg_id": user_tg_id,
            "message_tg_id": message_tg_id,
            "reason": reason,
        })
        db_redis.tgData_set({
            "typee": "restrict",
            "group_tg_id": group_tg_id,
            "user_tg_id": user_tg_id,
            "reason": reason,
            "until_date": -1,
        })
        
        bot_url = helpp.get_bot_url(group_tg_id, 1)
        
        net.sendMessageOne(bot_url, group_tg_id, template.msg_send_cheat_coin(user, user_tg_id))
            
    if int(flag) == 2:
        group_trade_type = int(trade_type)
        
        can_send = True
        has_bank_flag, has_coin_flag, has_zhifubao_flag = assist.has_special_text(info)
        if group_trade_type == 2:
            # 代收群 (删银行卡)
            if has_bank_flag:
                can_send = False
        elif group_trade_type == 3:
            # 代付群（删钱包地址）
            if has_coin_flag:
                can_send = False
        elif group_trade_type == 4:
            # 支付宝 (删 手机号, 邮箱号)
            if has_zhifubao_flag:
                can_send = False
        elif group_trade_type == 9:
            # 所有 (删 银行卡, 钱包地址, 手机号, 邮箱号)
            if has_bank_flag or has_coin_flag or has_zhifubao_flag:
                can_send = False

        if not can_send:
            print("该群内发送不允许的信息：银行卡，钱包地址，手机号，邮箱号 %s %s" % (group_tg_id, user_tg_id))
            
            db_redis.tgData_set({
                "typee": "delete",
                "group_tg_id": group_tg_id,
                "user_tg_id": user_tg_id,
                "message_tg_id": message_tg_id,
                "reason": "该群内发送不允许的信息：银行卡，钱包地址，手机号，邮箱号",
            })
            
            bot_url = helpp.get_bot_url(group_tg_id, 1)
            
            net.sendMessageOne(bot_url, group_tg_id, template.msg_send_has_special_text())
    
