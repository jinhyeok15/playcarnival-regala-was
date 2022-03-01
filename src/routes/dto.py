from flask import jsonify

class ResponseEntity:
    def __init__(self, data=None):
        self.data = data
    
    def push(self, data):
        self.data = data

    def response(self, code: int, message=None):
        res_body = {"status": code}
        if message:
            res_body["message"] = message
        if self.data:
            res_body.update(self.data)
        return jsonify(res_body)

# record
class RecordRegalaDto(ResponseEntity):
    def __init__(self, equipment_id: int, req_body):
        super().__init__()
        self.equipment_id = equipment_id
        self.user_id = req_body.get("user_id")
