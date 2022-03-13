from routes.services import record_service

from flask import Blueprint, request
from routes.dto import *
import asyncio

bp = Blueprint("record", __name__, url_prefix="/record")

@bp.route('/<int:equipment_id>', methods=['POST'])
def record_regala(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    res = ResponseEntity("request")
    interface = DataInterface
    return asyncio.run(record_service.record_regala(dto, res, interface))

@bp.route('/<int:equipment_id>/state', methods=['POST'])
def get_record_state(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    res = ResponseEntity("recordStatus")
    interface = DataInterface
    return record_service.get_record_state(dto, res, interface)
