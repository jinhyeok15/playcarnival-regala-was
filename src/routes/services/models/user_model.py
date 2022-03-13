from .. import models

class User(models.Model):
    def __init__(self, data=None):
        super().__init__(self.__names__, data)

    user_id = models.Model.Column('user_idx', int, ID=True)
    user_name = models.Model.Column('user_name', str)
    user_phone = models.Model.Column('user_phone', str)
    created_at = models.Model.Column('created_at', models.Model.time)
    modified_at = models.Model.Column('modified_at', models.Model.time)
    user_enabled = models.Model.Column('user_enabled', int)
    user_social_id = models.Model.Column('user_social_idx', str)

    __names__ = ['user_id', 'user_name', 'user_phone', 'created_at', 'modified_at', 'user_enabled', 'user_social_id']
