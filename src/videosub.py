from manage import getRedis, Dao

from multiprocessing import Process
import json

redis_conn= getRedis()
dao = Dao()

def sub():
    pubsub = redis_conn.pubsub()
    pubsub.subscribe("video")
    for message in pubsub.listen():
        if message.get("type") == "message":
            data = json.loads(message.get("data"))

            # video_title ex) 서경대 Futsal Park 2021.12.15 16:5815
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%Y%m%d%H%M%S")
            video_title = data.get("stadium_name") + current_time

            dao.execute(
                '''
                    UPDATE equipment
                    SET equipment_service_state = 0
                    WHERE equipment_idx=%s;
                ''', data.get("equipment_id")
            )

            dao.execute(
                '''
                    UPDATE record_state
                    SET user_user_idx = %s, record_status = 'UPLOAD'
                    WHERE equipment_equipment_idx = %s;
                ''', (data.get("user_id"), data.get("equipment_id"))
            )

            dao.execute(
                '''
                    INSERT INTO 
                    video (video_url, video_title, video_equipment_idx, video_user_idx)
                    VALUES (%s, %s, %s, %s);
                ''', (data.get("url"), video_title, data.get("equipment_id"), data.get("user_id"))
            )
            dao.save()
            print("All job success!!")
        else:
            print("message listening...")


if __name__=="__main__":
    p = Process(target=sub)
    p.start()
