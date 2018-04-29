import cv2
import numpy
from matplotlib import pyplot as plt

import math
import numpy as np

alg_count = 4
def alg_simple_dev(img, column):
    return numpy.var(img[:, column])


def alg_float_avg_dev_with_filtered(img, img_hz_filtered, column):
    # ...
    return numpy.var(img[:, column] - img_hz_filtered[:, column])


def analyze_img(img):
    # print 'average lighting:', numpy.average(img)
    # cv2.blur(img, (5,5))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_grey = img[:, :, 2]
    skipped = 0
    kernel = numpy.ones([1, 81]) / 81
    img_hz_filtered = cv2.filter2D(img_grey, cv2.CV_32F, kernel, borderType=cv2.BORDER_REPLICATE)
    kernel = numpy.ones([81, 1]) / 81
    img_vert_filtered = cv2.filter2D(img_grey, cv2.CV_32F, kernel, borderType=cv2.BORDER_REPLICATE)
    kernel = numpy.ones([61, 61]) / 3721
    img_blurred = cv2.filter2D(img_grey, cv2.CV_32F, kernel, borderType=cv2.BORDER_REPLICATE)
    result_alg_simple_dev, result_alg_horiz_fil_dev, result_alg_vert_fil_dev, result_alg_gauss_fil_dev = \
        [], [], [], []
    for cut_loc in range(50, 500, 1):
        if np.average(img_grey[:, cut_loc]) > 130:
            skipped += 1
            continue
        result_alg_horiz_fil_dev.append(alg_float_avg_dev_with_filtered(img_grey, img_hz_filtered, cut_loc))
        result_alg_vert_fil_dev.append(alg_float_avg_dev_with_filtered(img_grey, img_vert_filtered, cut_loc))
        result_alg_gauss_fil_dev.append(alg_float_avg_dev_with_filtered(img_grey, img_blurred, cut_loc))
        result_alg_simple_dev.append(alg_simple_dev(img_grey, cut_loc))
    print  str(len(result_alg_gauss_fil_dev)), ' valid columns,', str(skipped), ' skipped.'
    result_alg_simple_dev_avg = np.average(np.array(result_alg_simple_dev))
    result_alg_horiz_fil_dev_avg = np.average(np.array(result_alg_horiz_fil_dev))
    result_alg_vert_fil_dev_avg = np.average(np.array(result_alg_vert_fil_dev))
    result_alg_gauss_fil_dev_avg = np.average(np.array(result_alg_gauss_fil_dev))

    to_return = [result_alg_simple_dev_avg, result_alg_vert_fil_dev_avg, result_alg_horiz_fil_dev_avg, result_alg_gauss_fil_dev_avg]
    return to_return

def analyze_file(filename):
    print 'analyze: ', filename
    result = analyze_img(cv2.imread(filename))
    print 'simple: ', result[0]
    print 'hori. filter: ', result[1]
    print 'vert. filter: ', result[2]
    print 'gauss filter: ', result[3]


class ClusterAnalyzer():
    count = 0

    def __init__(self, ra):
        self.results = [[], [], [], []]
        self.ra = ra
        self.count = ClusterAnalyzer.count
        self.remark = ''
        ClusterAnalyzer.count += 1

    def addremark(self, remark):
        self.remark = remark

    def addimg(self, filename):
        img = cv2.imread(filename)
        if img is None:
            print 'error when reading: ', filename
            return
        imgresult = analyze_img(img)
        print filename + '@Ra=' + self.ra + ' analysis: ' + str(imgresult)
        self.results[0].append(imgresult[0])
        self.results[1].append(imgresult[1])
        self.results[2].append(imgresult[2])
        self.results[3].append(imgresult[3])

    def __repr__(self):
        repr = str('\n' + 'count: ' + str(self.count) + '\n' +
            'simple: '+ str(self.results[0]) + '\n' +
            'hori. filter: '+ str(self.results[1]) + '\n' +
            'vert. filter: '+ str(self.results[2]) + '\n' +
            'gauss filter: '+ str(self.results[3]) + '\n')
        return repr

    def to_analysis(self):
        return (self.ra, self.results)



if __name__ == '__main__':
    clusters = []
    clusters[0] = ClusterAnalyzer(1)
    clusters[1] = ClusterAnalyzer(2)

'''
analyze_file('/home/wilhelm/RGB/A1.jpg')
analyze_file('/home/wilhelm/RGB/A2.jpg')
analyze_file('/home/wilhelm/RGB/A3.jpg')
analyze_file('/home/wilhelm/RGB/A4.jpg')
analyze_file('/home/wilhelm/RGB/A5.jpg')
analyze_file('/home/wilhelm/RGB/A6.jpg')

analyze_file('/home/wilhelm/RGB/B1.jpg')
analyze_file('/home/wilhelm/RGB/B2.jpg')
analyze_file('/home/wilhelm/RGB/B3.jpg')
analyze_file('/home/wilhelm/RGB/B4.jpg')
analyze_file('/home/wilhelm/RGB/B5.jpg')
analyze_file('/home/wilhelm/RGB/B6.jpg')

 #----
 
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

'''
