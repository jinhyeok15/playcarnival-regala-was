# from src import rtsp_test, video_stitcher, video_recorder, google_drive_test
from flask import Flask, request, jsonify
import json
from manage import DAO, getRedis

app = Flask (__name__)
red = getRedis()
dao = DAO()

@app.route('/record/<equipment_id>', methods = ['POST'])
def record_regala(equipment_id):
    req_body = request.json
    user_id = req_body.get("user_id")

    # userId로 유저 validation, get_by_equipment_id
    get_user_sql = "SELECT * FROM user WHERE user_idx=%s;"
    user = dao.findOne(get_user_sql, user_id)

    if not user:
        return jsonify({"status": 403, "message": "접근 권한 없음"})
    
    get_equipment_sql = "SELECT * FROM equipment WHERE equipment_idx=%s;"
    equipment = dao.findOne(get_equipment_sql, equipment_id)

    if not equipment:
        return jsonify({"status": 404, "message": "등록되지 않은 장치입니다"})
    
    req_body.update({"equipment_id": equipment_id})

    get_stadium_sql = "SELECT * FROM stadium WHERE stadium_idx=%s;"
    stadium = dao.findOne(get_stadium_sql, equipment['equipment_stadium_idx'])
    req_body.update({"stadium_name": stadium['stadium_name']})

    red.publish('regalaData', json.dumps(req_body))

    update_equipment_status_sql = '''
        UPDATE equipment
        SET equipment_service_state = 1
        WHERE equipment_idx=%s;
    '''
    dao.execute(update_equipment_status_sql, equipment_id)

    update_record_state_sql = '''
        UPDATE record_state
        SET user_user_idx = %s, record_status = 'RECORD'
        WHERE equipment_equipment_idx = %s;
    '''
    dao.execute(update_record_state_sql, (user_id, equipment_id))

    dao.save()

    return jsonify({"status": 200, "request":req_body})

@app.route('/record/<equipment_id>/state', methods=['POST'])
def get_record_state(equipment_id):
    req_body = request.json
    user_id = req_body.get("user_id")

    get_user_sql = "SELECT * FROM user WHERE user_idx=%s;"
    user = dao.findOne(get_user_sql, user_id)

    get_record_state_sql = "SELECT * FROM record_state WHERE equipment_equipment_idx=%s;"
    record_state = dao.findOne(get_record_state_sql, equipment_id)

    if not user or user['user_idx'] != record_state['user_user_idx']:
        return jsonify({"status": 403, "message": "접근 권한 없음"})
    return jsonify({"status": 200, "recordStatus": record_state['record_status']})


if __name__=="__main__":
    app.run(host='0.0.0.0') # 외부 접속 가능하게 하기 위해선 localhost => 0.0.0.0으로 변경해 주셔야 합니다
