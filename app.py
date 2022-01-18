import cv2
import torch
from argparse import ArgumentParser
import pafy
import re
import warnings
import time
import os

  
YOUTUBE_REGEX = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


class ObjectDetection :
    def __init__(self, youtube_url="", video_path=""):
        self.youtube_url = youtube_url
        self.video_path = video_path
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device=device)

    def run(self):
        # Loop until the end of the video
        if self.youtube_url == "":
            if self.video_path == "":
                stream = cv2.VideoCapture(0)
            else:
                stream = cv2.VideoCapture(self.video_path)
        else:
            # Check if this is a valid youtube url
            if re.match(YOUTUBE_REGEX, self.youtube_url):
                # Download the video
                video_path = self.download_best(self.youtube_url)            
                stream = cv2.VideoCapture(video_path)
            else:
                print('Invalid youtube url: {}'.format(self.youtube_url))
                return
        # Detect Objects for given stream
        self.detect_objects(stream)
        return

    def get_video_path(self):
        index = os.system("ls inputs | wc -l")
        if not os.path.exists("inputs"):
            os.makedirs("inputs")
        video_path = "inputs/input-" + str(index) + ".mp4"
        return video_path

    def download_best(self, youtube_url):
        video = pafy.new(self.youtube_url)
        best = video.getbest(preftype="mp4")
        video_path = self.get_video_path()
        best.download(video_path)
        return video_path
    
    def detect_objects(self, stream):
        frame_rate, prev = opt.fps, 0
        while stream.isOpened():
            # Capture frame-by-frame
            _, frame = stream.read()
            time_elapsed = time.time() - prev
            
            frame = cv2.resize(frame, (640, 480), fx = 0, fy = 0)

            # Suppress warning false from yolov5 if you're not using cuda
            if opt.ignore_warnings:
                warnings.filterwarnings("ignore")
            if time_elapsed > 1./frame_rate:
                prev = time.time()
                result = self.model([frame], size=128)
                result.render()
                for img in result.imgs:
                    cv2.imshow('Classify', img)
            # define q as the exit button
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        # release the video capture object
        stream.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()
    


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--youtube_link", dest="youtube_link", type=str, help="enter a valid youtube link")
    parser.add_argument("--fps", dest="fps", type=int, help="enter desired fps")
    parser.add_argument("--ignore_warnings", dest="ignore_warnings", type=bool)
    parser.add_argument("--video_path", dest="video_path", type=str, help="enter a valid video path")
    parser.add_argument("--store_input_file", dest="store_input_file", type=str)

    parser.set_defaults(youtube_link="")
    parser.set_defaults(fps=20)
    parser.set_defaults(ignore_warnings=True)
    parser.set_defaults(video_path="")
    parser.set_defaults(store_input_file='N')
    
    opt = parser.parse_args()
    obj = ObjectDetection(opt.youtube_link, opt.video_path)
    obj.run()
    
    if opt.store_input_file == 'N':
        os.system("rm -f inputs/*")