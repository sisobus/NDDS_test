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

class Int_Index:
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

    datas = get_data_in_file('data/data_100000_30_1_4.txt')

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
    '''
    vps.append( [ 'B' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'C' for i in xrange(NUMBER_OF_DIMENSION) ] )
    vps.append( [ 'D' for i in xrange(NUMBER_OF_DIMENSION) ] )
    for i in xrange(6):
        vps.append(generate_random_vp())
        '''

    datas = get_data_in_file('data/data_100000_30_1_4.txt')

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
        plt.title('cluster = 1')
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

def print_graph(image_name,xp,yp):
    plt.plot(xp,yp,lw=2)
    plt.xlim(0,31)
    #plt.show()
    plt.savefig(image_name,dpi=100)
    plt.clf()



def generate_regular_vp():
    vps = []
    n = NUMBER_OF_DIMENSION
    all_A = [ 'A' for i in xrange(NUMBER_OF_DIMENSION) ]
    all_B = [ 'B' for i in xrange(NUMBER_OF_DIMENSION) ]
    all_C = [ 'C' for i in xrange(NUMBER_OF_DIMENSION) ]
    all_D = [ 'D' for i in xrange(NUMBER_OF_DIMENSION) ]

    segments = []
    segments.append(all_A[:n/2])
    segments.append(all_A[:n/2])
    segments.append(all_B[:n/2])
    segments.append(all_B[:n/2])
    segments.append(all_C[:n/2])
    segments.append(all_C[:n/2])
    segments.append(all_D[:n/2])
    segments.append(all_D[:n/2])
    for i in xrange(len(segments)):
        for j in xrange(len(segments)):
            if i <> j:
                vps.append(segments[i]+segments[j])
    seven = []
    eight = []
    for i in xrange(len(segments)):
        seven.append(segments[i][:len(segments[i])/2])
        eight.append(segments[i][len(segments[i])/2:])
    for i in xrange(len(seven)):
        for j in xrange(len(eight)):
            for ii in xrange(len(seven)):
                for jj in xrange(len(eight)):
                    if i <> ii and j <> jj:
                        vps.append(seven[i]+eight[j]+seven[ii]+eight[jj])

    

    ret = []
    for i in xrange(len(vps)):
        isFind = False
        for j in xrange(len(ret)):
            if ret[j] == vps[i]:
                isFind = True
                break
        if isFind:
            continue
        ret.append(vps[i])
    return ret

def f(a):
    if a == 'A':
        return 0
    elif a == 'B':
        return 1
    elif a == 'C':
        return 2
    elif a == 'D':
        return 3

def rf(a):
    if a == 0:
        return 'A'
    elif a == 1:
        return 'B'
    elif a == 2:
        return 'C'
    elif a == 3:
        return 'D'

def test3():
#    vps = generate_regular_vp()
    vps = []
    datas = get_data_in_file('data/data_100000_30_1_4.txt')
    count = [ [ 0 for j in xrange(4) ] for i in xrange(NUMBER_OF_DIMENSION) ]
    for i in xrange(len(datas)):
        n = NUMBER_OF_DIMENSION
        for j in xrange(n):
            count[j][f(datas[i][j])] = count[j][f(datas[i][j])] + 1
    for i in xrange(4):
        for j in xrange(NUMBER_OF_DIMENSION):
            print count[j][i],
        print ''
    major = []
    minor = []
    second = []
    third  = []
    for i in xrange(NUMBER_OF_DIMENSION):
        mx = 0
        mx_idx = 0
        mn = 987654321
        mn_idx = 0
        tmp = []
        for j in xrange(4):
            if mx < count[i][j]:
                mx = count[i][j]
                mx_idx = j
            if mn > count[i][j]:
                mn = count[i][j]
                mn_idx = j
        for j in xrange(4):
            if not ((mx == count[i][j] and mx_idx == j) or (mn == count[i][j] and mn_idx == j)):
                tmp.append(j)
        if count[i][tmp[0]] < count[i][tmp[1]]:
            tt = tmp[0]
            tmp[0] = tmp[1]
            tmp[1] = tt
        major.append(rf(mx_idx))
        minor.append(rf(mn_idx))
        second.append(rf(tmp[0]))
        third.append(rf(tmp[1]))
    print major
    print minor
    print second
    print third
    vps.append(major)
    vps.append(minor)
    vps.append(second)
    vps.append(third)
    vps.append(major[:len(major)/2]+minor[len(minor)/2:])
    vps.append(minor[:len(minor)/2]+major[len(major)/2:])



    print len(vps)
    ans = []
    i = 0
    for vp in vps:
        n = len(datas)
        x = [ [] for j in xrange(31) ]
        for j in xrange(n):
            next_position = hamming_distance(vp,datas[j])
            x[next_position].append(j)
        mx = 0
        for j in xrange(31):
            if mx < len(x[j]):
                mx = len(x[j])
        ans.append(Int_Index(mx,i))
        print i
        i = i + 1
    ans.sort()
    for i in xrange(6):
        vp_idx = ans[i].id
        cur_vp = vps[vp_idx]
        x = [ [] for j in xrange(31) ]
        n = len(datas)
        for j in xrange(n):
            next_position = hamming_distance(cur_vp,datas[j])
            x[next_position].append(j)
        xp = []
        yp = []
        for j in xrange(31):
            xp.append(j)
            yp.append(len(x[j]))
        print cur_vp
        print yp
        print_graph('figure/%d.png'%i,xp,yp)



if __name__ == '__main__':
    #test1()
    #test2()
    test3()
