class Model:
    from datetime import datetime
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
        return self.data[name]
    
    def set_data(self, data):
        for name in self.__names__:
            if not data[name]:
                raise KeyError("Data key is not matched with model columns")
            column = eval(f'self.{name})')
            column.put(data[name])
        self.data = data
