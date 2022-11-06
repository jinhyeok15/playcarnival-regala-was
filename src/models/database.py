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
    def wrapper(modelcls, *args, **kwargs):
        try:
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                return func(modelcls, *args, cursor=cur, **kwargs)
        finally:
            cur.close()
    return wrapper


@connection
def get_data_by_id(modelcls, id, cursor=None):
    id_attr = _get_id_attr(modelcls, modelcls.__names__)
    q = '''
        SELECT * FROM {} WHERE {}={};
    '''.format(_get_table_name(modelcls.__name__), id_attr[0], id if isinstance(id, int) else f"'{id}'")

    cursor.execute(q)
    try:
        return cursor.fetchone()
    except:
        return None


@connection
def fetch_data(modelcls, filter, cursor=None):
    q = "SELECT * FROM {} ".format(_get_table_name(modelcls.__name__))
    if filter:
        q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in filter.items()])+";"
    cursor.execute(q)
    return cursor.fetchall()


@connection
def get_data(modelcls, filter, cursor=None):
    q = "SELECT * FROM {} ".format(_get_table_name(modelcls.__name__))
    q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in filter.items()])+';'
    cursor.execute(q)
    return cursor.fetchone()


@connection
def update(model, filter, cursor=None):
    q = 'UPDATE {} SET '.format(_get_table_name(model.__class__.__name__))
    q += ', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in model.data.items()])+" "
    q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in _get_filter_items(model, filter)])+";"
    cursor.execute(q)


@connection
def create(model, cursor=None):
    q = 'INSERT INTO {}'.format(_get_table_name(model.__class__.__name__))
    q += '('+', '.join([name for name in model.data.keys()])+') '
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
        q = 'UPDATE {} SET '.format(_get_table_name(model.__class__.__name__))
        q += ', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in model.data.items()])+" "
        q += 'WHERE '+', '.join([f"{k}={v}" if isinstance(v, int) else f"{k}='{v}'" for k, v in _get_filter_items(model, filter)])+";"
        self.cur.execute(q)
    
    async def create(self, model):
        q = 'INSERT INTO {}'.format(_get_table_name(model.__class__.__name__))
        q += '('+', '.join([name for name in model.data.keys()])+') '
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


def _get_id_attr(modelcls, names):
    for name in names:
        if eval(f'modelcls.{name}.is_id'):
            return eval(f'modelcls.{name}.attr')
    raise Exception("ID not found")

def _get_filter_items(model, filter):
    names = model.__class__.__names__
    items = []
    for name in names:
        if name in filter.data:
            colname = eval(f"model.{name}.column_name")
            items.append((colname, filter.data[name]))
    return items


class Dao:
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
