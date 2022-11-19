from flask import jsonify
from typing import List


class Data:
    def __init__(self, data={}):
        self.__data = data
    
    def __call__(self, data={}):
        self.__data = data
    
    def call(self, data):
        self.__call__(data)
        return self
    
    def add(self, entity):
        if len(entity) != 1:
            TypeError('Input value is not entity type')

        self.__data.update(entity)
    
    def get(self):
        return self.__data


class ResponseEntity:
    def __init__(self, res_name='data', many=False):
        self.__res_data = [] if many else {}
        self.__res_name = res_name
        self.many = many
        self.cursor = 0
    
    def add(self, data):
        if self.many:
            self.__res_data.append(data.get())
        else:
            self.__res_data.update(data.get())
    
    def addall(self, data_set: List[Data]):
        self.__res_data = [data.get() for data in data_set] if self.many else None

    def response(self, code: int, message=None):
        res_body = {"status": code}
        if message:
            res_body["message"] = message
        if self.__res_data:
            res_body.update({self.__res_name: self.__res_data})
        return jsonify(res_body)


class DataInterface(Data):
    __name__ = 'Data'