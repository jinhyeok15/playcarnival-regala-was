import json
from .models.record_model import *
from .models.user_model import *
from .models.dao import *

from ._redis import getRedis
import asyncio

red = getRedis()

async def record_regala(req, res, interface):
    itf = interface()
    user_id = req.user_id
    user = User.find_by_id(user_id)
    if not user:
        return res.response(403, "NOT_VALID_ACCESS")
    
    equipment_id = req.equipment_id
    equipment = Equipment.find_by_id(equipment_id)
    if not equipment:
        return res.response(404, "UNREGISTERED_EQUIPMENT")

    stadium = Stadium.find_by_id(equipment.get("stadium_id"))

    itf.push({"user_id": user_id})
    itf.add({"equipment_id": equipment_id})
    itf.add({"stadium_name": stadium.get("name")})
    res.add(itf)

    red.publish('regalaData', json.dumps(res.res_data))

    sess = SQLSession()
    await asyncio.gather(
        sess.update(Equipment(itf.push({"service_state": 1})), itf.push({"equipment_id": equipment_id})),
        sess.update(RecordState(itf.push({
            "user_id": user_id,
            "status": 'RECORD'
        })), itf.push({"equipment_id": equipment_id}))
    )
    sess.commit()

    return res.response(200, "OK")


def get_record_state(req, res, interface):
    itf = interface()
    user_id = req.user_id
    user = User.find_by_id(user_id)
    
    equipment_id = req.equipment_id
    record_state = RecordState.find_by_id(equipment_id)

    if not user or user.user_id != record_state.user_id:
        return req.response(403, "NOT_VALID_ACCESS")
    
    itf.push({"record_status": record_state.status.get()})
    res.add(itf)
    return res.response(200, "OK")
