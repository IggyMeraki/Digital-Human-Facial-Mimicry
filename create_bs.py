from utils.faceCapture import FaceMeshDetector
import numpy as np
import os

class Create_BS:
    def __init__(self):
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.result_path = os.path.join(self.script_path, "npy")
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        self.file_name = "pose.npy"
        self.bs_data = []
        self.detector = FaceMeshDetector()

    def proccess_frame(self,frame):
        self.detector.update(frame,True)
        lm,bs,rm = self.detector.get_results()
        if lm is not None and bs is not None and rm is not None:
            self.bs_data.append(bs)

    def stop_record(self):
        np.save(os.path.join(self.result_path, self.file_name), np.array(self.bs_data))
        self.bs_data = []

if __name__ == '__main__':
    ceate_bs = Create_BS()
    ceate_bs.ceate_bs()