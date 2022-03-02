from flask import jsonify

class ResponseEntity:
    def __init__(self, res_name='data', many=False):
        self.data = [{}] if many else {}
        self.res_name = res_name
        self.many = many
        self.cursor = 0
    
    def push(self, data):
        self.data = data
    
    def add(self, field):
        if self.many:
            self.data[self.cursor].update(dict([field.attr]))
        else:
            self.data.update(dict([field.attr]))

    def response(self, code: int, message=None, data=None):
        res_body = {"status": code}
        if message:
            res_body["message"] = message
        if data:
            res_body.update({self.res_name: data})
        return jsonify(res_body)
    
    def next(self):
        self.data.append({})
        self.cursor += 1


# record
class RecordRegalaDto(ResponseEntity):
    def __init__(self, equipment_id: int, req_body):
        super().__init__()
        self.equipment_id = equipment_id
        self.user_id = req_body.get("user_id")
