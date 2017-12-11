import imageio
import imagehash
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import time
import progressbar
import numpy as np
from adjusted_rand_index import rand_index

def findMedians(a):
    return ''.join(sorted(d)[len(a)/2] for d in zip(*a))

def HashFiles():
    mypath = './Data/'
    hashpath = './DataHash/'
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    total = len(files)
    ext = '.txt'
    iter = 1
    with progressbar.ProgressBar(max_value=total) as progress:
        fhash = open(hashpath + 'hashes' + ext, "w")

        for file in files:
            hash = []
            filename, file_extension = os.path.splitext(file)
            reader = imageio.get_reader(mypath+file)
            for i, im in enumerate(reader):
                hash.append(str(imagehash.average_hash(Image.fromarray(im, 'RGB'))))

            singleHash =findMedians(hash)
            fhash.write('\n' + singleHash + ',' + filename)

            progress.update(iter)
            iter += 1

        fhash.close()

def loadHashes():

    fname = './DataHash/hashes.txt'
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def comparison(labels,names):
    k = len(set(labels))
    clusters = []

    for i in range(k):
        sets = [set() for _ in xrange(970)]
        for i in range(9700):
            sets[labels[i]].update([names[i]])
    print sets
    return rand_index(sets)



# what to do
recomputeHash = False # (2:56:47)
usePrecomputedHashes = True


start_time = time.time()
# Hash All Files
if recomputeHash:
    HashFiles()


if usePrecomputedHashes:
    data=loadHashes()
    data.pop(0)



d = np.empty((9700,8))
names = []
iter = 0
for str1 in data:
    i1,i2 = str1.split(',')
    numstr = '{0:08d}'.format(abs(hash(i1.split(',')[0])) % (10 ** 8))

    num = map(int,numstr)
    d[iter,:] = num
    iter+=1
    names.append(i2)


#d2 = {'Option{}Results'.format(i):[ random.randint(1,100) for _ in range(5)] for i in range(100)}

from sklearn.cluster import MiniBatchKMeans, KMeans

k_means = KMeans(init='k-means++', n_clusters=970, n_init=10).fit(d)

labels = k_means.labels_
TotalTime = time.time() - start_time # 0:48
print TotalTime
print '-------'
print comparison(labels,names)
print 'Elapsed Time: '
print (time.time() - start_time)


