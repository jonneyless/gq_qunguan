import json
import time

import helpp
from config import admin_url
from lib import db_redis, db
from lib.db import setKeywordReplyRecord
from net import sendPhotoOne, sendVideoOne, sendDocumentOne, sendMessageOneWithBtn, sendMessageOne, deleteMessages


def keyword_reply(item):
    if db_redis.reply_repeat_check(item["chat_id"], item["reply"]["keyword"]):
        return

    chatId = item["chat_id"]
    userId = item["tg_id"]
    messageId = item["message_id"]
    keyword = item["reply"]["keyword"]

    senderTypes = []
    if 'sender_type' in item['reply']:
        senderTypes = json.loads(item["reply"]["sender_type"])

    if db.official_one(userId):
        senderType = 1
    else:
        if db.group_admin_single(userId):
            senderType = 2
        else:
            senderType = 3

    if senderType not in senderTypes:
        return

    db_redis.set_reply_repeat(chatId, keyword)

    last = db.getLastKeywordReplyRecord(chatId, keyword)
    if last is None or int(last['created_at']) < (int(time.time()) - 180):
        botUrl = helpp.get_bot_url(chatId, 2)

        replies = []
        if 'replies' in item['reply']:
            replies = json.loads(item["reply"]["replies"])

        replyMsgIds = []

        for reply in replies:
            text = None
            if 'text' in reply:
                text = reply["text"]

            file = ''
            fileType = 0
            if 'file' in reply:
                file = admin_url + "uploads/" + reply["file"]
                fileType = reply["file_type"]

            replyMarkup = None
            if 'buttonText' in reply:
                replyMarkup = {'inline_keyboard': [[{'text': reply['buttonText'], 'url': reply['buttonUrl']}]]}

            if file != '':
                if fileType == 1:
                    msgId = sendPhotoOne(botUrl, chatId, file, text, replyMarkup)
                elif fileType == 2:
                    msgId = sendVideoOne(botUrl, chatId, file, text, replyMarkup)
                else:
                    msgId = sendDocumentOne(botUrl, chatId, file, text, replyMarkup)
            else:
                if text is None:
                    text = "欢迎"

                msgId = sendMessageOneWithBtn(botUrl, chatId, text, replyMarkup)

            if msgId != -1:
                replyMsgIds.append(msgId)

            setKeywordReplyRecord(chatId, keyword, messageId, replyMsgIds)

            if last is not None and last['created_at'] > (int(time.time()) - 12 * 3600):
                messageIds = json.loads(last['reply_message_ids'])
                messageIds.append(last['message_id'])

                deleteMessages(botUrl, chatId, messageIds)
