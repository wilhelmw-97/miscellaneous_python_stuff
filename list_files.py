import os
import numpy as np
import cvtest2 as cvt
import json

def analyze_dir(dir):
    print 'analyze: ', dir
    ra = dir.split('/')[-1]
    if ra == '':
        ra = dir.split('/')[-2]

    ra = ra.split('_')[0]
    cluster = cvt.ClusterAnalyzer(ra)
    files = os.listdir(dir)
    os.chdir(dir)
    for m_file in files:
        if os.path.isfile(m_file):
            cluster.addimg(m_file)
            print 'adding: ', m_file, 'to Ra=', ra
    return cluster


a = os.listdir('/home/wilhelm/RGB')
dirs = []
# adds all dir in folder to dirs
for name in a:
    if os.path.isdir('/home/wilhelm/RGB/' + name):
        dirs.append('/home/wilhelm/RGB/' + name)
# analyze content of dirs and store in mydict
mydict = {}
for dir in dirs:
    result = analyze_dir(dir)
    mydict[result.ra] = result


algorithm_count = 4

#   sorted_infos structure:
#   [
#   four rows: four algorithms
#   columns = count(Ra):
#   [info for 0.1, 0.2, 0.4, 0.9]
#   [info for 0.1, 0.2, 0.4, 0.9]
#   [...]
#   []
#   ]

# analyze and chart results
sorted_Ra = mydict.keys.sorted()
sorted_infos = [None] * algorithm_count
for i in range(algorithm_count):
    sorted_infos[i] = [None] * len(sorted_Ra)
for key, item in mydict:
    for i in range(len(sorted_Ra)):
        if sorted_Ra[i] == key:
            pass




# generate two corresponding arrays: ra <-> values generated from each algorithm

print mydict



