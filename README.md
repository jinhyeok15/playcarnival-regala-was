# 프로젝트 개요

[ROS](https://velog.io/@717lumos/ROS-ROS-%EA%B8%B0%EB%B3%B8-%EA%B0%9C%EB%85%90) 환경의 영상 촬영 기기 내부에 flask 웹앱서버와 Redis 프로세스를 동작시키고, 앱 내에서 촬영 버튼을 클릭할 때 촬영 요청을 flask에서 받아 요청 정보를 publish한다.

redis_pubsub/video_upload.py에서 해당 요청을 subscribe하고 video 촬영과 관련한 프로세스를 처리한다. 영상 촬영 후 저장할 영상을 구글 드라이브에 저장한 후, url을 받아 publish한다.

redis_pubsub/video_query.py에서 video url을 포함한 데이터를 subscribe하여 db에 저장한다.
