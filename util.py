import os


def checkAuth(key):
    if (key == os.getenv('FREEFLASH_API_KEY')):
        return True
    return False


def convert_bytes(bytes_number):
    tags = ["Byte", "KB", "MB", "GB", "TB"]

    i = 0
    double_bytes = bytes_number

    while (i < len(tags) and bytes_number >= 1024):
        double_bytes = bytes_number / 1024.0
        i = i + 1
        bytes_number = bytes_number / 1024

    return str(round(double_bytes, 2)) + " " + tags[i]
