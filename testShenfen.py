from lib import db

group_tg_id = "-1001677560391"
user_tg_id = "1890717643"

print("%s %s" % (group_tg_id, user_tg_id))
print("official %s" % db.official_one(user_tg_id))
print("white %s" % db.white_one(user_tg_id))
print("group_admin %s" % db.group_admin_one(group_tg_id, user_tg_id))
print("cheat %s" % db.cheat_one(user_tg_id))
print("cheats_special %s" % db.cheats_special_one(user_tg_id))
