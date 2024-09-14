
# for linux readme

1. requirements.txt 文件内容如下：
mediapipe==0.10.14
numpy==1.24.4
opencv-contrib-python-headless==4.10.0.84
PyQt5==5.15.11
PyQt5_sip==12.15.0
scipy==1.9.1

2. 摄像头读取翻转，qt_main.py中有两处要更改（可视化部分、mp推理部分）
image = cv2.flip(image, -1)

3. play_video函数中video_path使用绝对路径，否则无法读取视频文件