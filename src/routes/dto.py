from flask import jsonify

class DTO:
    def __init__(self, data={}):
        self.data = data
    
    def push(self, data):
        self.data = data


class ResponseEntity:
    def __init__(self, res_name='data', many=False):
        self.res_data = [] if many else None
        self.res_name = res_name
        self.many = many
        self.cursor = 0
    
    def add(self, dto):
        if self.many:
            self.res_data.append(dto.data)
        else:
            self.res_data = dto.data
    
    def addall(self, dto_data):
        self.res_data = [dto.data for dto in dto_data] if self.many else None

    def response(self, code: int, message=None):
        res_body = {"status": code}
        if message:
            res_body["message"] = message
        if self.res_data:
            res_body.update({self.res_name: self.res_data})
        return jsonify(res_body)


class DataInterface(DTO):
    __name__ = 'DTO'


# record
class RecordRegalaDto(DTO):
    __name__ = 'DTO'
    def __init__(self, equipment_id: int, req_body):
        super().__init__()
        self.equipment_id = equipment_id
        self.user_id = req_body.get("user_id")
