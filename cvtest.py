import cv2
import numpy
from matplotlib import pyplot as plt
i = 0
cam = cv2.VideoCapture()
cam.open(1)
fig = plt.figure()
while True:
    try:
        a, img = cam.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = img[:,:,2]
        img_grey = cv2.Laplacian(img, cv2.CV_64F)
        #img2 = cv2.Canny(img, 220, 400)
        cut_line = img_grey[:, img_grey.shape[1]/2]
        img =

    except KeyboardInterrupt:
        break


'''

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x,y)
'''