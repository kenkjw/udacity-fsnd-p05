import random
import string

def token(n=32):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(n))
