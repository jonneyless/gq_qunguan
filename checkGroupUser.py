import asyncio
from lib import db
from telethon import TelegramClient
from assist import get_current_timestamp
import net


bot_token = "6245957008:AAFlAhO2ULFioLWlYMddSHyV5W00lkW54os"
api_id = 27127438
api_hash = 'a103aa33a68882267db12de32a2d9f86'


# boss_group_tg_id = -1001620186906
ad_group_tg_id = -1001660660101

bot_yu444_url = "https://api.telegram.org/bot5197558289:AAF8J63Uuu6KSKpgUQJPvA1pyH8s69FFI7E/"


async def index():
    start_time = get_current_timestamp()
    
    tg_ids = []
    tg_ids.append(ad_group_tg_id)

    bot = await TelegramClient('./sessions/welcomeBeiyong', api_id, api_hash).start(bot_token=bot_token)
    
    for group_tg_id in tg_ids:
        group_tg_id = int(group_tg_id)
        users = None
        
        try:
            users = await bot.get_participants(group_tg_id)
        except:
            print("error %s" % group_tg_id)
            pass
        
        if users is not None:
            objs = []
            
            print(len(users))
            
            for user in users:
                if (not hasattr(user, "id")) or (not hasattr(user, "username")) or (
                        not hasattr(user, "first_name")) or (not hasattr(user, "last_name")):
                    continue
                if user.id is None:
                    continue
                
                if user.deleted:
                    print(user)
        
                user_tg_id = user.id
                
                obj = {
                    "group_tg_id": group_tg_id,
                    "user_tg_id": user_tg_id,
                    "username": "",
                    "firstname": "",
                    "lastname": "",
                    "fullname": "",
                }
        
                if user.username is not None:
                    obj["username"] = user.username
        
                if user.first_name is not None:
                    obj["firstname"] = user.first_name
        
                if user.last_name is not None:
                    obj["lastname"] = user.last_name
        
                obj["fullname"] = obj["firstname"] + obj["lastname"]
                
                # if obj["fullname"] == "" and obj

                if int(user_tg_id) == 5197558289:
                    continue

                if not db.group_admin_single(user_tg_id):
                    flag, description = net.banChatMemberWrap(bot_yu444_url, ad_group_tg_id, user_tg_id)
                    
                    # flag = ""
                    # description = ""
                    
                    print("%s %s %s not admin，%s %s" % (user_tg_id, obj["fullname"], obj["username"], flag, description))
                    
                    if flag:
                        db.user_group_new_save(ad_group_tg_id, user_tg_id, 2, 2, 1, 2)

                
    end_time = get_current_timestamp()
        
    print("handle %s spend %s" % (len(tg_ids), (end_time - start_time)))

    await bot.disconnect()
    
 
async def main():
    await index()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
