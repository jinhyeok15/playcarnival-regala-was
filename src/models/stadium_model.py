from model import Model

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
