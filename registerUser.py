# This script build user_credentials.txt

__author__ = 'Saurabh Bhatia'


from Crypto.Cipher import DES
import base64
import os

def main():
    user = raw_input('Username: ') + "@gmail.com"
    encryptedPass, pads = encrypt(raw_input('Password: '))
    f = open('user_credentials.txt', 'w')
    f.write('user:%s\n' % user)
    f.write('pads:%d\n' % pads)
    f.write('pass:%s' % encryptedPass)
    
    
def encrypt(pwd):
    obj = DES.new('abcdefgh', DES.MODE_ECB)
    if len(pwd) % 8 != 0:
        # will have to pad to next multiple of 8
        newLen = ((len(pwd)/8) + 1) * 8
        pads = newLen - len(pwd)
        return (obj.encrypt(pwd + 'X'*pads), pads)
        
if __name__ == '__main__':
    main()