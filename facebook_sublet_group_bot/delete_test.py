# coding=utf-8
import os
import pickle
import sys
import time
import facebook

__author__ = 'Henri Sweers'


def load_properties():
    prop_file = "login_prop"
    if os.environ.get('MEMCACHEDCLOUD_SERVERS', None):
        import bmemcached
        mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').
                               split(','),
                               os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                               os.environ.get('MEMCACHEDCLOUD_PASSWORD'))
        obj = mc.get('props')
        if not obj:
            return {}
        else:
            return obj
    else:
        if os.path.isfile(prop_file):
            with open(prop_file, 'r+') as login_prop_file:
                data = pickle.load(login_prop_file)
                return data
        else:
            sys.exit("No prop file found")


def test():
    # Load the properties
    saved_props = load_properties()

    # Access token
    sublets_oauth_access_token = saved_props['sublets_oauth_access_token']

    # ID of the FB group
    group_id = saved_props['group_id']

    graph = facebook.GraphAPI(sublets_oauth_access_token)

    obj = graph.put_object(group_id, "feed", message="test")
    postid = obj['id']

    try:
        graph.delete_object(id=postid)
    except Exception as e:
        print 'ERROR: ' + e.message
        print type(e)
        print 'Failed to delete with GraphAPI'
        return False

    print "Confirming deletion..."
    time.sleep(2)
    try:
        print graph.get_object(id=postid)
        return False
    except:
        print "Deletion confirmed ✓"
        return True


if __name__ == "__main__":
    test()
