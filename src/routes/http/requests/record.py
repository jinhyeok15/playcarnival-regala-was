from routes.http import Data

# record
class RecordRegalaRequest(Data):
    __name__ = 'RequestData'
    def __init__(self, equipment_id: int, req_body):
        super().__init__()
        self.equipment_id = equipment_id
        self.user_id = req_body.get("user_id")
