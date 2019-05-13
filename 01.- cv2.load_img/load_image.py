# Documentation:
# https://www.pyimagesearch.com/2014/06/02/opencv-load-image/
# Usage:
# python load_image.py --image images/image-001.jpg --full

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to where the image file resides")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# Configure windows
windowName = "Image Visualizer"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Loading the image using OpenCV
# The cv2.imread function returns a NumPy array representing the image
image = cv2.imread(args["image"])

# The NumPy shape may seem reerse to you (specifiying the height before the width),
# but in terms of a matrix definition it actually makes sense. When we define
# matrices, it is common to write them in the form of #rows x #columns

# Show image info
print(f"Width: {image.shape[1]} pixels")
print(f"Height: {image.shape[0]} pixels")
print(f"Channels: {image.shape[2]}")

# Display the image to our screen
cv2.imshow(windowName, image)


# Note: OpenCV stores RGB channels in reverse order.
# While we normally think in terms of Red, Green and Blue; OpenCV actually stores them in 
# the following order: Blue, Green and Red

# Get the pixel located at (0,0) represented as a tuple (b,g,r)
copy = image.copy()
(b, g, r) = copy[0, 0]
print(f"Pixel at (0,0) - RGB: ({r}, {g}, {b})")

# Modify the pixel located at (0,0)
copy[0, 0] = (0,0,255)
(b, g, r) = copy[0, 0]
print(f"Pixel at (0,0) - RGB: ({r}, {g}, {b})")

# Use NumPy array slicing capabilities to access larger rectangular portions of image
copy [0:100, 0: 100] = (0,0,0)

cv2.imshow("Modified Image", copy)

# Write our image to disk
cv2.imwrite("images/demo.jpg", copy)

# Wait for a key press to finish program
# It’s very important that we make a call to this function, otherwise our window will close automatically!
# If we removed, then the window containing our image would close automatically. By making a call to cv2.waitKey, 
# we are able to pause the execution of our script, thus displaying our image on our screen, until we press any 
# key on our keyboard.
# The only argument cv2.waitKey takes is an integer, which is a delay in milliseconds. If this value is positive, then 
# after the specified number of milliseconds elapses the window will close automatically. If the number of milliseconds 
# is zero, then the function will wait infinitely until a key is pressed.
# The return value of cv2.waitKey is either the code of the pressed key, or -1, indicating that no key was pressed 
# prior to the supplied amount of milliseconds elapsing.
cv2.waitKey(0)

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()


# Nota sobre slice
# ------------------------------------------
# a[inicio:final]           # desde el elemento 'inicio' hasta 'final'-1
# a[inicio:]                # desde el elemento 'inicio' hasta el final del array
# a[:final]                 # desde el primer elemento hasta elemento 'final'-1
# a[:]                      # todos los elementos del array
# a[inicio:final:salto]     # desde el elemento 'inicio' hasta 'final' pero saltando
#                           # el número de elementos indicado por 'salto'
# a[-1]                     # selecciona el último elemento del array
# a[-2:]                    # selecciona los dos últimos elementos del array
# a[:-2]                    # selecciona todos los elementos excepto los dos últimos