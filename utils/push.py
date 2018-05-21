import redis

pool = redis.ConnectionPool(host='localhost', port=6379,
                            decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)
# r.lpush("apks",
#         "gta.grand.five.criminal.auto,http://apk.apkmonk.com/apks-16/gta.grand.five.criminal.auto_2018-05-16.apk?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=IFVYHACUO60QSGWW9L9Z%2F20180521%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20180521T041339Z&X-Amz-Expires=2400&X-Amz-SignedHeaders=host&X-Amz-Signature=510ef7b45fbb2057aa3754ea8a279c68c91d070b95bd1d38d9d48b70270d5a08")
# r.lpush("apks",
#         "pine.game.skydancer,http://apk2.apkmonk.com/apk-15/pine.game.skydancer_2018-05-15.apk?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=IFVYHACUO60QSGWW9L9Z%2F20180521%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20180521T042113Z&X-Amz-Expires=2400&X-Amz-SignedHeaders=host&X-Amz-Signature=3d7c4bdc3234d38dad19931e22bca54985d9b8b06c651c1c8a831fb175b61c55")
r.lpush("apks", "com.qq.com,https://sm.myapp.com/original/Audio/QQMusic_Setup_1598.4685_QMgr-15.9.5.0.exe")
r.lpush("apks", "com.qmusic.com,https://sm.myapp.com/original/Audio/QQMusic_Setup_1598.4685_QMgr-15.9.5.0.exe")

# r.rpop("apks")

# r.rpop("apks")
# r.rpop("apks")
print(len(r.lrange("apks", 0, -1)))
