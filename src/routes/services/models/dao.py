from . import config
import pymysql

db_config = config.db
db = pymysql.connect(
    user=db_config['user'],
    passwd=db_config['password'],
    host=db_config['host'],
    db=db_config['database'],
    charset='utf8'
)


def connection(func):
    def wrapper(model, *args, **kwargs):
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                return func(model, *args, cursor=cur, **kwargs)
        finally:
            cur.close()
    return wrapper


@connection
def findById(model, id, cursor=None):
    id_attr = _get_id_attr(model, model.__names__)
    q = '''
        SELECT * FROM {} WHERE {}={};
    '''.format(_get_table_name(model.__name__), id_attr[0], id if isinstance(id, int) else f"'{id}'")

    cursor.execute(q)
    try:
        return cursor.fetchone()
    except:
        return None


@connection
def find(model, filter, cursor=None):
    q = "SELECT * FROM {} ".format(_get_table_name(model.__name__))
    if filter:
        q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in filter.items()])+";"
    cursor.execute(q)
    return cursor.fetchall()


@connection
def findOne(model, filter, cursor=None):
    q = "SELECT * FROM {} ".format(_get_table_name(model.__name__))
    q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in filter.items()])+';'
    cursor.execute(q)
    return cursor.fetchone()


@connection
def update(model, filter, cursor=None):
    q = 'UPDATE {} SET '.format(_get_table_name(model.__name__))
    q += ', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in model.data.items()])+"\n"
    q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in filter.items()])+";"
    cursor.execute(q)


@connection
def create(model, cursor=None):
    q = 'INSERT INTO {}'.format(_get_table_name(model.__name__))
    q += '('+', '.join([name for name in model.data.keys()])+')\n'
    q += 'VALUES ('+', '.join([value if isinstance(value, int) else f"'{value}'" for value in model.data.values()])+');'
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
    
    async def update(self, model, filter):
        q = 'UPDATE {} SET '.format(_get_table_name(model.__name__))
        q += ', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in model.data.items()])+"\n"
        q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in filter.items()])+";"
        self.cur.execute(q)
    
    async def create(self, model):
        q = 'INSERT INTO {}'.format(_get_table_name(model.__name__))
        q += '('+', '.join([name for name in model.data.keys()])+')\n'
        q += 'VALUES ('+', '.join([value if isinstance(value, int) else f"'{value}'" for value in model.data.values()])+');'
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
