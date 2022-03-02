import json
from .models.record import *
from .models.user import *
from .models.dao import *

from ._redis import getRedis
import asyncio

red = getRedis()

async def record_regala(req, res, interface):
    user_id = req.user_id
    user = User.find_by_id(user_id)
    if not user:
        return res.response(403, "NOT_VALID_ACCESS")
    
    equipment_id = req.equipment_id
    equipment = Equipment.find_by_id(equipment_id)
    if not equipment:
        return res.response(404, "UNREGISTERED_EQUIPMENT")

    stadium = Stadium.find_by_id(equipment.get("stadium_id"))
    
    res.add(interface({"user_id": user_id}))
    res.add(interface({"equipment_id": equipment_id}))
    res.add(interface({"stadium_name": stadium.get("name")}))

    red.publish('regalaData', json.dumps(res.res_data))

    sess = SQLSession()
    await asyncio.gather(
        sess.update(Equipment(interface({"service_state": 1})), {"equipment_id": equipment_id}),
        sess.update(RecordState(interface({
            "user_id": user_id,
            "status": 'RECORD'
        })), {"equipment_id": equipment_id})
    )
    sess.commit()

    return res.response(200, "OK")


def get_record_state(req, res, interface):
    user_id = req.user_id
    user = User.find_by_id(user_id)
    
    equipment_id = req.equipment_id
    record_state = RecordState.find_by_id(equipment_id)

    if not user or user.user_id != record_state.user_id:
        return req.response(403, "NOT_VALID_ACCESS")
    
    res.add(interface({"record_status": record_state.status.get()}))
    return res.response(200, "OK")
