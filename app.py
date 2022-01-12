import cv2
import torch


# Creating a VideoCapture object to read the video
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
device = torch.device('cpu')
model = model.to(device)
cap = cv2.VideoCapture(0)

 
# Loop until the end of the video
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0)
 
    result = model([frame])
    result.render()
    cv2.imshow('Classify',result.imgs[0])
 
    # define q as the exit button
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
 
# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()