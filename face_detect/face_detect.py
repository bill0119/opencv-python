import cv2
import threading
import time

class captureVideo:
    def __init__(self, URL):
        self.frame = []
        self.face = []
        self.status = False
        self.isStop = False

        self.cap = cv2.VideoCapture(URL)
        # self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)

        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("FPS ", fps, ",width ", width, ",height ", height)

    def start(self):
        threading.Thread(target = self.queryFrame, daemon = True, args = ()).start()

    def stop(self):
        self.isStop = True

    def initFaceDetect(self):
        self.face = cv2.CascadeClassifier(
            'C:\Python38\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

    def faceDetect(self, frame):
        # gray image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # face detect
        faces = self.face.detectMultiScale(gray, 1.1, 4)
        # draw block
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame
    def getFrame(self):
        return self.frame

    def queryFrame(self):
        while (not self.isStop):
            self.status, self.frame = self.cap.read()

        self.cap.release()

URL = "rtsp://root:1111111a@10.16.4.169/live1s1.sdp"
video = captureVideo(URL)
video.start()
video.initFaceDetect()
time.sleep(1)

while True:
    frame = video.getFrame()

    # face detect
    frame = video.faceDetect(frame)

    cv2.imshow('Image', frame)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        video.stop()
        break
