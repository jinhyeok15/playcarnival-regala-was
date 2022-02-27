from model import Model

class RecordState(Model):
    equipment_id = Model.Column('equipment_equipment_idx', int, ID=True)
    user_id = Model.Column('user_user_idx', int)
    status = Model.Column('record_status', str)
    updated_at = Model.Column('record_state_updateTime', Model.time)

    __names__ = ['equipment_id', 'user_id', 'status', 'updated_at']
