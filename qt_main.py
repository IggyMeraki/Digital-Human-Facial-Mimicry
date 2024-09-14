from qt_ui.qt_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QUrl,QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy
from create_bs import Create_BS
from run_blender import run_blender
import cv2
import threading
import time



class Communicate(QObject):
    update_text = pyqtSignal(str)
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initcomm()

        self.quit = False

        self.cap = cv2.VideoCapture(1)  # 打开摄像头
        self.timeout = 10               #设定最长录制多少秒
        self.bs = Create_BS()

        self.recordButton.clicked.connect(lambda: self.state_change(True))
        self.recordButton.setEnabled(True)
        self.stopButton.clicked.connect(lambda: self.state_change(False))
        self.stopButton.setEnabled(False)
        self.playButton.clicked.connect(self.play_video)
        self.playButton.setEnabled(False)

        self.on_off_state = False

        #################### 启动摄像头
        # 设置定时器，每30ms调用一次 update_frame 函数
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(40)
        ################################# WWWWWWWWWWWWWWWWWWWWW

        self.bs_thread = None
        self.bs_thread = threading.Thread(target=self.create_bs)
        self.bs_thread.start()

        self.blender_thread = threading.Thread(target=run_blender,args = (self.comm_state,self.playButton,))
        self.comm_msg.update_text.emit(f"欢迎使用Blender GUI\n本项目基于Blender和AI模型，通过AI模型对人脸进行学习、模仿，并最终驱动Blender虚拟数字人物进行表情模仿\n请点击开始录制按钮进行录制(最长录制{self.timeout}秒)\n由于AI模型需要时间推理，请耐心等待\n")

        # 创建视频播放器和视频窗口
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        self.label_video_detect.setLayout(layout)
        self.label_video_detect.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChange)

    def initcomm(self):
        self.comm_state = Communicate()
        self.comm_state.update_text.connect(self.update_state)
        self.comm_msg = Communicate()
        self.comm_msg.update_text.connect(self.update_msg)

    def update_state(self, text):
        self.textBrowser_state.insertPlainText(text)
        self.textBrowser_state.verticalScrollBar().setValue(self.textBrowser_state.verticalScrollBar().maximum())

    def update_msg(self, text):
        self.textBrowser_msg.insertPlainText(text)
        self.textBrowser_msg.verticalScrollBar().setValue(self.textBrowser_msg.verticalScrollBar().maximum())

    def play_video(self):
        video_path = "outputs/blender.mp4"  # 替换为本地视频路径
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.mediaPlayer.play()
        self.playButton.setEnabled(False)
        self.recordButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.comm_state.update_text.emit("正在播放渲染结果...\n")

    def handleMediaStatusChange(self,status):
        if status == QMediaPlayer.EndOfMedia:
            self.comm_state.update_text.emit("渲染结果播放结束\n")
            self.playButton.setEnabled(True)
            self.recordButton.setEnabled(True)
            self.mediaPlayer.setMedia(QMediaContent())
            self.mediaPlayer.stop()

    def state_change(self, state,timeout = False):
        if state:
            self.start_time = time.time()
            self.on_off_state = True
            self.recordButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.playButton.setEnabled(False)
            self.comm_state.update_text.emit("开始录制\n")
            self.timer3 = QTimer()
            self.timer3.timeout.connect(lambda: self.state_change(False,True))
            self.timer3.start(self.timeout*1000)
        else:
            self.stop_time = time.time()
            self.record_time = self.stop_time - self.start_time
            self.comm_state.update_text.emit("录制时间：%.2f秒\n" % self.record_time)
            self.timer3.stop()
            if timeout == True:
                self.comm_state.update_text.emit(f"录制超{self.timeout}s自动结束\n")
            else:
                self.comm_state.update_text.emit("录制结束\n")
            self.on_off_state = False
            self.recordButton.setEnabled(True)
            self.stopButton.setEnabled(False)
            self.playButton.setEnabled(True)
            self.comm_state.update_text.emit("AI模型推理中......\n")
            self.bs.stop_record()
            print("保存bs")
            self.blender_thread = threading.Thread(target=run_blender,args = (self.comm_state,self.playButton,self.recordButton,))
            self.blender_thread.start()

    def create_bs(self):
        try:
            while True:
                if self.on_off_state:
                    t1 = time.time()
                    image_flag, image = self.cap.read()
                    if image_flag:
                        self.bs.proccess_frame(image)
                    else:   
                        try:
                            raise Exception("Camera Error")
                        except Exception as e:
                            print(e)
                            self.comm_state.update_text.emit("摄像头打开失败，请检查摄像头是否连接正确\n程序将在3s后自动退出\n")
                            time.sleep(3)
                            QMainWindow.close(self)
                    # print("create bs time:", time.time() - t1)
                else:
                    pass
                if self.quit:
                    break
        except Exception as e:
            print(e)

    def update_frame(self):
        # 从摄像头读取一帧
        ret, frame = self.cap.read()

        if ret:
            # try :
            # 将 BGR 格式转换为 RGB 格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)

            # # 使用cv2.resize进行降采样            
            frame = cv2.resize(frame, (self.label_video_origin.size().width(),  self.label_video_origin.size().height()), interpolation=cv2.INTER_LINEAR)

            # 获取图像大小并创建 QImage
            h, w, ch = frame.shape
            bytes_per_line = ch * w         # h,w    (480, 640)
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # 将 QImage 显示在 QLabel 中
            self.label_video_origin.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        # 在窗口关闭时清理资源
        self.quit = True
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        if self.bs_thread is not None and self.bs_thread.is_alive():
            self.bs_thread.join()
        if self.blender_thread is not None and self.blender_thread.is_alive():
            self.blender_thread.join()
        event.accept()
        QApplication.quit()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())