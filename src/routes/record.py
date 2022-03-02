from routes.services import record

from flask import Blueprint, request
from routes.dto import *
import asyncio

bp = Blueprint("record", __name__, url_prefix="/record")

@bp.route('/<int:equipment_id>', methods=['POST'])
def record_regala(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    res = ResponseEntity("request")
    return asyncio.run(record.record_regala(dto, res))

@bp.route('/<int:equipment_id>/state', methods=['POST'])
def get_record_state(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    res = ResponseEntity("recordStatus")
    return record.get_record_state(dto, res)
