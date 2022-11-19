from .configs import DB_CONFIG, REDIS
import redis
import pymysql

class Dao:
    def __init__(self):
        self.db = pymysql.connect(
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            db=DB_CONFIG['database'],
            charset='utf8'
        )
        self.cur = self.db.cursor(pymysql.cursors.DictCursor)
    def findOne(self, sql, variables):
        self.cur.execute(sql, variables)
        return self.cur.fetchone()
    
    def execute(self, sql, variables):
        self.cur.execute(sql, variables)
    
    def save(self):
        self.db.commit()

def get_redis():
    setting = REDIS
    IP = setting['ip']
    PORT = setting['port']
    CHARSET = setting['charset']
    DECODE_RES = setting['decode_responses']
    return redis.Redis(host=IP, port=PORT, charset=CHARSET, decode_responses=DECODE_RES)
