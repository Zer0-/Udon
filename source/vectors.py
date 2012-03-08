""" 2d vector library """

def add(a, b):
    """return a vector that is the sum of two vectors"""
    return [a[0] + b[0], a[1] + b[1]]

def subtract(a, b):
    """return a vector that is a subtract b"""
    return [a[0] - b[0], a[1] - b[1]]

def addref(a, b):
    """add vector b to vector a"""
    a[0] += b[0]
    a[1] += b[1]
    
def subtractref(a, b):
    """subtract b from a"""
    a[0] -= b[0]
    a[1] -= b[1]

def byscalar(c, v):
    return [v[0] * c, v[1]*c]

def byscalar_ref(c, v):
    v[0] = v[0] * c
    v[1] = v[1] * c    
