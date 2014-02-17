# coding=utf-8
import os
import pickle
import sys
import time
from delete import delete_post
import facebook


prop_file = "login_prop"
running_on_heroku = False


def load_properties():
    if running_on_heroku:
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

    usr = saved_props['FB_USER']
    pwd = saved_props['FB_PWD']

    # ID of the FB group
    group_id = saved_props['group_id']

    graph = facebook.GraphAPI(sublets_oauth_access_token)

    obj = graph.put_object(group_id, "feed", message="test")
    postid = obj['id']
    url = "http://www.facebook.com/" + postid

    try:
        delete_post(usr, pwd, url, test)
    except Exception as e:
        print 'ERROR: ' + e.message
        print type(e)
        graph.delete_object(postid)
        print "Deleted manually"

    print "Confirming deletion..."
    time.sleep(2)
    try:
        print graph.get_object(id=postid)
    except:
        print "Deletion confirmed ✓"


if __name__ == "__main__":
    # Check to see if we're running on Heroku
    if os.environ.get('MEMCACHEDCLOUD_SERVERS', None):
        import bmemcached

        # Authenticate Memcached
        running_on_heroku = True
        mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').
                               split(','),
                               os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                               os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

    test()