from services import record

from flask import Blueprint, request
from dto import *

bp = Blueprint("record", __name__, url_prefix="/record")

@bp.route('/<int:equipment_id>', methods=['POST'])
def record_regala(equipment_id):
    req_body = request.get_json()
    dto = RecordRegalaDto(equipment_id, req_body)
    return record.record_regala(dto)
