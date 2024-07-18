def msg_notice_game_group_true():
    msg = """有本机器人在群，此群是真群！请注意看我的用户名是 @qunguan (群管拼音)，谨防假机器人。私聊我输入词语可以搜索真公群,如：卡商、白资、承兑等。请找有头衔的人在群内交易，切勿相信主动私聊你的，都是骗子。非群内交易没有任何保障。客服频道 @kefu 汇旺公群 @hwgq"""

    return msg
    

def no_search():
    msg = """该内容无搜索结果，请重新输入！ 
请关注 @hwgq 从这个频道可以进入所有汇旺担保公群！
你也可以试试超级搜索 @chaoji 。"""

    return msg
    

def msg_private_yanzheng():
    msg = """1、 验证公群请发群编号（群编号是公群两个字后面带的数字序号，如果公群123，123就是群编号），机器人会自动发送群链接，看看和自己所在的是不是同一个群可以自助验群；
2、验证专群给 @he444bot 这个机器人发专群群编号(专群群编号为一个字母加5个数字)，看和交易员的共同群验群；
3、如果不会自助验群，请联系客服 @hwdb 进行人工验群。
"""

    return msg


def msg_notice_group_true(group_admins, title):
    # msg = "汇旺担保官方人员 "

    # for index in range(len(group_admins)):
    #     group_admin = group_admins[index]

    #     msg += "%s " % group_admin["username"]

    # msg += "在本群，本群《%s》是真群。" % title
    
    msg = """有本机器人在群，此群是真群！请注意看我的用户名是 @qunguan (群管拼音)，谨防假机器人。私聊我输入词语可以搜索真公群,如：卡商、白资、承兑等。请找有头衔的人在群内交易，切勿相信主动私聊你的，都是骗子。非群内交易没有任何保障。客服频道 @kefu 汇旺公群 @hwgq"""

    return msg


def msg_notice_group_false():
    return "本群少于两个官方人员疑似假群，请通过公群导航 @hwgq 核对。"


def msg_check_group_true():
    return "这是真汇旺担保公群，可以放心交易。"


def msg_check_group_false():
    return "这是骗子建立的假公群，切勿上当受骗，并联系汇旺担保官方举报。"


def msg_group_set_welcome_info(title, info):
    return "欢迎语设置成功，当前欢迎语是：欢迎***加入 %s %s" % (title, info)


def msg_group_show_welcome_info(title, info):
    if info is None:
        info = ""
    
    return "当前欢迎语是：欢迎***加入 %s %s" % (title, info)


def msg_group_close_welcome_info():
    return "欢迎语已关闭"


def msg_send_cheat_bank(userr, cheat_bank):
    return "%s使用骗子银行卡账号%s" % (userr["fullname"], cheat_bank)


def msg_send_cheat_coin(userr, cheat_coin):
    return "%s使用骗子虚拟币地址%s" % (userr["fullname"], cheat_coin)


def msg_send_has_huiwang(userr):
    return "%s疑似冒充汇旺官方人员，已自动将其踢出群组" % userr["fullname"]


def msg_send_has_special_text():
    return "xxx并非群管理，所发地址/账号无效，请提高警惕，小心被骗。"
    
    
def msg_start_text():
    # text = "您好，这里是汇旺公群机器人\n"
    # text += "公群导航 @hwgq 避免进假群\n"
    # text += "公群流程 @gongqunLC 了解公群交易注意事项\n"
    # text += "客服频道 @kefu 可以快速分辨工作人员\n"
    # text += "另外可以私聊我发送公群编号直接获取进群方式，请输入精确的公群编号，例如【123】\n"
    
    text = """您好，这里是汇旺公群机器人
公群导航 @hwgq 避免进假群
公群流程 @gongqunLC 了解公群交易注意事项
客服频道 @kefu 可以快速分辨工作人员
另外可以私聊我发送公群编号直接获取进群方式，例如【123】；也可以输入词语进行搜索，如 卡商、代收、白资"""
    
    return text


def msg_group_close():
    text = "本公群今日已下课，\n"
    text += "如需交易，请在该群恢复营业后在群内交易！ 切勿私下交易！！！\n"
    text += "如有业务咨询请联系群老板/业务员\n"
    text += "如有纠纷请联系纠纷专员 @hwdb\n"
    
    return text
    
    
def msg_group_open():
    return "群已开，群内可以正常营业"
    
    
def msg_group_error():
    return "当前公群处于暂停交易状态，擅自交易后果自负，请群老板或业务员处理完相关事务后再重新开群"
    
    
def msg_night_close_msg():
    return "尊敬的客户您好，当前时间已暂停受理业务，请在金边时间 8:00～2:00 与工作人员联系"
    
    
def msg_first_notice():
    return "私下交易没有安全保障，出现纠纷平台概不负责，所有交易请在公群内进行，并及时入账，切勿私下交易！"
    
    
def msg_boss_pwd():
    msg = "请输入8-18位的密码，密码只能由字母和数字组成，字母区分大小写，放弃请点击【取消】\n"
    msg += "注：密码仅对本账号有效，一经设置无法修改，请牢记您的密码，任何担保工作人员不会主动向您索要密码，此密码仅作为找回身份使用，谨防泄漏"
    
    return msg
    
    
def msg_ok():
    return "操作成功"
    
    
def msg_error():
    return "操作失败，请重试"
    
    