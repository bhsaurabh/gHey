# User facing application to send messages
__author__ = 'Saurabh Bhatia'

# import statements
import sys
import xmlrpclib

def main():
    if not len(sys.argv) > 1:
        print("Enter at-least one recipient")
        sys.exit(1)
    toList = sys.argv[1:]
    
    # get the RPC server
    s = xmlrpclib.ServerProxy('http://localhost:9000', allow_none=True)
    
    # get the message
    print('Type message, Hit Ctrl+D when done')
    try:
        msgText = ''.join(sys.stdin.readlines())
    except KeyboardInterrupt:
        print('\nMessage aborted...')
        sys.exit(1)
    else:
        print('\nAttempting to send message')
        s.send2server(toList, msgText)

if __name__ == '__main__':
    main()