import time
import hashlib
import hmac

def getSignature(urlAndtimestamp, secret):
    urlAndtimestamp = bytes(urlAndtimestamp, 'utf-8')
    secret = bytes(secret, 'utf-8')

    digester = hmac.new(secret, urlAndtimestamp, hashlib.sha1)
    signature = digester.hexdigest()
    return signature
