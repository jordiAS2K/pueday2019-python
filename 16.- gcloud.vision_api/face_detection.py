# Doc: https://cloud.google.com/vision/
# La API Cloud Vision utiliza modelos ya preparados y permite crear modelos personalizados y flexibles que se adaptan a 
# cada caso práctico a través de AutoML Vision.
# 
# Usage:
# python face_detection.py --image resources/crazy.jpg
# python face_detection.py --image resources/smile.jpg
# python face_detection.py --image resources/surprise.jpg
# python face_detection.py --image resources/sad.jpg

# Import the necessary packages
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to where the image file resides")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# The Google Cloud Vision API allows developers to easily integrate vision detection features within applications, 
# including image labeling, face and landmark detection, optical character recognition (OCR), and tagging of explicit content.

# Authenticate API requests
# Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/credentials.json"

# Configure windows
windowName = "Google Cloud Vision API"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# The name of the image file to annotate
# os.path.dirname(__file__): absolute dir the script is in
filename = os.path.join(os.path.dirname(__file__), args["image"])

# Loads the image into memory
with io.open(filename, 'rb') as file:
    content = file.read()

# Load image in memory
img = cv2.imread(filename)
cv2.imshow(windowName, img)

# Wait until press a key
cv2.waitKey(0)

# Instantiates a client
client = vision.ImageAnnotatorClient()
image = types.Image(content = content)

# Performs object localization on the image file
response = client.face_detection(image)

# Process the response
faces  = response.face_annotations

print(f'Number of faces found: {len(faces)}')
print(faces)
for face in faces:
    print("-------------------------------------------------")
    print(f"Confidence: {face.detection_confidence}")
    print(f"Alegre: {face.joy_likelihood}")
    print(f"Triste: {face.sorrow_likelihood}")
    print(f"Enfadado: {face.anger_likelihood}")
    print(f"Sorprendido: {face.surprise_likelihood}")
    print(f"Borroso: {face.blurred_likelihood}")
    print(f"Con sombrero: {face.headwear_likelihood}")
    print("-------------------------------------------------")
    
    points = []
    for point in face.bounding_poly.vertices:
        points.append((point.x,point.y))
        
    cv2.rectangle(img, pt1 = points[0], pt2 = points[2], color = (0,255,0), thickness = 2)        

        
cv2.imshow(windowName, img)

cv2.waitKey(0)


