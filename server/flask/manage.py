import config
import redis
import pymysql

class DAO:
    def __init__(self):
        db_config = config.db
        self.db = pymysql.connect(
            user=db_config['user'],
            passwd=db_config['password'],
            host=db_config['host'],
            db=db_config['database'],
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

def getRedis():
    setting = config.REDIS
    IP = setting['ip']
    PORT = setting['port']
    CHARSET = setting['charset']
    DECODE_RES = setting['decode_responses']
    return redis.Redis(host=IP, port=PORT, charset=CHARSET, decode_responses=DECODE_RES)
