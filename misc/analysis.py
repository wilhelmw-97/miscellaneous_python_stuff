import numpy, cv2
import matplotlib.pyplot as plt

def processrow(rowinf):
    return numpy.var(rowinf)
a = cv2.imread('/home/wilhelm/Desktop/large.jpg'
               )

topleft = (5,0)
bottomright = (a.shape[0], a.shape[1])
cv2.namedWindow('image')
print 'img dem:', a.shape
cut_img = a[ topleft[0]:bottomright[0] , topleft[1]:bottomright[1] , : ]
print 'cut_img dem:', cut_img.shape
cut_img_hsv = cv2.cvtColor(cut_img, cv2.COLOR_BGR2HSV)
print 'cut_img_hsv dem:', cut_img_hsv.shape
cut_img_hsv_onlyv = cut_img_hsv[:,:,2]
cv2.imshow('image', cut_img_hsv_onlyv)
cv2.waitKey(0)
largestvariance = 0
largestvarianceindex = 0
for i in range(0, bottomright[0] - topleft[0]):

    variance = processrow( cut_img_hsv_onlyv[i, :].reshape( bottomright[1] - topleft[1] ))
    print 'row', i, ': ', variance

    if largestvariance < variance:
        largestvarianceindex = i
        largestvariance = variance

print 'largestvariance: ', largestvariance, 'at index: ', largestvarianceindex
#cv2.line(img,(0,0),(511,511),(255,0,0),5)

cv2.line(cut_img, (0, largestvarianceindex), ( bottomright[1] - topleft[1], largestvarianceindex), (255,0,0), 2)
cv2.imshow('image', cut_img)

x = numpy.arange(0, bottomright[1] - topleft[1], 1)

y = cut_img_hsv_onlyv[largestvarianceindex, :].reshape( bottomright[1] - topleft[1] )

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x,y)


cv2.waitKey(0)
plt.show()
cv2.waitKey(0)








