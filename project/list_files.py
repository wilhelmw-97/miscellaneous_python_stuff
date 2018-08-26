import os
from cvtest2 import ClusterAnalyzer
import numpy as np
import matplotlib.pyplot as plt
import ImageFolder

i_to_color = ['red', 'blue', 'green', 'brown']
i_to_alg = ['simple var', 'vert gauss + var', 'horiz gauss + var', 'gauss + var']

def get_ImageFolder_list(mydir):
    os.chdir(mydir)
    if not mydir.endswith('/'):
        mydir += ('/')
    gen = os.walk('.')
    folders_list = gen.next()
    print folders_list
    ImF = []
    for fold in folders_list[1]:
        fold = mydir + fold
        ImF.append(ImageFolder.ImageFolder(fold))

    return ImF

def plot_ImageFolder_list(if_list, alg_num=0, median_only=False):
    x_holder = np.array([])
    y_holder = np.array([])
    if median_only:
        #for folder in if_list:
        #    new_x = np.array([folder.ra])
        #    x_holder = np.concatenate((x_holder, new_x))
        #    new_y = np.median(folder.data)
        pass
        #    y_holder = np.concatenate((y_holder,np.array([new_y])))
    else:
        for folder in if_list:
            new_x = np.array([folder.ra] * len(folder.data))
            x_holder = np.concatenate((x_holder, new_x))
            new_y = []
            for picturelist in folder.data:
                new_y.append(picturelist[alg_num])
            new_y = np.array(new_y)
            y_holder = np.concatenate((y_holder,new_y))

    return (x_holder, y_holder)




mydir = raw_input('dir?')
if mydir == '':
    mydir = '/home/wilhelm/rgb1'
dir_list = get_ImageFolder_list(mydir)
for i in dir_list:
    print i
    print ''
result = plot_ImageFolder_list(dir_list, alg_num=3, median_only=False)
plt.scatter(*result, c='red')
plt.show()