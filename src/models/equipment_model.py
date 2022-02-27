from model import Model

class Equipment(Model):
    equipment_id = Model.Column('equipment_idx', int, ID=True)
    stadium_id = Model.Column('equipment_stadium_idx', int)
    equipment_qr = Model.Column('equipment_qr', str)
    service_state = Model.Column('equipment_service_state', int)
    state = Model.Column('equipment_state', int)
    create_at = Model.Column('create_at', Model.time)
    modified_at = Model.Column('modified_at', Model.time)
    host = Model.Column('equipment_host', str)

    __names__ = [
        'equipment_id', 'stadium_id', 'equipment_qr', 'service_state', 'state', 'create_at', 'modified_at', 'host'
    ]
