import config

#To print only in debug mode, call dprint, and it either works like
#the python3.0 print function or it doesn't do anything
#This is to avoid writing conditionals for print statements
def _doprint(*toprint):
    s = ""
    for i in toprint:
        s = "%s %s" % (s, i)
    print s

def _dontprint(*toprint):
    pass

if config.DEBUG:
    dprint = _doprint
else:
    dprint = _dontprint

