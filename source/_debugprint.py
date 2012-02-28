import config

#Were going to print to the console only if the DEBUG setting is on
#To do this we call dprint in our app, and it either works like
#the python3.0 print function or it doesn't do anything
#to avoid shitting in the command line.
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
