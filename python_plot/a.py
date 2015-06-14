#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import sys
import math
import random
import matplotlib.pyplot as plt

NUMBER_OF_ALPHABET  = 4
NUMBER_OF_DIMENSION = 30
gene = ['A','B','C','D']

def hamming_distance(a,b):
    n = len(a)
    if n <> len(b):
        print 'calculate hamming distance error:length <>'
        exit(-1)
    ret = 0
    for i in xrange(n):
        if a[i] <> b[i]:
            ret = ret + 1
    return ret

def generate_random_vp():
    ret = []
    for i in xrange(NUMBER_OF_DIMENSION):
        now = random.randrange(0,4)
        ret.append(gene[now])
    return ret

def get_data_in_file(filename):
    ret = []
    with open(filename,'r') as fp:
        r = fp.read().rstrip().split('\n')
    for i in xrange(1,100001):
        t = r[i].split(':')[1].split(',')
        ret.append(t)
    return ret

def test1():
    vps = []
    vps.append( [ 'A' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'B' for i in xrange(NUMBER_OF_DIMENSION) ] ) 
    vps.append( [ 'C' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'D' for i in xrange(NUMBER_OF_DIMENSION) ] )
    for i in xrange(6):
        vps.append(generate_random_vp())

    datas = get_data_in_file('data/data_100000_30_10.txt')

    for vp in vps:
        i = 0
        for data in datas:
            if i == 30:
                break
            print hamming_distance(vp,data),
            i = i + 1
        print ''

def test2():
    vps = []
    vps.append( [ 'A' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'B' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'C' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'D' for i in xrange(NUMBER_OF_DIMENSION) ] )
    for i in xrange(6):
        vps.append(generate_random_vp())

    datas = get_data_in_file('data/data_100000_30_10.txt')

    cur_datas = datas
    vp_number = 0
    for vp in vps:
        n = len(cur_datas)
        x = [ [] for i in xrange(31) ]
        for i in xrange(n):
            next_position = hamming_distance(vp,cur_datas[i])
            x[next_position].append(i)
        (mx, position) = (0,0)

        xp = []
        yp = []

        for i in xrange(31):
            xp.append(i)
            yp.append(len(x[i]))
            if mx < len(x[i]):
                (mx, position) = (len(x[i]),i)
        plt.title('cluster = 10')
        plt.xlabel('vp['+str(vp_number)+']\' x')
        plt.ylabel('number of data')
        plt.plot(xp,yp,lw=2)
        plt.xlim(0,31)
        plt.show()

        cur_datas = []
        for data_id in x[position]:
            cur_datas.append(datas[data_id])
        print len(cur_datas)
        vp_number = vp_number + 1



if __name__ == '__main__':
    #test1()
    test2()
