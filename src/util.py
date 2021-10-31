import os


def page_cached(fn):
    if os.path.exists(fn):
        return os.stat(fn).st_size > 0
    return False

def check_caches(dn):
    pass