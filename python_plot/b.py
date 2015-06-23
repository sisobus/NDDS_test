#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import sys
import math
import glob
import random
import matplotlib.pyplot as plt
import string
import commands

class IntIndex:
    def __init__(self):
        self.x = 0
        self.id = 0
    def __init__(self,x,id):
        self.x = x
        self.id = id
    def __lt__(self,other):
        if self.x == other.x:
            return self.id < other.id
        return self.x < other.x

def hammingDistance(a,b):
    n = len(a)
    if n <> len(b):
        print 'calculate hamming distance error:length <>'
        exit(-1)
    ret = 0
    for i in xrange(n):
        if a[i] <> b[i]:
            ret = ret + 1
    return ret

def generateUniformRandomVP(numberOfDimension,numberOfAlphabet):
    ret = []
    alphabet = list(string.ascii_uppercase)
    for i in xrange(numberOfDimension):
        cur = random.randrange(0,numberOfAlphabet)
        ret.append(alphabet[cur])
    return ret

def getDataInFile(filename):
    onlyFileName = filename.split('.')[0]
    numberOfDataSize  = int(onlyFileName.split('_')[1])
    numberOfDimension = int(onlyFileName.split('_')[2])
    numberOfAlphabet  = int(onlyFileName.split('_')[4])

    ret = []
    with open(filename,'r') as fp:
        r = fp.read().rstrip().split('\n')
    for i in xrange(1,numberOfDataSize+1):
        t = r[i].split(':')[1].split(',')
        ret.append(t)
    return ret

def saveGraph(imageFileName,xp,yp):
    plt.plot(xp,yp,lw=2)
    plt.xlim(0,len(xp)+1)
    plt.savefig(imageFileName,dpi=100)
    plt.clf()

def f(a):
    alphabet = list(string.ascii_uppercase)
    for i in xrange(len(alphabet)):
        if a == alphabet[i]:
            return i
    return -1

def rf(a):
    a = int(a)
    alphabet = list(string.ascii_uppercase)
    return alphabet[a]

def createDirectory(directoryName):
    if not os.path.exists(directoryName):
        command = 'mkdir %s'%directoryName
        ret = commands.getoutput(command)


def test1():
    filenames = glob.glob('data/*.txt')
    createDirectory('vp')
    createDirectory('d1')
    createDirectory('figure')

    for filename in filenames:
        print filename
        onlyFileName = filename.split('/')[1].split('.')[0]
        numberOfDataSize  = int(onlyFileName.split('_')[1])
        numberOfDimension = int(onlyFileName.split('_')[2])
        numberOfAlphabet  = int(onlyFileName.split('_')[4])
        typeOfData        = str(onlyFileName.split('_')[3])
        datas = getDataInFile(filename)

        alphabet = list(string.ascii_uppercase)
        vps = []

        # vp = AAAAAAA...AAA
        all_A = []
        for i in xrange(numberOfDimension):
            all_A.append(alphabet[0])
    
        # vp = data freq major 
        major = []
        majorVPFileName = 'vp/vp_%d_%d_%s_%d_1.out'%(numberOfDataSize,numberOfDimension,typeOfData,numberOfAlphabet)
        if os.path.exists(majorVPFileName):
            with open(majorVPFileName,'r') as fp:
                major = fp.read().rstrip().split(' ')
        else:
            count = [ [ 0 for j in xrange(numberOfAlphabet) ] for i in xrange(numberOfDimension) ]
            for i in xrange(len(datas)):
                for j in xrange(numberOfDimension):
                    count[j][f(datas[i][j])] = count[j][f(datas[i][j])] + 1
            for i in xrange(numberOfDimension):
                mx, mx_idx = (0,0)
                for j in xrange(numberOfAlphabet):
                    if mx < count[i][j]:
                        mx = count[i][j]
                        mx_idx = j
                major.append(rf(mx_idx))
            with open(majorVPFileName,'w') as fp:
                for i in xrange(len(major)):
                    fp.write(str(major[i])+' ')

        # vp = ABABABACABA...
        random_1 = generateUniformRandomVP(numberOfDimension,numberOfAlphabet)

        # vp = AABBCCDDAABBAA... 
        random_2 = []
        for i in xrange(int(numberOfDimension/2)+1):
            cur = random.randrange(0,numberOfAlphabet)
            for j in xrange(2):
                random_2.append(alphabet[cur])
        random_2 = random_2[:numberOfDimension]

        # vp = AAAABBBBAAAACCCCBBBB...
        random_4 = []
        for i in xrange(int(numberOfDimension/4)+1):
            cur = random.randrange(0,numberOfAlphabet)
            for j in xrange(4):
                random_4.append(alphabet[cur])
        random_4 = random_4[:numberOfDimension]

        
        vps.append(all_A)
        vps.append(major)
        vps.append(random_1)
        vps.append(random_2)
        vps.append(random_4)

        VPTypeName = [ 'A','M','R1','R2','R4' ]
        for i in xrange(len(vps)):
            xp = []
            yp = []
            yFileName = 'd1/yp_%d_%d_%s_%d_%s.out'%(numberOfDataSize,numberOfDimension,typeOfData,numberOfAlphabet,VPTypeName[i])
            if os.path.exists(yFileName):
                with open(yFileName,'r') as fp:
                    yp = fp.read().rstrip().split(' ')
                xp = [ j for j in xrange(numberOfDimension+1) ]
            else :
                x = [ [] for j in xrange(numberOfDimension+1) ]
                for j in xrange(numberOfDataSize):
                    nextPosition = hammingDistance(vps[i],datas[j])
                    x[nextPosition].append(j)
                for j in xrange(numberOfDimension+1):
                    xp.append(j)
                    yp.append(len(x[j]))
                with open(yFileName,'w') as fp:
                    for j in xrange(len(yp)):
                        fp.write(str(yp[j])+' ')

            imageFileName = 'figure/figure_%d_%d_%s_%d_%s.png'%(numberOfDataSize,numberOfDimension,typeOfData,numberOfAlphabet,VPTypeName[i])
            if not os.path.exists(imageFileName):
                saveGraph(imageFileName,xp,yp)

def vpCorrelationTest(vps,filename):
    onlyFileName = filename.split('/')[1].split('.')[0]
    numberOfDataSize  = int(onlyFileName.split('_')[1])
    numberOfDimension = int(onlyFileName.split('_')[2])
    numberOfAlphabet  = int(onlyFileName.split('_')[4])
    typeOfData        = str(onlyFileName.split('_')[3])
    datas = getDataInFile(filename)

    alphabet = list(string.ascii_uppercase)

    vpTotalDistance = 0
    for i in xrange(len(vps)):
        for j in xrange(len(vps)):
            if i == j:
                continue
            dist = hammingDistance(vps[i],vps[j])
            vpTotalDistance = vpTotalDistance + dist

    curDatas = datas
    for i in xrange(len(vps)):
        n = len(curDatas)
        x = [ [] for j in xrange(numberOfDimension+1) ]
        for j in xrange(n):
            nextPosition = hammingDistance(vps[i],curDatas[j])
            x[nextPosition].append(j)
        (mx, position) = (0,0)
        xp = []
        yp = []
        for j in xrange(numberOfDimension+1):
            xp.append(j)
            yp.append(len(x[j]))
            if mx < len(x[j]):
                (mx, position) = (len(x[j]),j)
        createDirectory('vpCorrelationTest')
        imageFileName = 'vpCorrelationTest/figure_%d_%d_%d_%s_%d_%d.png'%(vpTotalDistance,numberOfDataSize,numberOfDimension,typeOfData,numberOfAlphabet,i)
        if not os.path.exists(imageFileName):
            saveGraph(imageFileName,xp,yp)

        curDatas = []
        for dataId in x[position]:
            curDatas.append(datas[dataId])

def test2():
    alphabet = list(string.ascii_uppercase)
    filenames = glob.glob('data/*.txt')

    for filename in filenames:
        print filename
        onlyFileName = filename.split('/')[1].split('.')[0]
        numberOfDataSize  = int(onlyFileName.split('_')[1])
        numberOfDimension = int(onlyFileName.split('_')[2])
        numberOfAlphabet  = int(onlyFileName.split('_')[4])
        typeOfData        = str(onlyFileName.split('_')[3])

        vps = []
        vps.append( [ alphabet[0] for i in xrange(numberOfDimension) ] )
        vps.append( [ alphabet[1] for i in xrange(numberOfDimension) ] )
        vps.append( [ alphabet[2] for i in xrange(numberOfDimension) ] )
        vps.append( [ alphabet[3] for i in xrange(numberOfDimension) ] )

        vpCorrelationTest(vps,filename)

        vps = []
        vps.append( [ alphabet[0] for i in xrange(numberOfDimension) ] )
        vps.append( [ alphabet[1] for i in xrange(numberOfDimension) ] )
        ab = vps[0][:numberOfDimension/2]+vps[1][numberOfDimension/2:]
        ba = vps[1][:numberOfDimension/2]+vps[0][numberOfDimension/2:]
        vps.append(ab)
        vps.append(ba)

        vpCorrelationTest(vps,filename)


if __name__ == '__main__':
    #test1()
    test2()
