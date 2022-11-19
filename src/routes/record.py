# flask
from flask import Blueprint, request

# services
from services.record_service import (
    record_regala_service, 
    find_record_state_service
)

# http
from routes.http import (
    ResponseEntity,
    DataInterface
)
from routes.http.requests.record import (
    RecordRegalaRequest
)

# python modules
import asyncio

bp = Blueprint("record", __name__, url_prefix="/record")

@bp.route('/<int:equipment_id>', methods=['POST'])
def route_record_regala(equipment_id):
    req_body = request.get_json()
    req = RecordRegalaRequest(equipment_id, req_body)
    res = ResponseEntity()
    interface = DataInterface
    return asyncio.run(record_regala_service(req, res, interface))

@bp.route('/<int:equipment_id>/state', methods=['POST'])
def route_get_record_state(equipment_id):
    req_body = request.get_json()
    req = RecordRegalaRequest(equipment_id, req_body)
    res = ResponseEntity()
    interface = DataInterface
    return find_record_state_service(req, res, interface)
