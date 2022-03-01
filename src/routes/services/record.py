from models.record import *
from models.user import *
from models.dao import *

from _redis import getRedis

red = getRedis()

def record_regala(dto):
    data = {}
    dto.push(data)
    return dto.response(200)
