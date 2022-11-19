from datetime import datetime

from pymysql import DatabaseError

from .database import (
    get_data_by_id,
    fetch_data,
    get_data,
    update,
    create
)


class Model:
    time = datetime
    def __init__(self, __names__, data=None):
        self.__names__ = __names__
        self.data = {}
        if not data:
            pass
        elif isinstance(data, dict):
            self.data.update(data)
            self.__names__ = []
            tmp = []
            for name in __names__:
                colname = eval(f'self.{name}.column_name')
                coltype = eval(f'self.{name}.column_type.__name__')
                if colname in data:
                    value = data[colname]
                    value = f"'''{value}'''"
                    eval('self.{}.put(self._string_to({}, {}))'.format(name, value, coltype))
                    tmp.append(name)
            self.__names__ = tmp
        elif data.__name__=="DTO":
            self._set_model_by_dto_data(data.data)
    
    def _set_model_by_dto_data(self, dto_data):
        names = self.__names__
        tmp = []
        for name in names:
            colname = eval(f'self.{name}.column_name')
            coltype = eval(f'self.{name}.column_type.__name__')
            if name in dto_data:
                value = dto_data[name]
                self.data[colname] = value
                value = f"'''{value}'''"
                eval('self.{}.put(self._string_to({}, {}))'.format(name, value, coltype))
                tmp.append(name)
        self.__names__ = tmp
    
    def _string_to(self, value, column_type):
        if value=='None':
            return None
        elif column_type==self.time:
            return self.time.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif column_type==int:
            return int(value)
        else:
            return column_type(value)


    class Column:
        def __init__(self, column_name, column_type, ID=False):
            self.column_name = column_name
            self.column_type = column_type
            self.attr = (column_name, column_type)
            self.is_id = ID
        
        def put(self, value):
            if not value:
                self.attr = self.column_name, None
            elif not isinstance(value, self.column_type):
                raise TypeError
            else:
                self.attr = self.column_name, value
            return self
        
        def get(self):
            return self.attr[1]
    
    def get(self, name):
        return self.data[eval(f'self.{name}.column_name')]
    
    @classmethod
    def find_by_id(cls, id):
        dto_data = get_data_by_id(cls, id)
        return cls(dto_data)
    
    @classmethod
    def find(cls, filter):
        dto_data = fetch_data(cls, filter)
        return [cls(entity) for entity in dto_data]
    
    @classmethod
    def find_one(cls, filter):
        dto_data = get_data(cls, filter)
        return cls(dto_data)
    
    @classmethod
    def update(cls, filter):
        try:
            update(cls, filter)
            return 1
        except DatabaseError as e:
            print("DB update error: ", e)
            return 0
    
    @classmethod
    def create(cls):
        try:
            create(cls)
            return 1
        except DatabaseError as e:
            print("DB create error: ", e)
            return 0
