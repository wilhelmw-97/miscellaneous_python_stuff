import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = '/home/wilhelm/Downloads/10769932_223344208971_2.jpg'
mzimg = cv2.imread(image_path, flags=cv2.IMREAD_GRAYSCALE)
#mzimg = mzimg[1]
mzimg = cv2.threshold(mzimg, 200, 255, cv2.THRESH_BINARY)
mzimg = mzimg[1]
plt.imshow(mzimg, cmap='gray')
plt.show()

start_x = int(raw_input("enter starting x pixel"))
step_x = int(raw_input("enter second x"))
step_x = step_x - start_x
end_x = int(raw_input("enter ending x pixel"))
start_y = int(raw_input("enter starting y pixel"))
step_y = int(raw_input("enter second y"))
step_y = step_y - start_y
end_y = int(raw_input("enter ending y pixel"))

x_count = int((end_x - start_x)/step_x + 0.5)
y_count = int((end_y - start_y)/step_y + 0.5)
step_x = ((end_x - start_x)/x_count + 0)
step_x = ((end_x - start_x)/x_count + 0)

print 'real step x:', step_x
print 'real step y:', step_y
print 'real x count:', x_count
print 'real y count:', y_count
x_temp = start_x - step_x
y_temp = start_y - step_y
for ix in range(x_count):
    x_temp += step_x
    for iy in range(y_count):
        y_temp += step_y
        print 'drawing at: (', x_temp, ', ', y_temp, ')'
        cv2.circle(mzimg, (int(x_temp), int(y_temp)), 4, 160, thickness= 5)
    y_temp = start_y - step_y

plt.imshow(mzimg, cmap='gray')
plt.show()
choice = raw_input('accept? y/n')
if not (choice == 'Y' or choice == 'y'):
    print 'end'
    exit(0)

mzmat = mzimg[start_y:step_y:, start_x:step_x:]
print mzmat