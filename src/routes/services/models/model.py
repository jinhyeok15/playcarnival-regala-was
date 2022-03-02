from datetime import datetime

class Model:
    time = datetime
    def __init__(self, __dict__={}):
        self.data = __dict__
        self.__names__ = []
        for key, value in __dict__.items():
            if type(value)==str:
                value = "'''"+value+"'''"
            eval('self.{}.put({})'.format(key, value))
            self.__names__.append(key)

    class Column:
        def __init__(self, column_name, column_type, ID=False):
            self.column_name = column_name
            self.column_type = column_type
            self.attr = (column_name, column_type)
            self.is_id = ID
        
        def put(self, value):
            if not isinstance(value, self.column_type):
                raise TypeError
            else:
                self.attr = self.column_name, value
            return self
        
        def get(self):
            return self.attr[1]
    
    def get(self, name):
        return self.data[eval(f'self.{name}.column_name')]
    
    def set_instance(self, data):
        names = self.__class__.__names__
        for name in names:
            try:
                column = eval(f'self.{name}')
                value = data[column.column_name]
                eval(f"self.{name}.put(self.string_to('{value}', {column.column_type.__name__}))")
            except:
                raise KeyError("Data key is not matched with model columns")
        self.data.update(data)
        return self
    
    @staticmethod
    def string_to(value, column_type):
        if column_type.__name__==Model.time.__name__:
            return Model.time.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            return column_type(value)
