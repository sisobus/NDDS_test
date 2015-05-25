#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import random
from optparse import OptionParser
parser = OptionParser()

parser.add_option('-d', '--dim', default=10,\
    help='Number of dimensions', dest='dim')
parser.add_option('-n', '--data_size', default=100,\
    help='Number of data', dest='size')
(options, ags) = parser.parse_args(sys.argv[1:])

a = ['A','G','T','C']
dim = int(options.dim)
size = int(options.size)
for i in xrange(size):
    s = ""
    for j in xrange(dim):
        s += a[random.randrange(0,4)]
    print s
