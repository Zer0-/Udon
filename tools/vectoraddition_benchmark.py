#performance testing for 2dimentional vector addition
from timeit import Timer
from random import random
from numpy import array as v

class V2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v1, v2):
        return V2(v1.x + v2.x, v1.y + v2.y)

m = 1000000 # one million

def reference():
    a = random()
    b = random()
    for i in range(m):
        a + b

def addnaive(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def addnaivetuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def nocopyadd(a, b):
    a[0] += b[0]
    a[1] += b[1]

def addmap(a, b):
    return map(sum, zip(a,b))

def addzip(a, b):
    m = [a[0], a[1]]
    for i, bi in enumerate(b): m[i] += bi
    return m

def t1():
    a, b = gen()
    a = v(a)
    b = v(b)
    for i in range(m):
        a + b

def t2():
    a, b = gen()
    for i in range(m):
        addnaive(a, b)

def t3():
    a, b = gen()
    for i in range(m):
        addmap(a, b)

def t4():
    a, b = gen()
    for i in range(m):
        addzip(a, b)

def t5():
    a = V2(random(), random())
    b = V2(random(), random())
    for i in range(m):
        a.add(a, b)

def t6():
    a, b = gen()
    for i in range(m):
        nocopyadd(a, b)

def t7():
    a, b = gentuple()
    for i in range(m):
        addnaivetuple(a, b)    

def gen():
    a = [random(), random()]
    b = [random(), random()]
    return a, b

def gentuple():
    a = (random(), random())
    b = (random(), random())
    return a, b

def time(s):
    t = Timer(s)
    print s, t.timeit(number=1)

time(reference) # only numbers
time(t1)# numpy
time(t2)# [a[0] + b[0], a[1] + b[1]] - naive method
time(t3)# using map and zip
time(t4)# using zip
time(t5)# using a class representation of a vector
time(t6)# naive add but modifies original vector
time(t7)# naive add but using tuples
