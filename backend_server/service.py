import json
import pyjsonrpc
import os
import sys
import operations

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add is called with %d and %d" % (a, b)
        return a + b

    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" %(SERVER_HOST, SERVER_PORT)

http_server.serve_forever()