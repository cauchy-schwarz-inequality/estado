from hashlib import sha1
from random import randint
from time import time


def slug_hash():
    """ A utility function to obtain unique-ish names 
    """
    m = sha1()

    now = time()
    current_time_bytes = int(now).to_bytes(5, byteorder="big")
    m.update(current_time_bytes)

    digest = m.hexdigest()[:7]

    random_first = randint(0,100)
    random_second = randint(0,100)
    
    return f"{digest}-{random_first}-{random_second}"


    
