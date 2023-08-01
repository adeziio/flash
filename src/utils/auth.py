import os


def checkAuth(key):
    if (key == os.getenv('FREEFLASH_API_KEY')):
        return True
    return False
