from manage import getRedis, DAO

from multiprocessing import Process
import json

redis_conn= getRedis()
dao = DAO()

import time
# rtsp_test.func()
def rtsp_func():
    time.sleep(3)
    print('turn on complete!')

# video_recorder.func()
def recorder_func(data):
    data = json.loads(data)
    user_id = data.get("user_id")
    equipment_id = data.get("equipment_id")
    time.sleep(10)
    print(f'record start\nuser_id: {user_id},\nequipment: {equipment_id}')

# google_upload.func()
def upload_func(data):
    # ** 중요사항 ** url을 update해서 publish로 전달해주어야 함
    data = json.loads(data)
    url = f"www.placarnival.com/regala/google_drive/서경대 Futsal Park 2021.12.15 16:5815.mp4"
    data.update({"url": url})
    # publish 달면, videosub.py에서 subscribe해서 url db에 저장할 수 있습니다
    redis_conn.publish("video", json.dumps(data))  # publish title: video -> videosub.py subscribe
    print(f'upload success, close session.')


def sub():
    pubsub = redis_conn.pubsub()
    pubsub.subscribe("regalaData")  # subscribe 제목: app.py에서 publish할 때 사용한 title=regalaData
    for message in pubsub.listen():
        if message.get("type") == "message":
            data = message.get("data")
            rtsp_func()
            recorder_func(data)
            upload_func(data)
        else:
            print("Message listening...")


if __name__=="__main__":
    p = Process(target=sub)
    p.start()
