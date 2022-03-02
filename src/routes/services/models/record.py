from .model import Model

class Equipment(Model):
    equipment_id = Model.Column('equipment_idx', int, ID=True)
    stadium_id = Model.Column('equipment_stadium_idx', int)
    equipment_qr = Model.Column('equipment_qr', str)
    service_state = Model.Column('equipment_service_state', int)
    state = Model.Column('equipment_state', int)
    created_at = Model.Column('created_at', Model.time)
    modified_at = Model.Column('modified_at', Model.time)
    host = Model.Column('equipment_host', str)

    __names__ = [
        'equipment_id', 'stadium_id', 'equipment_qr', 'service_state', 'state', 'created_at', 'modified_at', 'host'
    ]

class Stadium(Model):
    stadium_id = Model.Column('stadium_idx', int, ID=True)
    name = Model.Column('stadium_name', str)
    address = Model.Column('stadium_address', str)
    operating_hours = Model.Column('stadium_operating_hours', str)
    phonenumber = Model.Column('stadium_number', str)
    latitude = Model.Column('stadium_latitude', str)
    longitude = Model.Column('stadium_longitude', str)
    trouble_state = Model.Column('stadium_trouble_state', int)
    stadiumQr = Model.Column('stadiumQR', str)
    stadium_img = Model.Column('stadium_img', str)
    created_at = Model.Column('created_at', Model.time)
    modified_at = Model.Column('modified_at', Model.time)

    __names__ = [
        'stadium_id', 'name', 'address', 'operating_hours',
        'phonenumber', 'latitude', 'longitude', 'trouble_state', 'stadiumQr',
        'stadium_img', 'created_at', 'modified_at'
    ]

class RecordState(Model):
    equipment_id = Model.Column('equipment_equipment_idx', int, ID=True)
    user_id = Model.Column('user_user_idx', int)
    status = Model.Column('record_status', str)
    updated_at = Model.Column('record_state_updateTime', Model.time)

    __names__ = ['equipment_id', 'user_id', 'status', 'updated_at']
