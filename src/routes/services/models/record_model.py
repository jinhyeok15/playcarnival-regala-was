from .. import models

class Equipment(models.Model):
    def __init__(self, data=None):
        super().__init__(self.__names__, data)

    equipment_id = models.Model.Column('equipment_idx', int, ID=True)
    stadium_id = models.Model.Column('equipment_stadium_idx', int)
    equipment_qr = models.Model.Column('equipment_qr', str)
    service_state = models.Model.Column('equipment_service_state', int)
    state = models.Model.Column('equipment_state', int)
    created_at = models.Model.Column('created_at', models.Model.time)
    modified_at = models.Model.Column('modified_at', models.Model.time)
    host = models.Model.Column('equipment_host', str)

    __names__ = [
            'equipment_id', 'stadium_id', 'equipment_qr', 'service_state', 'state', 'created_at', 'modified_at', 'host'
        ]


class Stadium(models.Model):
    def __init__(self, data=None):
        super().__init__(self.__names__, data)

    stadium_id = models.Model.Column('stadium_idx', int, ID=True)
    name = models.Model.Column('stadium_name', str)
    address = models.Model.Column('stadium_address', str)
    operating_hours = models.Model.Column('stadium_operating_hours', str)
    phonenumber = models.Model.Column('stadium_number', str)
    latitude = models.Model.Column('stadium_latitude', str)
    longitude = models.Model.Column('stadium_longitude', str)
    trouble_state = models.Model.Column('stadium_trouble_state', int)
    stadiumQr = models.Model.Column('stadiumQR', str)
    stadium_img = models.Model.Column('stadium_img', str)
    created_at = models.Model.Column('created_at', models.Model.time)
    modified_at = models.Model.Column('modified_at', models.Model.time)

    __names__ = [
                'stadium_id', 'name', 'address', 'operating_hours',
                'phonenumber', 'latitude', 'longitude', 'trouble_state', 'stadiumQr',
                'stadium_img', 'created_at', 'modified_at'
            ]


class RecordState(models.Model):
    def __init__(self, data=None):
        super().__init__(self.__names__, data)

    equipment_id = models.Model.Column('equipment_equipment_idx', int, ID=True)
    user_id = models.Model.Column('user_user_idx', int)
    status = models.Model.Column('record_status', str)
    updated_at = models.Model.Column('record_state_updateTime', models.Model.time)

    __names__ = ['equipment_id', 'user_id', 'status', 'updated_at']
