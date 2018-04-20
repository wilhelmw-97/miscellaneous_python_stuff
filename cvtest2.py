import cv2
import numpy
from matplotlib import pyplot as plt

import math

def alg_simple_dev()

def find_lighting_dev(img):
    #print 'average lighting:', numpy.average(img)
    # cv2.blur(img, (5,5))
    iii = 0
    lighting_dev_sum = 0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_grey = img[:, :, 2]

    kernel = numpy.ones([1, 81] )  / 81
    #print kernel.shape
    img_filtered = cv2.filter2D(img_grey, cv2.CV_32F, kernel, borderType=cv2.BORDER_REPLICATE)





    for cut_loc in range(100, 500, 2):
        lighting_dev = 0

        line_cut = img_grey[:, cut_loc].copy()
        line_filtered = img_filtered[:, cut_loc]
        #xs = numpy.arange(0, img_grey.shape[0], 1)
        #plt.plot(xs, line_cut, xs, line_filtered)  # plot image line
        #plt.show()

        #img_grey[:, int(img_grey.shape[1]/2)] = 0
        total_avg = numpy.average(line_cut)
        if total_avg > 110: continue
        else:

        #    print total_avg
            iii = iii + 1
        total_avg_arr = numpy.zeros(line_cut.shape)
        total_avg_arr.fill(total_avg)

        for i in numpy.nditer(line_cut):
            lighting_dev = numpy.var(line_cut-line_filtered)

            #if i > total_avg:
            #    lighting_dev = lighting_dev + i - total_avg
            #elif i < total_avg:
            #    lighting_dev = lighting_dev + total_avg - i

        lighting_dev_sum = lighting_dev_sum + lighting_dev
    return lighting_dev_sum / iii





print 'a1= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/A1.jpg') )
print 'a2= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/A2.jpg') )
print 'a3= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/A3.jpg') )
print 'a4= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/A4.jpg') )
print 'a5= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/A5.jpg') )
print 'a6= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/A6.jpg') )
print
print 'b1= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/B1.jpg') )
print 'b2= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/B2.jpg') )
print 'b3= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/B3.jpg') )
print 'b4= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/B4.jpg') )
print 'b5= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/B5.jpg') )
print 'b6= ', find_lighting_dev( cv2.imread('/home/wilhelm/RGB/B6.jpg') )


