from models.record import *
from models.user import *
from models.dao import *

from _redis import getRedis

red = getRedis()

async def record_regala(dto):
    user_id = dto.user_id
    user = findById(User, user_id)

    if not user:
        return dto.response(403, "NOT_VALID_ACCESS")
    
    equipment_id = dto.equipment_id
    equipment = findById(Equipment, equipment_id)

    if not equipment:
        return dto.response(404, "UNREGISTERED_EQUIPMENT")
    
    stadium = findById(Stadium, equipment.stadium_id.get())

    sql_session = SQLSession()

    data = {"request": dto.data}
    dto.push(data)
    return dto.response(200)
