from .model import Model

class User(Model):
    user_id = Model.Column('user_idx', int, ID=True)
    user_name = Model.Column('user_name', str)
    user_phone = Model.Column('user_phone', str)
    created_at = Model.Column('created_at', Model.time)
    modified_at = Model.Column('modified_at', Model.time)
    user_enabled = Model.Column('user_enabled', int)
    user_social_id = Model.Column('user_social_idx', str)

    __names__ = ['user_id', 'user_name', 'user_phone', 'created_at', 'modified_at', 'user_enabled', 'user_social_id']
