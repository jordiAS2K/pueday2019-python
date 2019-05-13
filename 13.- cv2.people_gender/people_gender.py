# Usage:
# python people_gender.py --full
# python people_gender.py --image images/sample.jpg --full
# python people_gender.py --image images/couple.jpg --full
# python people_gender.py --image images/hoffman.jpg --full

# Import required modules
import math
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = False, help = "path to where the image resides  (optional)")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode  (optional)")
args = vars(ap.parse_args())

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            boxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, boxes


# Configure windows
windowName = "Gender Detection"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#Models por face
faceProto = "models/opencv_face_detector.pbtxt"
faceModel = "models/opencv_face_detector_uint8.pb"

#Models for ages
ageProto = "models/age_deploy.prototxt"
ageModel = "models/age_net.caffemodel"

#Models for gender
genderProto = "models/gender_deploy.prototxt"
genderModel = "models/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Hombre', 'Mujer']

# Load network
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
faceNet = cv2.dnn.readNet(faceModel, faceProto)

# Open a video file or an image file or a camera stream
if (args["image"]):
	frame = cv2.imread(args["image"])
else:
    video = cv2.VideoCapture(cv2.CAP_DSHOW)

padding = 20
while True:
    # Read frame
    if(not args["image"]): (grabbed, frame) = video.read()

    (frameFace, boxes) = getFaceBox(faceNet, frame)
   
    for box in boxes:
        face = frame[max(0,box[1]-padding):min(box[3]+padding,frame.shape[0]-1),max(0,box[0]-padding):min(box[2]+padding, frame.shape[1]-1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        
        label = "{},{}".format(gender, age)
        cv2.putText(frameFace, label, (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow(windowName, frameFace)

    cv2.imshow(windowName, frameFace)
    
    key = cv2.waitKey(1)
    if (args["image"] or key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1):
        break

if (args["image"]): cv2.waitKey(0)

# close all windows
cv2.destroyAllWindows()


