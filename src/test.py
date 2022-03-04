from routes.services import models
from routes.services.models import record, user
import unittest
import datetime
from routes import dto

class TestModel(unittest.TestCase):
    equipment_data = {
        'equipment_idx': 1, 
        'equipment_stadium_idx': 1, 
        'equipment_qr': 'fever', 
        'equipment_service_state': 0, 
        'equipment_state': 0, 
        'created_at': datetime.datetime(2022, 1, 14, 9, 59, 5),
        'modified_at': datetime.datetime(2022, 2, 20, 14, 35, 50), 
        'equipment_host': '52.78.23.134:5000'
    }
    
    def test_dict_in(self):
        d = {"user_id": 1, "user_name": "Jin"}
        names = ["user_id", "user_nam"]
        self.assertTrue(names[0] in d)
        self.assertFalse(names[1] in d)
    
    def test_column(self):
        interface = dto.DataInterface({"user_id": 1})
        u =  user.User(interface)
        self.assertEqual(u.get("user_id"), 1)
        self.assertEqual(u.user_id.attr, ("user_idx", 1))
    
    def test_get_column_name(self):
        interface = dto.DataInterface({"user_id": 1})
        u =  user.User(interface)
        self.assertEqual(u.user_id.__class__.__name__, "Column")
    
    def test_datetime_instance(self):
        interface = dto.DataInterface({"user_id": 1})
        u =  user.User(interface)
        print(u.created_at.column_type)
        self.assertTrue(u.created_at.column_type==u.time)
        self.assertEqual(u.created_at.column_type, u.time)


class TestDTO(unittest.TestCase):
    def test_dto_interface(self):
        self.assertEqual(dto.DataInterface().__name__, 'DTO')
        self.assertEqual(type(dict()).__name__, 'dict')
    
    def test_dto_push(self):
        itf = dto.DataInterface()
        itf.push({"user_id": 1})
        self.assertEqual(itf.data, {"user_id": 1})


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(TestDTO('test_dto_interface'))
    # suite.addTest(TestModel('test_dict_in'))
    # suite.addTest(TestModel('test_column'))
    # suite.addTest(TestModel('test_get_column_name'))
    # suite.addTest(TestModel('test_datetime_instance'))
    suite.addTest(TestDTO('test_dto_push'))
    return suite

if __name__=="__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
