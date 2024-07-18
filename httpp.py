import requests
import json

from config import official_channels

headers_all = {
    "Content-Type": "application/json",
}


# ----------------------------------------------------------------------------------------------------------------------

def hwdb_hasChat(user_tg_id):
    tg_url = "http://private.chat.com:81/api/hasChat"

    headers = headers_all

    data = {
        "key": "huionedb",
        "user_tg_id": user_tg_id,
    }
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=30)
    if response is not None:
        response = json.loads(response.text)
        if "message" in response:
            if response["message"] == "success":
                return True

    return False
    
    
# ----------------------------------------------------------------------------------------------------------------------

def zhuan_hasChat(user_tg_id):
    tg_url = "http://he444.444danbao.com/api/hasChat"

    headers = headers_all

    data = {
        "key": "huionedb",
        "user_tg_id": user_tg_id,
    }
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=30)
    if response is not None:
        response = json.loads(response.text)
        if "message" in response:
            if response["message"] == "success":
                return True

    return False
    
    
# ----------------------------------------------------------------------------------------------------------------------

def getChatMemberWithToken(group_tg_id, user_tg_id, token):
    tg_url = "https://api.telegram.org/bot%s/getChatMember" % token

    headers = headers_all

    data = {
        "chat_id": group_tg_id,
        "user_id": user_tg_id,
    }
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=30)
    if response is not None:
        response_text = json.loads(response.text)
        if "ok" in response_text and response_text["ok"]:
            if "result" in response_text:
                result = response_text["result"]
                if "status" in result:
                    status = result["status"]
                    if status != "left" and status != "kicked":
                        return True

    return False


# ----------------------------------------------------------------------------------------------------------------------

def flushGroup(group_tg_id):
    tg_url = "http://welcome.test/api/flushGroup"

    headers = headers_all

    data = {
        "key": "huionedb3",
        "user_tg_id": group_tg_id,
    }
    
    requests.post(tg_url, json=data, headers=headers, timeout=30)
    
    