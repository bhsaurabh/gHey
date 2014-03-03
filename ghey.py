# application to send gtalk pings
__author__ = 'Saurabh Bhatia'

import server
from eventDispatcher import EventDispatcher
from messageEvents import MessageEvent

class App(object):
    """
    Application entry point
    """
    def __init__(self):
        # setup catching of events
        self.eventDispatcher = EventDispatcher()
        # setup backend server
        self.server = server.Server(self.eventDispatcher)
        
        
    def listenChat(self):
        # create a simple XML-RPC server
        from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
        
        class RequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ('/RPC2')
        
        # create a server
        rpcserver = SimpleXMLRPCServer(('localhost', 9000), requestHandler=RequestHandler, allow_none=True)
        rpcserver.register_multicall_functions()
        rpcserver.register_introspection_functions()
        
        def sendToServer(toList, msg):
            self.eventDispatcher.dispatch_event(MessageEvent(MessageEvent.messageTyped, {'to':toList, 'msg':msg}))
        
        # register method to send to Base_Server
        rpcserver.register_function(sendToServer, 'send2server')
        
        # Run the RPC server main loop
        rpcserver.serve_forever()
        
        
if __name__ == '__main__':
    gheyApp = App()
    gheyApp.listenChat()