from services.record_service import record_regala_service, get_record_state_service

from flask import Blueprint, request
from routes.dto import *
import asyncio

bp = Blueprint("record", __name__, url_prefix="/record")

@bp.route('/<int:equipment_id>', methods=['POST'])
def record_regala_service(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    res = ResponseEntity("request")
    interface = DataInterface
    return asyncio.run(record_regala_service(dto, res, interface))

@bp.route('/<int:equipment_id>/state', methods=['POST'])
def get_record_state_service(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    res = ResponseEntity("recordStatus")
    interface = DataInterface
    return get_record_state_service(dto, res, interface)
