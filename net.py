import json
import time

import requests
from retrying import retry

from config import chat_photo_path
from lib import db_redis

headers_tg = {
    "Content-Type": "application/json",
}

description_arr = [
    "Forbidden: bot was blocked by the user",
    "Forbidden: bot was kicked from the group chat",
    "Forbidden: bot was kicked from the supergroup chat",
    "Bad Request: not enough rights to send text messages to the chat",
    "Bad Request: message to delete not found",
    "Bad Request: chat not found",
    "Bad Request: group chat was upgraded to a supergroup chat",

    "Bad Request: USER_ALREADY_PARTICIPANT"
]

declineChatJoinRequest_description_arr = [
    "Bad Request: HIDE_REQUESTER_MISSING",
    "Forbidden: user is deactivated",
    "Bad Request: USER_ID_INVALID",
    "Forbidden: bot was kicked from the supergroup chat",
    "Bad Request: chat not found"
]


# ============================================================================================================================================

def getDeleteMessagesRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("getDeleteMessagesRetry: %s" % description)
        return True
    else:
        return False


def deleteMessagesWrap(bot_url, chat_id, message_ids):
    description = ""

    try:
        return deleteMessages(bot_url, chat_id, message_ids)
    except Exception as e:
        description = e
        print("deleteMessagesWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=getDeleteMessagesRetry)
def deleteMessages(bot_url, chat_id, message_ids):
    tg_url = bot_url + "deleteMessages"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "message_ids": json.dumps(message_ids),
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("deleteMessages Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)
        print("delete %s %s %s" % (chat_id, len(message_ids), response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("deleteMessage sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================

def getBanChatMemberRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("getBanChatMemberRetry: %s" % description)
        return True
    else:
        return False


def banChatMemberWrap(bot_url, chat_id, user_id):
    description = ""

    try:
        return banChatMember(bot_url, chat_id, user_id)
    except Exception as e:
        description = e
        print("banChatMemberWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=getBanChatMemberRetry)
def banChatMember(bot_url, chat_id, user_id):
    tg_url = bot_url + "banChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("banChatMember Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)
        print("kick: %s %s %s" % (chat_id, user_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("banChatMember sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================

def getUnbanChatMemberRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("getUnbanChatMemberRetry: %s" % description)
        return True
    else:
        return False


def unbanChatMemberWrap(bot_url, chat_id, user_id):
    description = ""

    try:
        return unbanChatMember(bot_url, chat_id, user_id)
    except Exception as e:
        description = e
        print("unbanChatMemberWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=getUnbanChatMemberRetry)
def unbanChatMember(bot_url, chat_id, user_id):
    tg_url = bot_url + "unbanChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("unbanChatMember Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)
        print("unban: %s %s %s" % (chat_id, user_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("unbanChatMember sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================

def getRestrictChatMemberRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("getRestrictChatMemberRetry: %s" % description)
        return True
    else:
        return False


def restrictChatMemberWrap(bot_url, chat_id, user_id, until_date=-1):
    description = ""

    try:
        return restrictChatMember(bot_url, chat_id, user_id, until_date)
    except Exception as e:
        description = e
        print("restrictChatMemberWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=getRestrictChatMemberRetry)
def restrictChatMember(bot_url, chat_id, user_id, until_date=-1):
    tg_url = bot_url + "restrictChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "until_date": until_date,
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("restrictChatMember Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("restrictChatMember sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================

def getCancelRestrictChatMemberRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("getCancelRestrictChatMemberRetry: %s" % description)
        return True
    else:
        return False


def cancelRestrictChatMemberWrap(bot_url, chat_id, user_id):
    description = ""

    try:
        return cancelRestrictChatMember(bot_url, chat_id, user_id)
    except Exception as e:
        description = e
        print("cancelRestrictChatMemberWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=getCancelRestrictChatMemberRetry)
def cancelRestrictChatMember(bot_url, chat_id, user_id):
    tg_url = bot_url + "restrictChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "permissions": {
            "can_send_messages": True,
            "can_send_media_messages": True,
            "can_send_polls": False,
            "can_send_other_messages": True,
            "can_add_web_page_previews": False,
            "can_change_info": False,
            "can_invite_users": False,
            "can_pin_messages": False,
        },
        "until_date": -1,
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("cancelRestrictChatMember Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("cancelRestrictChatMember sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================

def approveChatJoinRequestRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("approveChatJoinRequestRetry: %s" % description)
        return True
    else:
        return False


def approveChatJoinRequestWrap(bot_url, chat_id, user_id):
    description = ""

    try:
        return approveChatJoinRequest(bot_url, chat_id, user_id)
    except Exception as e:
        description = e
        print("approveChatJoinRequestWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=approveChatJoinRequestRetry)
def approveChatJoinRequest(bot_url, chat_id, user_id):
    tg_url = bot_url + "approveChatJoinRequest"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("approveChatJoinRequest Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 失败，不需要重试
    # flag = True 成功，不需要重试
    # flag = None 失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)
        print("approveChatJoinRequest %s %s %s" % (chat_id, user_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("approveChatJoinRequest sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================

def declineChatJoinRequestRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("declineChatJoinRequestRetry: %s" % description)
        return True
    else:
        return False


def declineChatJoinRequestWrap(bot_url, chat_id, user_id):
    description = ""

    try:
        return declineChatJoinRequest(bot_url, chat_id, user_id)
    except Exception as e:
        description = e
        print("declineChatJoinRequestWrap Exception: %s" % e)

    return None, description


@retry(stop_max_attempt_number=3, retry_on_result=declineChatJoinRequestRetry)
def declineChatJoinRequest(bot_url, chat_id, user_id):
    tg_url = bot_url + "declineChatJoinRequest"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("declineChatJoinRequest Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 失败，不需要重试
    # flag = True 成功，不需要重试
    # flag = None 失败，需要重试：tg异常，tg限制

    if response is not None:
        response_text = json.loads(response.text)
        print("declineChatJoinRequest %s %s %s" % (chat_id, user_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""

                if "description" in response_text:
                    description = response_text["description"]

                if description in declineChatJoinRequest_description_arr:
                    # 不用重试
                    flag = False
                else:
                    if "error_code" in response_text:
                        error_code = str(response_text["error_code"])

                        if error_code == "429":
                            if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                                retry_after = int(response_text["parameters"]["retry_after"])
                                print("declineChatJoinRequest sleep %s" % retry_after)
                                time.sleep(retry_after)
                                # 需要重试
                                flag = None
                        elif error_code == "403":
                            pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description


# ============================================================================================================================================
# ============================================================================================================================================
# 单个操作，不需要重试

def remove_admin(bot_url, group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"

    headers = headers_tg

    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        # "can_manage_chat" => true,
        # "can_post_messages" => true,
        # "can_edit_messages" => true,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
    }

    print(tg_url)
    print(data)

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("remove_admin Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        print(response_text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def promote_empty_admin(bot_url, group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"

    headers = headers_tg

    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        "is_anonymous": False,
        "can_manage_chat": True,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_manage_video_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
        "can_post_stories": False,
        "can_edit_stories": False,
        "can_delete_stories": False,
        "can_manage_topics": False,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("promote_empty_admin Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def recover_admin(bot_url, group_tg_id, user_tg_id):
    tg_url = bot_url + "promoteChatMember"

    headers = headers_tg

    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
        "is_anonymous": False,
        "can_manage_chat": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": True,
        "can_manage_voice_chats": False,
        "can_restrict_members": True,
        "can_promote_members": False,
        "can_change_info": False,
        "can_invite_users": True,
        "can_pin_messages": True,
        "can_manage_topics": False,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("recover_admin Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def setChatPermissions(bot_url, group_tg_id, send=True):
    tg_url = bot_url + "setChatPermissions"

    headers = headers_tg

    permissions = {
        "can_send_messages": send,
        "can_send_audios": False,
        "can_send_documents": False,
        "can_send_photos": send,
        "can_send_videos": send,
        "can_send_video_notes": False,
        "can_send_voice_notes": False,
        "can_send_polls": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
        "can_change_info": False,
        "can_invite_users": False,
        "can_pin_messages": False,
        "can_manage_topics": False,
    }

    data = {
        "chat_id": group_tg_id,
        "permissions": json.dumps(permissions),
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("setChatPermissions Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def set_admin_title(bot_url, chat_id, user_id, title):
    tg_url = bot_url + "setChatAdministratorCustomTitle"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "custom_title": title
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("setChatAdministratorCustomTitle Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def promote_super_admin(bot_url, chat_id, user_id, short=True):
    tg_url = bot_url + "promoteChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "is_anonymous": False,
        "can_manage_chat": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,

        "can_invite_users": True,
        "can_pin_messages": True,

        "can_manage_topics": False,
    }
    if not short:
        # 官方交易员账号全部权限
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            # "can_manage_chat" => true,
            # "can_post_messages" => true,
            # "can_edit_messages" => true,
            "can_delete_messages": True,
            "can_manage_voice_chats": True,
            "can_restrict_members": True,
            "can_promote_members": True,
            "can_change_info": True,
            "can_invite_users": True,
            "can_pin_messages": True,
        }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("promote_admin Exception: %s" % e)

    # if int(chat_id) == -1001885709812:
    #     print(response)
    #     print(bot_url)

    if response is not None:
        response_text = json.loads(response.text)

        print(response_text)

        if int(chat_id) == -1001885709812:
            print(response_text)

        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def promote_admin(bot_url, chat_id, user_id, short=True):
    tg_url = bot_url + "promoteChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "is_anonymous": False,
        "can_manage_chat": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_delete_messages": False,
        "can_manage_voice_chats": False,
        "can_restrict_members": False,
        "can_promote_members": False,
        "can_change_info": False,

        "can_invite_users": True,
        "can_pin_messages": True,

        "can_manage_topics": False,
    }
    if not short:
        # 非交易账号部分权限
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "is_anonymous": False,
            "can_manage_chat": False,
            "can_post_messages": False,
            "can_edit_messages": False,
            "can_delete_messages": True,
            "can_manage_voice_chats": False,
            "can_restrict_members": True,
            "can_promote_members": False,
            "can_change_info": False,
            "can_invite_users": True,
            "can_pin_messages": True,
        }

    print(tg_url)
    print(data)
    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("promote_admin Exception: %s" % e)

    # if int(chat_id) == -1001885709812:
    #     print(response)
    #     print(bot_url)

    if response is not None:
        response_text = json.loads(response.text)

        if int(chat_id) == -1001885709812 or int(chat_id) == -1002233012973:
            print(response_text)

        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def game_promote_admin(bot_url, chat_id, user_id, short=False):
    tg_url = bot_url + "promoteChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,

        "is_anonymous": False,
        "can_manage_chat": False,
        "can_promote_members": False,
        "can_change_info": False,
        "can_post_stories": False,
        "can_edit_stories": False,
        "can_delete_stories": False,
        "can_post_messages": False,
        "can_edit_messages": False,
        "can_manage_topics": False,

        "can_invite_users": True,
        "can_delete_messages": True,
        "can_pin_messages": True,
        "can_restrict_members": True,
        "can_manage_video_chats": True,
    }
    if short:
        data["can_manage_video_chats"] = False

    print(tg_url)
    print(data)

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("promote_admin Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)

        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def deleteMessageOne(bot_url, chat_id, message_id):
    tg_url = bot_url + "deleteMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("deleteMessageOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def deleteMessages(bot_url, chat_id, message_ids):
    tg_url = bot_url + "deleteMessages"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "message_ids": json.dumps(message_ids),
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("deleteMessages Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def sendMessage(bot_url, chat_id, text):
    tg_url = bot_url + "sendMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "text": text,
    }

    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendMessageOne Exception: %s" % e)


def sendMessageOne(bot_url, chat_id, text, reply_message_id=None):
    tg_url = bot_url + "sendMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_notification": True,
        "link_preview_options": {
            "is_disabled": True
        }
    }

    if reply_message_id is not None:
        data["reply_parameters"] = {
            "message_id": reply_message_id
        }

    message_id = -1
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendMessageOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                message_id = response_text["result"]["message_id"]

    return message_id


def sendMessageOneWithBtn(bot_url, chat_id, text, replyMarkup=None):
    tg_url = bot_url + "sendMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_notification": True,
        "link_preview_options": {
            "is_disabled": True
        }
    }

    if replyMarkup is not None:
        data["reply_markup"] = replyMarkup

    message_id = -1
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendMessageOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)

        print(response_text)

        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                message_id = response_text["result"]["message_id"]

    return message_id


def sendPhotoOne(bot_url, chat_id, photo, caption=None, btns=None):
    tg_url = bot_url + "sendPhoto"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "photo": photo,
    }

    if caption is not None:
        data["caption"] = caption

    if btns is not None:
        data["reply_markup"] = btns

    message_id = -1
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendPhotoOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                message_id = response_text["result"]["message_id"]

    return message_id


def sendVideoOne(bot_url, chat_id, video, caption=None, btns=None):
    tg_url = bot_url + "sendVideo"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "video": video,
    }

    if caption is not None:
        data["caption"] = caption

    if btns is not None:
        data["reply_markup"] = btns

    message_id = -1
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendVideoOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                message_id = response_text["result"]["message_id"]

    return message_id


def sendDocumentOne(bot_url, chat_id, document, caption=None, btns=None):
    tg_url = bot_url + "sendDocument"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "document": document,
    }

    if caption is not None:
        data["caption"] = caption

    if btns is not None:
        data["reply_markup"] = btns

    message_id = -1
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("sendDocumentOne Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                message_id = response_text["result"]["message_id"]

    return message_id


def setChatTitle(bot_url, chat_id, title):
    tg_url = bot_url + "setChatTitle"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "title": title,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("setChatTitle Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def pinChatMessage(bot_url, chat_id, message_id):
    tg_url = bot_url + "pinChatMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("pinChatMessage Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def unpinChatMessage(bot_url, chat_id, message_id):
    tg_url = bot_url + "unpinChatMessage"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("unpinChatMessage Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)

        print("unpinChatMessage %s %s %s" % (chat_id, message_id, response_text))

        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def setChatDescription(bot_url, chat_id, description):
    tg_url = bot_url + "setChatDescription"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "description": description,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("setChatDescription Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def unpinAllChatMessages(bot_url, chat_id):
    tg_url = bot_url + "unpinAllChatMessages"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
    }

    flag = False
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("unpinAllChatMessages Exception: %s" % e)

    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            flag = True

    return flag


def send_and_delete_last(bot_url, chat_id, text, key_short="mm"):
    m_id = sendMessageOne(bot_url, chat_id, text)

    last_m_id = db_redis.last_message_id_get(chat_id, key_short)
    if last_m_id is not None:
        deleteMessageOne(bot_url, chat_id, last_m_id)

    if m_id is not None and int(m_id) > 0:
        db_redis.last_message_id_set(chat_id, m_id, key_short)


def send_btn_and_delete_last(bot_url, chat_id, text, btns, key_short="mmb"):
    m_id = sendMessageOneWithBtn(bot_url, chat_id, text, btns)

    last_m_id = db_redis.last_message_id_get(chat_id, key_short)
    if last_m_id is not None:
        deleteMessageOne(bot_url, chat_id, last_m_id)

    if m_id is not None and int(m_id) > 0:
        db_redis.last_message_id_set(chat_id, m_id, key_short)


def promote_admin_title(bot_url, chat_id, user_id, title):
    flag = False
    result_admin = promote_admin(bot_url, chat_id, user_id, True)
    if result_admin:
        result_admin_title = set_admin_title(bot_url, chat_id, user_id, title)
        if result_admin_title:
            flag = True

    return flag


def game_promote_admin_title(bot_url, chat_id, user_id, title, short=True):
    flag = False
    result_admin = game_promote_admin(bot_url, chat_id, user_id, short)
    if result_admin:
        if len(title) > 0:
            result_admin_title = set_admin_title(bot_url, chat_id, user_id, title)
            if result_admin_title:
                flag = True
        else:
            flag = True

    return flag


# ============================================================================================================================================
# ============================================================================================================================================


def getYajin(tgId):
    yajinNum = 0
    yajinMoney = 0
    groups = []

    url = "http://www.yajin.com:8089/api/history"

    headers = headers_tg

    response = requests.get(url, headers=headers, timeout=30)
    if response is not None:
        data = response.json()

        if "msg" in data and data['msg'] == "success":
            yajinNum = data['data']['nums']
            yajinMoney = data['data']['money']
            groups = data['data']['detail']

    return {"yajin_num": yajinNum, "yajin_money": yajinMoney, "groups": groups}

def checkJzHaveData(group_tg_id, start_at, end_at):
    tg_url = "http://jz.admin.com:8680/api/cal/haveData"

    headers = headers_tg

    data = {
        "key": "huionedb",
        "group_tg_id": group_tg_id,
        "start_at": start_at,
        "end_at": end_at,
    }

    status = 0

    response = requests.post(tg_url, json=data, headers=headers, timeout=30)
    if response is not None:
        response_text = json.loads(response.text)

        if ("message" in response_text) and response_text["message"] == "ok":
            status = response_text["data"]["status"]

            print("checkJzHaveData %s %s" % (group_tg_id, status))

    return int(status)


def removeNotOfficialAdmin(group_tg_id):
    tg_url = "http://jz.admin.com:8680/api/removeNotOfficialAdmin"

    headers = headers_tg

    data = {
        "key": "huionedb",
        "group_tg_id": group_tg_id,
    }

    flag = False

    response = requests.post(tg_url, json=data, headers=headers, timeout=30)
    if response is not None:
        response_text = json.loads(response.text)
        if ("message" in response_text) and response_text["message"] == "success":
            flag = True

    return flag


def getChatInfo(bot_url, chat_id):
    tg_url = bot_url + "getChat"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
    }

    response = None

    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=30)
    except:
        pass

    if response is not None:
        response_text = json.loads(response.text)

        if "ok" in response_text:
            if response_text["ok"]:
                if "result" in response_text:
                    return response_text["result"]
            else:
                return False

    return None


def getChatAdmins(bot_url, chat_id):
    tg_url = bot_url + "getChatAdministrators"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
    }

    response = None

    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=10)
    except:
        pass

    admins = []
    if response is not None:
        response_text = json.loads(response.text)

        if "ok" in response_text:
            if response_text["ok"]:
                if "result" in response_text:
                    for admin in response_text["result"]:
                        admins.append(admin['user']['username'])

    return admins


def getBio(base_url, chat_id):
    bio = db_redis.bio_get(chat_id)
    if bio is None:
        result = getChatInfo(base_url, chat_id)
        if result is not None:
            if "bio" in result:
                bio = result["bio"]
                db_redis.bio_set(chat_id, bio)

    return bio


def getChatMemberIn(base_url, chat_id, user_id):
    tg_url = base_url + "getChatMember"

    headers = headers_tg

    data = {
        "chat_id": chat_id,
        "user_id": user_id,
    }

    response = None

    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=10)
    except:
        pass

    flag = False
    ok = 2
    description = ""
    if response is not None:
        response_text = json.loads(response.text)
        chat_id_hwgq = -1001624139937  # hwgq
        chat_id_gongqiu = -1001082308171  # gongqiu
        chat_id_kefu = -1001015370323  # kefu

        chat_id = int(chat_id)

        if chat_id == chat_id_hwgq:
            chat_id = "hwgq"
        elif chat_id == chat_id_gongqiu:
            chat_id = "gongqiu"
        elif chat_id == chat_id_kefu:
            chat_id = "kefu"

        print("getChatMember %s %s %s" % (chat_id, user_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                if "result" in response_text:
                    result = response_text["result"]
                    if "status" in result:
                        status = result["status"]
                        if status == "member" or status == "administrator" or status == "creator":
                            flag = True
                            ok = 1
                        else:
                            ok = 1
            else:
                flag = False

                if "description" in response_text:
                    description = response_text["description"]

                    if description == "Bad Request: user not found":
                        flag = False
                        ok = 1

    return flag, description, ok


def sendAlert(base_url, chat_id, user_id, callback_query_id, text):
    tg_url = base_url + "answerCallbackQuery"

    headers = headers_tg

    data = {
        "callback_query_id": callback_query_id,
        "text": text,
        "show_alert": True,
    }

    response = None

    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=10)
    except:
        pass

    if response is not None:
        response_text = json.loads(response.text)
        print("sendAlert %s %s %s" % (chat_id, user_id, response_text))


def setChatPhotoRequestRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("setChatPhotoRequestRetry: %s" % description)
        return True
    else:
        return False


@retry(stop_max_attempt_number=3, retry_on_result=setChatPhotoRequestRetry)
def setChatPhotoRequest(bot_url, chat_id):
    tg_url = bot_url + "setChatPhoto"

    data = {
        "chat_id": chat_id,
    }

    response = None
    try:
        response = requests.post(tg_url, data=data, files={"photo": open(chat_photo_path, 'rb')}, timeout=15)
    except Exception as e:
        print("setChatPhotoRequest Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 失败，不需要重试
    # flag = True 成功，不需要重试
    # flag = None 失败，需要重试：tg异常，tg限制

    if response is not None:
        print(response.text)
        response_text = json.loads(response.text)
        # print(response_text)
        print("setChatPhotoRequest %s %s" % (chat_id, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("setChatPhotoRequest sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description
