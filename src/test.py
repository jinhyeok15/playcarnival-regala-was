from routes.services.models import record, user

if __name__=="__main__":
    import datetime
    data = {'equipment_idx': 1, 
    'equipment_stadium_idx': 1, 
    'equipment_qr': 'fever', 
    'equipment_service_state': 0, 
    'equipment_state': 0, 
    'created_at': datetime.datetime(2022, 1, 14, 9, 59, 5),
    'modified_at': datetime.datetime(2022, 2, 20, 14, 35, 50), 
    'equipment_host': '52.78.23.134:5000'}
    ins = record.Equipment().set_instance(data)
    