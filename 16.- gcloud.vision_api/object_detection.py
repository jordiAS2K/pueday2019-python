# Doc: https://cloud.google.com/vision/
# La API Cloud Vision utiliza modelos ya preparados y permite crear modelos personalizados y flexibles que se adaptan a 
# cada caso práctico a través de AutoML Vision.
#
# Usage
# python object_detection.py --image resources/duck_and_truck.jpg

# Import the necessary packages
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import argparse


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to where the image file resides")
args = vars(ap.parse_args())

# The Google Cloud Vision API allows developers to easily integrate vision detection features within applications, 
# including image labeling, face and landmark detection, optical character recognition (OCR), and tagging of explicit content.

# Authenticate API requests
# Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/credentials.json"


# The name of the image file to annotate
# os.path.dirname(__file__): absolute dir the script is in
filename = os.path.join(os.path.dirname(__file__), args["image"])

# Loads the image into memory
with io.open(filename, 'rb') as file:
    content = file.read()

# Instantiates a client
client = vision.ImageAnnotatorClient()
image = types.Image(content = content)

# Performs object localization on the image file
response = client.object_localization(image)

# Process the response
objects  = response.localized_object_annotations

print(f'Number of objects found: {len(objects)}')
for obj in objects:
    print(f'{obj.name} (confidence: {obj.score})')
    print('Normalized bounding polygon vertices: ')
    for vertex in obj.bounding_poly.normalized_vertices:
            print(f' - ({vertex.x}, {vertex.y})')




