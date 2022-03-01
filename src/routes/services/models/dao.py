import config
import pymysql


db_config = config.db
db = pymysql.connect(
    user=db_config['user'],
    passwd=db_config['password'],
    host=db_config['host'],
    db=db_config['database'],
    charset='utf8'
)

def connect(func):
    def wrapper(model: object, *args, **kwargs):
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                func(model, *args, cursor=cur, **kwargs)
        finally:
            cur.close()
    return wrapper

@connect
async def findById(model, id, cursor=None):
    id_attr = _get_id_attr(model, model.__names__)
    q = '''
        SELECT * FROM {} WHERE {}={};
    '''.format(_get_table_name(model.__name__), id_attr[0], id)
    cursor.execute(q)
    return model.set_data(cursor.fetchone())

@connect
async def find(model, filter, only=False, cursor=None):
    q = "SELECT * FROM {} ".format(_get_table_name(model.__name__))
    if filter:
        q += 'WHERE '+', '.join([f"{k}={v}" for k, v in filter.items()])+";"
    cursor.execute(q)
    if only:
        return model.set_data(cursor.fetchone())
    return [model.set_data(x) for x in cursor.fetchall()]

@connect
async def update(self, model: object, filter, cursor=None):
    q = 'UPDATE {} SET '.format(_get_table_name(model.__name__))
    q += ', '.join([f"{k}={v}" for k, v in model.data.items()])+"\n"
    q += 'WHERE '+', '.join([f"{k}={v}" for k, v in filter.items()])+";"
    cursor.execute(q)

@connect
async def create(self, model: object, cursor=None):
    q = 'INSERT INTO {}'.format(_get_table_name(model.__name__))
    q += '('+', '.join([name for name in model.data.keys()])+')\n'
    q += 'VALUES ('+', '.join([value for value in model.data.values()])+');'
    cursor.execute(q)

class SQLSession:
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
    
    async def update(self, model: object, filter):
        q = 'UPDATE {} SET '.format(_get_table_name(model.__name__))
        q += ', '.join([f"{k}={v}" for k, v in model.data.items()])+"\n"
        q += 'WHERE '+', '.join([f"{k}={v}" for k, v in filter.items()])+";"
        self.cur.execute(q)
    
    async def create(self, model: object):
        q = 'INSERT INTO {}'.format(_get_table_name(model.__name__))
        q += '('+', '.join([name for name in model.data.keys()])+')\n'
        q += 'VALUES ('+', '.join([value for value in model.data.values()])+');'
        self.cur.execute(q)

    def commit(self):
        self.db.commit()
        self.cur.close()


def _get_table_name(class_name):
    tmp = list(class_name)
    for i in range(len(tmp)):
        if i==0:
            tmp[0] = tmp[0].lower()
        if tmp[i].isupper():
            tmp[i] = "_"+tmp[i].lower()
    return "".join(tmp)

def _get_id_attr(model, names):
    for name in names:
        if eval(f'model.{name}.is_id'):
            return eval(f'model.{name}.attr')
    raise Exception("ID not found")
