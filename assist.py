import time
import re
from zhon.hanzi import punctuation
import langid
import emoji
import string


# ======================================================================================================================

def get_yesterday_time6():
    return timestamp2time(get_today_timestamp() + 3600 * 6 - 86400)
    
    
def get_today_time6():
    return timestamp2time(get_today_timestamp() + 3600 * 6)
    
    
def get_tommorrow_time6():
    return timestamp2time(get_today_timestamp() + 3600 * 6 + 86400)
    

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_today_time():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_today_timestamp():
    return time2timestamp(get_today_time(), False)


def get_current_timestamp():
    return int(time.time())


def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def get_simple_time(created_at):
    created_at = str(created_at)
    space = created_at.find(" ")
    return created_at[(space + 1):]


def get_simple_day(created_at):
    created_at = str(created_at)
    space = created_at.split(" ")
    return space[0]
    
    
def get_day_int():
    hour = time.strftime("%d", time.localtime())
    return int(hour)
    
    
def get_month(created_at):
    created_at_timestamp = time2timestamp(created_at)
    
    return int(time.strftime("%m", time.localtime(created_at_timestamp)))
    
    
# ======================================================================================================================

def get_start_end(created_at_timestamp):
    today = get_today_timestamp()
    
    start_at = get_today_time6()
    end_at = get_tommorrow_time6()
    
    if created_at_timestamp > today:
        if created_at_timestamp - today < 3600 * 6:
            # 0点-6点
            start_at = get_yesterday_time6()
            end_at = get_today_time6()
        else:
            pass
    else:
        # 昨日0点前的数据,
        start_at = get_yesterday_time6()
        end_at = get_today_time6()
        
    return start_at, end_at
    

def is_number(s):
    if s is None:
        return False
    
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        for i in s:
            unicodedata.numeric(i)
        return True
    except (TypeError, ValueError):
        pass
    return False
    
    
def unique_list(temp):
    return list(set(temp))
    
    
def handle_text(text):
    text = text.replace("𝅹", "")
    text = text.replace(" ", "")
    text = text.replace(",", "")
    text = text.replace(".", "")
    text = text.replace("，", "")
    text = text.replace("。", "")
    text = text.replace("+", "")
    text = text.replace("-", "")
    text = text.replace("*", "")
    text = text.replace("/", "")
    text = text.replace("(", "")
    text = text.replace("（", "")
    text = text.replace(")", "")
    text = text.replace("）", "")
    text = text.replace("、", "")

    text = text.lower()

    return text
    
    
# ======================================================================================================================

def user_same(obj, user_info):
    flag = False
    
    if obj["fullname"] == user_info["fullname"] and obj["username"] == user_info["username"]:
        flag = True
        
    return flag


def get_restrict_time(day):
    current_timestamp = get_current_timestamp()
    return current_timestamp + 86400 * day
    
    
# ======================================================================================================================

def has_bank(text):
    pattern = re.compile(r"([1-9])(\d{15}|\d{18})")
    result = re.search(pattern, text)

    if result is None:
        return False
    else:
        return True
        

def get_emoji_num(text):
    num = 0
    for character in text:
        if emoji.is_emoji(character):
            num = num + 1
            
    return num
    
    
def isEmojiAll(character):
    if emoji.is_emoji(character):
        return True
    
    return False
    

def isEmoji(content):
    if not content:
        return False
    if u"\U0001F600" <= content and content <= u"\U0001F64F":
        return True
    elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
        return True
    elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
        return True
    elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
        return True
    else:
        return False


def isTgEmoji(content):
    emojis = "😀😃😄😁😆😅😂🤣🥲😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🥸🤩🥳😏😒😞😔😟😕🙁😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀👽👾🤖🎃😺😸😹😻😼😽🙀😿😾👋🤚🖐🖖👌🤌🤏🤞🤟🤘🤙👈👉👆🖕👇👍👎👊🤛🤜👏🙌👐🤲🤝🙏💅🤳💪🦾🦵🦿🦶👣👂🦻"
    
    return content in emojis
    
    
def has_other_lang(text):
    result = re.search('[a-z]', text)
    if result is not None:
        return False
    
    result = re.search('[A-Z]', text)
    if result is not None:
        return False
    
    result = re.search('[0-9]', text)
    if result is not None:
        return False
    
    result = re.search('[\u4e00-\u9fa5]', text)
    if result is not None:
        return False
    
    text_len = len(text)
    for i in range(text_len):
        if isEmoji(text[i]):
            return False
        if isTgEmoji(text[i]):
            return False
        if isEmojiAll(text[i]):
            return False
    
    punctuation_str = string.punctuation
    for i in punctuation_str:
        text = text.replace(i, "")
    
    punctuation_str = punctuation
    for i in punctuation_str:
        text = text.replace(i, "")
        
    if len(text) == 0:
        return False
        
    lang, confidence = langid.classify(text)
    if lang is not None:
        lang = lang.lower()
        if lang == "en" or lang == "zh":
            return False
        else:
            return True
    
    return False
    
    
def has_special_text(text):
    return has_bank(text), has_coin(text), has_zhifubao(text)
    
    
def has_bank(text):
    pattern = re.compile(r"([1-9])(\d{15}|\d{18})")
    result = re.search(pattern, text)

    if result is None:
        return False
    else:
        return True


def has_coin(text):
    pattern = re.compile(r"T[A-Za-z0-9]{20,}")
    result = re.search(pattern, text)
    if result is None:
        return False
    else:
        return True


def has_zhifubao(text):
    if has_email(text) or has_phone(text):
        return True
    else:
        return False


def has_email(text):
    pattern_email = re.compile(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")
    result_email = re.search(pattern_email, text)

    if result_email is None:
        return False
    else:
        return True


def has_phone(text):
    pattern_phone = re.compile(
        r"(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[235-8]\d{2}|4(?:0\d|1[0-2]|9\d))|9[0-35-9]\d{2}|66\d{2})\d{6}")
    result_phone = re.search(pattern_phone, text)

    if result_phone is None:
        return False
    else:
        return True


def has_yajin(title):
    if title.find("已押") > 0:
        return True
        
    return False
    
    