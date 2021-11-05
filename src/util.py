import os
import datetime


def page_cached(fn):
    if os.path.exists(fn):
        return os.stat(fn).st_size > 0
    return False

def get_dt(date_time):
    return datetime.datetime.strptime(date_time, "%Y-%m-%d %I:%M%p")

def get_curr_dt():
    curr = datetime.datetime.now()
    print("[-] Today's date {}".format(curr.strftime("%Y-%m-%d %I:%M%p")))
    return curr

def get_dt_string(dt):
    return dt.strftime("%Y-%m-%d %I:%M%p")

def check_caches(dn):
    pass