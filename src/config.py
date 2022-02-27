# pymysql 설정
db = {
    'user': 'user',
    'password': 'password',
    'host': 'db-host',
    'port': '3306',
    'database': 'db'
}

# REDIS pubsub 설정
REDIS = {
    'ip': 'localhost',
    'port': 6379,
    'charset': 'utf-8',
    'decode_responses': True
}

# 안쓰는 db설정 (flask sqlarchemy 사용시 이용하는 설정)
DB_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8".format(
    db['user'],
    db['password'],
    db['host'],
    db['port'],
    db['database']
)
