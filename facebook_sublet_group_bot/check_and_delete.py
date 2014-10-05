#!/usr/bin/env python
# coding=utf-8

import os
import cPickle as pickle
import datetime
import facepy
import getopt
import time
import sys
import re
from util import log, Color, notify_mac

__author__ = 'Henri Sweers'

############## Global vars ##############

# 24 hours, in seconds
time_limit = 86400

# Pickle cache file caching warned posts
warned_db = "fb_subs_cache"

# Pickle cache file caching valid posts
valid_db = "fb_subs_valid_cache"

# Pickle cache file for properties
prop_file = "login_prop"

# Boolean for key extensions
extend_key = False

# Dry run to disable deletions on a run
dry_run = False

# Boolean for checking heroku
running_on_heroku = False

# Tags: allowed leading characters
allowed_leading_characters = ('*', '-')

# Tags: allowed tags
allowed_tags = {'looking', 'offering', 'parking', 'rooming'}


# Junk method that I use for testing stuff periodically
def test():
    log('Test', Color.PURPLE)


# Use this method to set new vals for props, such as on your first run
def set_new_props():
    saved_dict = load_properties()

    ###############################################################
    #### Uncomment lines below as needed to manually set stuff ####
    ###############################################################

    ###########################
    #### These are strings ####
    ###########################

    # saved_dict['sublets_oauth_access_token'] = "put-auth-token-here"
    # saved_dict['sublets_api_id'] = "put-app-id-here"
    # saved_dict['sublets_secret_key'] = "put-secret-key-here"
    # saved_dict['access_token_expiration'] = "put-access-token-expiration-here"
    # saved_dict['group_id'] = "put-group-id-here"

    ################################################################
    #### If you want post deletion, must be done outside of API ####
    ################################################################

    # saved_dict['FB_USER'] = "put-facebook-username-here"
    # saved_dict['FB_PWD'] = "put-facebook-password-here"


    ########################
    #### These are ints ####
    ########################

    # saved_dict['bot_id'] = put-bot-id-here
    # saved_dict['ignored_post_ids'].append(<id_num>)
    # saved_dict['ignore_source_ids'].append(<id_num>)
    # saved_dict['admin_ids'].append(<id_num>)

    #################################################################
    #### You can do other stuff too, the above are just examples ####
    #################################################################

    save_properties(saved_dict)


# Method for initializing your prop values
def init_props():
    test_dict = {'sublets_oauth_access_token': "put-auth-token-here",
                 'sublets_api_id': "put-app-id-here",
                 'sublets_secret_key': "put-secret-key-here",
                 'access_token_expiration': "put-access-token-expiration-here",
                 'group_id': 'put-group-id-here',
                 'FB_USER': "put-facebook-username-here",
                 'FB_PWD': "put-facebook-password-here",
                 'bot_id': -1,
                 'ignored_post_ids': [],
                 'ignore_source_ids': [],
                 'admin_ids': []}
    save_properties(test_dict)
    saved_dict = load_properties()
    assert test_dict == saved_dict


def save_properties(data):
    """
    Save props data into either memcache (heroku only) or pickle to local file
    :param data: Dictionary of props data
    """
    if running_on_heroku:
        mc.set('props', data)
    else:
        with open(prop_file, 'w+') as login_prop_file:
            pickle.dump(data, login_prop_file)


def load_properties():
    """
    Load properties data from either memcache (heroku only) or local pickled file

    :rtype : dict
    :return: Dictionary of all the properties
    """
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


# Method for loading a cache. Either returns cached values or original data
def load_cache(cachename, data):
    if running_on_heroku:
        if running_on_heroku:
            obj = mc.get(cachename)
            if not obj:
                return data
            else:
                return obj
    else:
        if os.path.isfile(cachename):
            with open(cachename, 'r+') as f:

                # If the file isn't at its end or empty
                if f.tell() != os.fstat(f.fileno()).st_size:
                    return pickle.load(f)
        else:
            log("--No cache file found, a new one will be created", Color.BLUE)
            return data


# Method for saving to cache
def save_cache(cachename, data):
    if running_on_heroku:
        mc.set(cachename, data)
    else:
        with open(cachename, 'w+') as f:
            pickle.dump(data, f)


# Manually update API token
def update_token(token):
    log("Updating token", Color.BLUE)
    graph = facepy.GraphAPI(token)
    try:
        graph.get('me/posts')
        props_dict = load_properties()
        props_dict['sublets_oauth_access_token'] = token
        props_dict['access_token_expiration'] = time.time() + 7200  # 2 hours buffer
        save_properties(props_dict)
        log("Token updated, you should now extend it", Color.BLUE)
    except Exception as e:
        log("API error - " + e.message, Color.RED)


# Set a property by name
def update_prop(prop_name, value):
    if prop_name in ("sublets_oauth_access_token", "access_token_expiration"):
        log("Please use -u or -e to update or extend tokens", Color.RED)
        return
    log("Setting \"" + prop_name + "\" to \"" + value + "\"", Color.BLUE)
    props_dict = load_properties()
    if prop_name not in props_dict.keys():
        input_response = raw_input("This key doesn't exist, do you want to add it? Y/N")
        if input_response.lower() != "y":
            return
    props_dict[prop_name] = value
    save_properties(props_dict)
    log("Done setting \"" + prop_name + "\"", Color.BLUE)


# Method for checking tag validity
def get_tags_old(message_text):
    p = re.compile(
        "^(-|\*| )*([\(\[\{])((looking)|(rooming)|(offering)|(parking))([\)\]\}])(:)?(\s|$)",
        re.IGNORECASE)

    split = message_text.strip().split(" ")

    # Check that they're on the first line
    if not p.match(split[0]) and split[0] not in allowed_leading_characters:
        return None

    tags_list = [l.lower()[1:-1] for l in split for m in (p.search(l),) if m]
    if len(tags_list) > 0:
        return tags_list
    else:
        return None


# Method for checking tag validity
def get_tags(message_text):
    p = re.compile(
        r"^(-|\*| )*(([\(\[\{])(.+)([\)\]\}]))+(:)?(\s|$)",
        re.IGNORECASE)

    # Insert space between two consecutive tags
    message_text = re.sub(r"([\)\]\}])([\(\[\{])", r"\1 \2", message_text)
    firstline_split = message_text.split("\n")[0].strip().split()

    # Check that they're on the first line
    if not p.match(firstline_split[0]) and firstline_split[0] not in allowed_leading_characters:
        return None

    tags_list = [re.sub(r"^(-|\*| )*", "", full_tag.lower())[1:(-2 if full_tag[-1] == ":" else -1)] for full_tag in
                 firstline_split for matched in (p.search(full_tag),) if matched]

    # Should really learn how to do python's builtin logging...
    # log('--Tags: ' + ', '.join(tags_list), Color.BLUE)

    if len(tags_list) > 0 and set(tags_list).issubset(allowed_tags):
        return tags_list
    else:
        return None


# Can't have "rooming" AND "offering". These people are usually just misusing the rooming tag
def validate_tags(tags):
    if not tags:
        return False
    elif "rooming" in tags and "offering" in tags:
        return False
    else:
        return True


# Method for checking if pricing reference is there
def check_price_validity(message_text):
    p = re.compile(
        "(\$)|((\d)+( )?((per)|(/)|(a))( )?(/)?((month)|(mon)|(mo))(\s)?)",
        re.IGNORECASE)

    if re.search(p, message_text) is not None:
        return True
    else:
        return False


# Checking if there's a parking tag
def check_for_parking_tag(message_text):
    p = re.compile(
        "^(-|\*| )*([\(\[\{])(parking)([\)\]\}])(:)?(\s|$)",
        re.IGNORECASE)

    if re.search(p, message_text):
        return True
    else:
        return False


# Method for extending access token
def extend_access_token(saved_props, token, sublets_api_id,
                        sublets_secret_key):
    log("Extending access token", Color.BOLD)
    access_token, expires_at = facepy.get_extended_access_token(
        token,
        sublets_api_id,
        sublets_secret_key
    )
    new_token = access_token
    unixtime = time.mktime(expires_at.timetuple())
    print time.mktime(expires_at.timetuple())
    saved_props['sublets_oauth_access_token'] = new_token
    saved_props['access_token_expiration'] = unixtime
    log("Token extended", Color.BOLD)


# Method for retrieving user ID's of admins in group, ignoring bot ID
def retrieve_admin_ids(group_id, auth_token):
    # Retrieve the uids via FQL query
    graph = facepy.GraphAPI(auth_token)
    admins_query = \
        "SELECT uid FROM group_member WHERE gid=" + group_id + " AND" + \
        " administrator"
    admins = graph.fql(query=admins_query)

    # Parse out the uids from the response
    admins_list = [admin['uid'] for admin in admins]

    # Update the admin_ids in our properties
    saved_props = load_properties()
    saved_props['admin_ids'] = admins_list
    save_properties(saved_props)

    return admins_list


# Delete posts older than 30 days old
def delete_old_posts(graph, group_id, admin_ids):
    old_date = int(time.time()) - 2592000  # 30 days in seconds
    old_query = "SELECT post_id, message, actor_id FROM stream WHERE " + \
                "source_id=" + group_id + " AND created_time<" + str(old_date) + \
                " LIMIT 300"
    log("Getting posts older than:")
    log("\t" + datetime.datetime.fromtimestamp(old_date)
        .strftime('%Y-%m-%d %H:%M:%S'))
    posts = graph.fql(query=old_query)
    deleted_posts_count = 0
    for post in posts["data"]:
        post_id = post['post_id']
        actor_id = post['actor_id']
        if int(actor_id) in admin_ids:
            # log('\n--Ignored post: ' + post_id, Color.BLUE)
            continue
        print post_id
        graph.delete(post_id)
        deleted_posts_count += 1
    log("Deleted " + str(deleted_posts_count) + " old posts", Color.RED)


# Main runner method
def sub_group():
    # Load the properties
    saved_props = load_properties()

    # Access token
    sublets_oauth_access_token = saved_props['sublets_oauth_access_token']

    # Access token expiration
    access_token_expiration = saved_props['access_token_expiration']

    # API App ID
    sublets_api_id = saved_props['sublets_api_id']

    # API App secret key
    sublets_secret_key = saved_props['sublets_secret_key']

    # ID of the FB group
    group_id = saved_props['group_id']

    # IDs of admins (unused right now, might remove later)
    admin_ids = saved_props['admin_ids']

    # FQL query for the group
    group_query = "SELECT post_id, message, actor_id FROM stream WHERE " + \
                  "source_id=" + group_id + " LIMIT 50"

    # Get current time
    now_time = time.time()

    # For logging purposes
    log("CURRENT CST TIMESTAMP: " + datetime.datetime.fromtimestamp(
        now_time - 21600).strftime('%Y-%m-%d %H:%M:%S'), Color.UNDERLINE)

    # Make sure the access token is still valid
    if access_token_expiration < now_time:
        sys.exit("API Token is expired")

    # Warn if the token's expiring soon
    if access_token_expiration - now_time < 604800:
        log("Warning - access token expires in less than a week", Color.RED)
        log("-- Expires on " + datetime.datetime.fromtimestamp(
            access_token_expiration).strftime('%Y-%m-%d %H:%M:%S'))

        # If you want it to automatically when it's close to exp.
        global extend_key
        extend_key = True

    # Extend the access token, default is ~2 months from current date
    if extend_key:
        extend_access_token(saved_props, sublets_oauth_access_token, sublets_api_id,
                            sublets_secret_key)

    # Log in, try to get posts
    graph = facepy.GraphAPI(sublets_oauth_access_token)

    # Make our first request, get the group posts
    group_posts = graph.fql(query=group_query)

    # Load the pickled cache of valid posts
    valid_posts = []
    log("Checking valid cache.", Color.BOLD)
    valid_posts = load_cache(valid_db, valid_posts)
    log('--Valid cache size: ' + str(len(valid_posts)), Color.BOLD)
    invalid_count = 0

    # Loop over retrieved posts
    for post in group_posts["data"]:

        # Important data received
        post_message = post['message']  # Content of the post
        post_id = post['post_id']  # Unique ID of the post

        # Unique ID of the person that posted it
        actor_id = post['actor_id']

        # Ignore mods and certain posts
        if int(actor_id) in admin_ids:
            log('\n--Ignored post: ' + post_id, Color.BLUE)
            continue

        # Boolean for tracking if the post is valid
        valid_post = True

        # Log the message details
        # log("\n" + post_message[0:75].replace('\n', "") + "...\n--POST ID: " +
        # str(post_id) + "\n--ACTOR ID: " + str(actor_id))

        # Check for pricing
        if not check_price_validity(post_message):
            valid_post = False
            log('----$', Color.RED)
            invalid_count += 1

        # Check for tag validity, including tags that say rooming and offering
        tags = get_tags(post_message)
        if not validate_tags(tags):
            valid_post = False
            log('----Tag', Color.RED)
            invalid_count += 1

        # Check post length.
        # Allow short ones if there's a craigslist link or parking
        if len(post_message) < 200 \
                and "craigslist" not in post_message.lower() \
                and not check_for_parking_tag(post_message):
            valid_post = False
            log('----Length', Color.RED)
            invalid_count += 1

        # Not a valid post
        if not valid_post:
            if dry_run:
                log("Dry - invalid deletion", Color.RED)
                log("--ID: " + post_id, Color.RED)
                log("--Message: " + post_message, Color.RED)
                log("\n")
            else:
                graph.delete(post_id)
        else:
            valid_posts.append(post_id)

    if not dry_run:
        log("Deleted " + str(invalid_count) + " invalid posts", Color.RED)

    # # Delete posts older than 30 days
    delete_old_posts(graph, group_id, admin_ids)

    # Save the updated caches
    log('Saving valid cache', Color.BOLD)
    save_cache(valid_db, valid_posts)

    save_properties(saved_props)

    # Done
    notify_mac()


# Main method
if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "fdpesu:n:v:g:",
                                   ["flushvalid", "dry", "printprops", "extend", "setprops", "token=", "propname=",
                                    "propvalue=", "propname="])
    except getopt.GetoptError:
        print 'check_and_delete.py -f -d -p -e -s -u <token> -n <propname> -v <propvalue> -g <propname>'
        sys.exit(2)

    # Check to see if we're running on Heroku
    if os.environ.get('MEMCACHEDCLOUD_SERVERS', None):
        import bmemcached

        log('Running on heroku, using memcached', Color.BOLD)

        # Authenticate Memcached
        running_on_heroku = True
        mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
                               os.environ.get('MEMCACHEDCLOUD_USERNAME'), os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

    propname = None
    propval = None
    log("Args - " + str(opts), Color.BOLD)
    if len(opts) != 0:
        for o, a in opts:
            if o in ("-e", "--extend"):
                extend_key = True
            elif o in ("-d", "--dry"):
                dry_run = True
            elif o in ("-s", "--setprops"):
                set_new_props()
                sys.exit()
            elif o in ("-u", "--update"):
                update_token(a)
                sys.exit()
            elif o in ("-n", "--propname"):
                propname = a
            elif o in ("-v", "--propvalue"):
                propval = a
            elif o in ("-p", "--printprops"):
                log("Printing props", Color.BLUE)
                props = load_properties()
                print props.keys()
                sys.exit()
            elif o in ("-g", "--getprop"):
                log("Getting value for " + a, Color.BLUE)
                props = load_properties()
                if a not in props.keys():
                    sys.exit(a + " doesn't exist in props")
                print props[a]
                sys.exit()
            elif o in ("-f", "--flushvalid"):
                response = raw_input("Are you sure? Y/N")
                if response.lower() == 'y':
                    log("Flushing cache for valid", Color.BLUE)
                    save_cache(valid_db, [])
                    log("Flushed cache", Color.BLUE)
                sys.exit()
            else:
                sys.exit('No valid args specified')

    if propname or propval:
        if propname and propval:
            log(propname + propval)
            update_prop(propname, propval)
        else:
            sys.exit('Must specify a prop name and value')
    else:
        sub_group()