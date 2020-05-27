import xmlrpclib

__HOST = 'localhost'
__PORT = '8000'

s = xmlrpclib.ServerProxy('http://' + __HOST + ':' + __PORT)
# print s.pow(2, 3)
s.add(2, 3)
s.div(5, 2)

s.system.listMethods()