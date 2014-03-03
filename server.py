#!/usr/bin/python

__author__ = 'Saurabh Bhatia'

# standard imports
import xmpp
from eventDispatcher import EventDispatcher
from messageEvents import MessageEvent
from Crypto.Cipher import DES

class User(object):
    """
    User object stores user credentials
    """
    def __init__(self):
        f = open('user_credentials.txt')
        lines = [line.strip() for line in f.readlines()]
        f.close()
        # get user and password hash
        self.user = lines[0].split(':')[1]
        self.passHash = lines[2].split(':')[1]
        self.pads = int(lines[1].split(':')[1])
    
    def getPass(self):
        '''
        Tally password against hash
        '''
        obj = DES.new('abcdefgh', DES.MODE_ECB)
        limit = -1 * self.pads
        return str(obj.decrypt(self.passHash)[:limit])
    
    def getUser(self):
        '''
        Return user name
        '''
        return self.user

class Server(object):
    """
    Main backend server...this keeps running
    """
    def __init__(self, eventDispatcher):
        # build a User object
        user = User()
        
        # setup catching of events
        self.eventDispatcher = eventDispatcher
        # Listen for the messageTyped event type
        self.eventDispatcher.add_event_listener(
            MessageEvent.messageTyped, self.sendMessage)
        
        # connect
        jid = xmpp.protocol.JID(user.getUser())
        self.connection = xmpp.Client(jid.getDomain(), debug=[]) # remove debug=[] to switch on debugging
        self.connection.connect() 
        # if login credentials are incorrect...fail immediately
        if not self.verifyAccess(jid, user):
            raise ValueError("Error could not authenticate")
        self.connection.RegisterHandler('message', self.messageHandler)
        self.connection.RegisterDisconnectHandler(self.disconnected)    
        self.connection.sendInitPresence(requestRoster=1)
        
        while self.connection.Process(1): 
            pass
        
    
    def messageHandler(self, connect_object, message_node):
        '''
        Receives any pings from other users
        '''
        sender = message_node.getFrom().getNode()
        body = message_node.getBody()
        if body != 'None':
            print("*****************************************************")
            print("FROM: %s" % str(sender))
            print("%s\n" % str(body))
        
    
    def disconnected(self):
        print("Seems we have lost connection...")
        
    def verifyAccess(self, jid, user):
        '''
        Tally credentials
        '''
        status = 'gHey!'
        result = self.connection.auth(jid.getNode(), user.getPass(), status)
        return result
        
    def sendMessage(self, event):
        '''
        Send a gTalk message to address specified by "to"
        '''
        # get to and msg
        data = event.data
        for to in data['to']:
            print('****')
            print(to)
            print(data['msg'])
            self.connection.send(xmpp.Message(to, data['msg']))

