from lib import db_redis
prefix = "qunguan_"


print("handleTg len %s" % db_redis.data_len(prefix + "TgData_qq"))
print("handleUser len %s" % db_redis.data_len("changeUserNew_qq"))
print("handleUserGroup len %s" % db_redis.data_len("changeUserGroupNew_qq"))
print("handleMsg48 len %s" % db_redis.data_len("saveMsg48_qq"))
print("handleMsg len %s" % db_redis.data_len("saveMsg_qq"))
print("handleApprove len %s" % db_redis.data_len("saveApprove_qq"))
print("handleCommand len %s" % db_redis.data_len("saveCommand_qq"))
print("handleSj len %s" % db_redis.data_len("saveSjMsg_qq"))

print("handleTgError len %s" % db_redis.data_len(prefix + "TgData_error_qq"))

# print("====")
# print("handleTgOld len %s" % db_redis.data_len(prefix + "TgData_qq_new"))
