# from src import rtsp_test, video_stitcher, video_recorder, google_drive_test

from routes import app

if __name__=="__main__":
    app.run(host='0.0.0.0') # 외부 접속 가능하게 하기 위해선 localhost => 0.0.0.0으로 변경해 주셔야 합니다
