from .models import config
import redis

def getRedis():
    setting = config.REDIS
    IP = setting['ip']
    PORT = setting['port']
    CHARSET = setting['charset']
    DECODE_RES = setting['decode_responses']
    return redis.Redis(host=IP, port=PORT, charset=CHARSET, decode_responses=DECODE_RES)
