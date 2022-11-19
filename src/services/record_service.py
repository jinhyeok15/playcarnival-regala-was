# models
from models.record_model import (
    Equipment,
    Stadium,
    RecordState
)
from models.user_model import (
    User,
)
from models.database import (
    SQLSession
)

# management
from manage import get_redis

# constants
from redis_pubsub.topics import PLAY_CAMERA

# python modules
import json
import asyncio

redis_conn = get_redis()

async def record_regala_service(req, res, interface):
    data_obj = interface()

    user_id = req.user_id
    user = User.find_by_id(user_id)
    if not user:
        return res.response(403, "NOT_VALID_ACCESS")
    
    equipment_id = req.equipment_id
    equipment = Equipment.find_by_id(equipment_id)
    if not equipment:
        return res.response(404, "UNREGISTERED_EQUIPMENT")

    stadium = Stadium.find_by_id(equipment.get("stadium_id"))

    data_obj.call({
        "user_id": user_id,
        "equipment_id": equipment_id,
        "stadium_name": stadium.get("name")
    })
    
    res.add(data_obj)

    redis_conn.publish(PLAY_CAMERA, json.dumps(res.res_data))

    # transaction
    sess = SQLSession()
    await asyncio.gather(
        sess.update(Equipment(data_obj.call({"service_state": 1})), data_obj.call({"equipment_id": equipment_id})),
        sess.update(RecordState(data_obj.call({
            "user_id": user_id,
            "status": 'RECORD'
        })), data_obj.call({"equipment_id": equipment_id}))
    )
    sess.commit()

    return res.response(200, "OK")


def find_record_state_service(req, res, interface):
    data_obj = interface()

    user_id = req.user_id
    user = User.find_by_id(user_id)
    
    equipment_id = req.equipment_id
    record_state = RecordState.find_by_id(equipment_id)

    if not user or user.user_id != record_state.user_id:
        return req.response(403, "NOT_VALID_ACCESS")
    
    data_obj.call({"record_status": record_state.status.get()})
    res.add(data_obj)
    return res.response(200, "OK")
