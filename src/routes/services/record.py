import json
from .models.record import *
from .models.user import *
from .models.dao import *

from ._redis import getRedis
import asyncio

red = getRedis()

async def record_regala(dto, res):
    user_id = dto.user_id
    user = findById(User, user_id)

    if not user:
        return dto.response(403, "NOT_VALID_ACCESS")
    res.add(user.user_id)
    
    equipment_id = dto.equipment_id
    equipment = findById(Equipment, equipment_id)
    
    if not equipment:
        return dto.response(404, "UNREGISTERED_EQUIPMENT")
    res.add(equipment.equipment_id)
    
    stadium = findById(Stadium, equipment.stadium_id.get())
    res.add(stadium.name)

    red.publish('regalaData', json.dumps(res.data))

    sess = SQLSession()
    await asyncio.gather(
        sess.update(Equipment({"service_state": 1}), {"equipment_id": equipment_id}),
        sess.update(RecordState({
            "user_id": user_id,
            "status": 'RECORD'
        }), {"equipment_id": equipment_id})
    )
    sess.commit()

    return dto.response(200, data=res.data)


def get_record_state(dto, res):
    user_id = dto.user_id
    user = findById(User(), user_id)
    
    equipment_id = dto.equipment_id
    record_state = findById(RecordState, equipment_id)

    if not user or user.user_id != record_state.user_id:
        return dto.response(403, "NOT_VALID_ACCESS")
    
    res.add(record_state.status)
    return dto.response(200, data=res.data)
