# 프로젝트 설명

<img width="862" alt="image" src="https://user-images.githubusercontent.com/82345753/217802276-2ef8c25d-6ccb-4b6e-a835-fce91f4631a0.png">

## Install Guide
### Prerequistion 
1. ROS
2. usb cam
    - avframe_camera_size_ = avpicture_get_size(AV_PIX_FMT_YUV420P, image_width, image_height); 
3. Camera Info Manager 
4. v4l2-ctl
 - sudo apt-get install v4l-utils
 - v4l-utils v4l2-ctl --list-devices

5. opencv python install
 - sudo python3 -m pip install opencv-python opencv-contrib-python

6. scikit-learn install 

## Code
### Core Code
1. rtsp_test.py  : 카메라 ON / OFF
2. video_stitcher.py : 이미지 스티칭
3. video_recorder.py : 녹화
4. google_drive_test.py : 구글 드라이브 업로드

### 카메라 연결 관련

* requirements
1. pip install Flask
2. pip install redis
3. pip install pymysql

### 실행 파일 관련 내용
* references
> 1. redis   
https://blog.devgenius.io/how-to-use-redis-pub-sub-in-your-python-application-b6d5e11fc8de   
https://www.twilio.com/blog/sms-microservice-python-twilio-redis-pub-sub?utm_source=pocket_mylist
> 2. flask   
https://rekt77.tistory.com/103

* 실행 명령
> python sub.py
> python videosub.py
> python app.py
    세 명령어 모두 다른 스크린에서 수행. 추후 dockerfile로 build할 경우 내용 변경 가능.

* app.py
> 클라이언트에서 접속할 서버를 켜두는 파일.   
> record_regala   
> 클라이언트에서 request를 보낼 경우 보낸 user_id 와 equipment_id 정보가 publish되며,
> response로 전달 받았던 user_id와 equipment_id를 돌려준다.
> get_record_state   
> 클라이언트에서 request를 보낼 경우, DB의 현재 촬영 상태를 돌려준다.

* sub.py
> app.py에서 publish한 메시지를 전달받아 촬영 실행을 수행하는 파일.

> 1. test용 함수   
> 1-1. rtsp_func   
> 카메라 on/off 관련 파일 실행을 위한 함수   
> 1-2. recorder_func   
> 카메라 촬영 관련 함수   
> 1-3. upload_func   
> 영상을 로컬 및 구글 드라이브에 저장하는 함수   
> ** 필수 ** 구글 드라이브에 저장한 url은 data에 update해서 publish 해주어야 한다   
