import os
import cPickle as pickle
import webbrowser
import datetime
import facebook
import time
import subprocess
import sys

__author__ = 'Henri Sweers'

############## Global vars ##############

# 24 hours, in seconds
time_limit = 86400

# Pickle cache file caching warned posts
db_file = "fb_subs_cache"

# Pickle cache file for properties
prop_file = "login_prop"


# Color class, used for colors in terminal
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Junk method that I use for testing stuff periodically
def test():
    log('Test', Color.PURPLE)


# Use this method to set new vals for props, such as on your first run
def set_new_props():
    saved_dict = load_properties()

    #### Uncomment lines below as needed to manually set stuff ####

    #### These are strings
    # saved_dict['sublets_oauth_access_token'] = "put-auth-token-here"
    # saved_dict['sublets_api_id'] = "put-app-id-here"
    # saved_dict['sublets_secret_key'] = "put-secret-key-here"
    # saved_dict['access_token_expiration'] = "put-access-token-expiration-here"
    # saved_dict['group_id'] = "put-group-id-here"

    #### These are ints
    # saved_dict['bot_id'] = put-bot-id-here
    # saved_dict['ignored_post_ids'].append(<id_num>)
    # saved_dict['ignore_source_ids'].append(<id_num>)

    #### You can do other stuff too, the above are just examples ####

    save_properties(saved_dict)


# Method for initializing your prop values
def init_props():
    test_dict = {'sublets_oauth_access_token': "put-auth-token-here",
                 'sublets_api_id': "put-app-id-here",
                 'sublets_secret_key': "put-secret-key-here",
                 'group_id': 'put-group-id-here',
                 'bot_id': -1,
                 'ignored_post_ids': [],
                 'ignore_source_ids': []}
    save_properties(test_dict)
    saved_dict = load_properties()
    assert test_dict == saved_dict


# Method for saving (with pickle) your prop values
def save_properties(data):
    with open(prop_file, 'w+') as login_prop_file:
        pickle.dump(data, login_prop_file)


# Method for loading (with pickle) your prop values
def load_properties():
    if os.path.isfile(prop_file):
        with open(prop_file, 'r+') as login_prop_file:
            data = pickle.load(login_prop_file)
            return data
    else:
        sys.exit("No prop file found")


# Nifty method for sending notifications on my mac when it's done
def notify_mac():
    if sys.platform == "darwin":
        try:
            subprocess.call(
                ["terminal-notifier", "-message", "Done", "-title", "FB_Bot",
                 "-sound", "default"])
        except OSError:
            print "If you have terminal-notifier, this would be a notification"


# Log method. If there's a color argument, it'll stick that in first
def log(message, *colorargs):
    if len(colorargs) > 0:
        print colorargs[0] + message + Color.END
    else:
        print message


# Method for checking tag validity
def check_tag_validity(message_text):
    valid_tags = [
        "[looking]", "[offering]", "[rooming]", "{looking}", "{offering}",
        "{rooming}", "(looking)",
        "(offering)", "(rooming)"]

    message_text = message_text.lower()
    for x in valid_tags:
        if x in message_text:
            return True

    return False


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

    # List of posts to ignore
    ignored_post_ids = saved_props['ignored_post_ids']

    # List of people to ignore
    ignore_source_ids = saved_props['ignore_source_ids']

    # ID of the FB group
    group_id = saved_props['group_id']

    # User ID of the bot
    bot_id = saved_props['bot_id']

    # FQL query for the group
    group_query = "SELECT post_id, message, actor_id FROM stream WHERE " + \
                  "source_id=" + group_id + " LIMIT 50"

    # Get current time
    now_time = time.time()

    # Make sure the access token is still valid
    if access_token_expiration < now_time:
        sys.exit("API Token is expired")

    # Warn if the token's expiring soon
    if access_token_expiration - now_time < 604800:
        log("Warning - access token expires in less than a week", Color.RED)
        log("-- Expires on " + datetime.datetime.fromtimestamp(
            access_token_expiration).strftime('%Y-%m-%d %H:%M:%S'))

    # Log in, try to get posts
    graph = facebook.GraphAPI(sublets_oauth_access_token)

    # Extend the access token, default is ~2 months from current date
    if extend_key:
        result = graph.extend_access_token(sublets_api_id, sublets_secret_key)
        new_token = result['access_token']
        new_time = int(result['expires']) + now_time

        saved_props['sublets_oauth_access_token'] = new_token
        saved_props['access_token_expiration'] = new_time

        log("Token extended", Color.BOLD)

    # Make our first request, get the group posts
    group_posts = graph.fql(query=group_query)

    # Load the pickled cache of previously warned posts
    already_warned = dict()
    log("Checking cache...", Color.BOLD)
    if os.path.isfile(db_file):
        with open(db_file, 'r+') as f:

            # If the file isn't at its end or empty
            if f.tell() != os.fstat(f.fileno()).st_size:
                already_warned = pickle.load(f)
    else:
        log("No cache file found, a new one will be created", Color.BLUE)

    log('(Cache size: ' + str(len(already_warned)) + ")", Color.BOLD)

    # Loop over retrieved posts
    for post in group_posts:

        # Important data received
        post_message = post['message']      # Content of the post
        post_id = post['post_id']           # Unique ID of the post

        # Unique ID of the person that posted it
        actor_id = post['actor_id']

        # Data to use
        post_comment = "(This is an automated comment)\n\nIt looks like" + \
                       " your post has a few issues:\n"

        # Boolean for tracking if the post is valid
        valid_post = True

        # Ignore mods and certain posts
        if post_id in ignored_post_ids or actor_id in ignore_source_ids:
            log('\n--Ignored post: ' + post_id, Color.BOLD)
            continue

        # Log the message details
        log("\n" + post_message[0:75].replace('\n', "") + "...\n--POST ID: " +
            str(post_id) + "\n--ACTOR ID: " + str(actor_id))

        # Check for pricing
        if "$" not in post_message and "/month" not in post_message and \
                "per month" not in post_message:
            valid_post = False
            post_comment += "- Your post doesn't seem to mention pricing" + \
                            " (no $ signs, <number>/month), \"per month\"\n"
            log('----$', Color.BLUE)

        # Check for tag validity
        if not check_tag_validity(post_message):
            valid_post = False
            post_comment += \
                "- Your post appears to be missing a proper tag at the" + \
                " front ([LOOKING], [ROOMING], or [OFFERING])\n"
            log('----Tag', Color.BLUE)

        # Check post length. Allow short ones if there's a craigslist link
        if len(post_message) < 200 and "craigslist" not in post_message.lower():
            valid_post = False
            post_comment += \
                "- Your post is a little short (<200 chars). Please give" + \
                " more information (what you're looking for, details," + \
                " preferences, etc.)\n"
            log('----Length', Color.BLUE)

        # Not a valid post
        if not valid_post:

            # If already warned, delete if it's been more than 24 hours, ignore
            # if it's been less
            if post_id in already_warned:
                if time_limit < now_time - already_warned[post_id]:
                    log('--Delete: ' + post_id, Color.RED)
                    url = "http://www.facebook.com/" + post_id
                    webbrowser.open_new_tab(url)
                    del already_warned[post_id]
                else:
                    time_delta = time_limit - (now_time -
                                               already_warned[post_id])
                    m, s = divmod(time_delta, 60)
                    h, m = divmod(m, 60)
                    log_message = '--Invalid, but still have '
                    if h > 0:
                        log_message += '%d hours and ' % h
                    log_message += '%02d minutes' % m
                    log(log_message, Color.RED)
                continue

            # Comment with a warning and cache the post
            else:

                # Should check to make sure the bot hasn't posted before
                post_comment += \
                    "\nPlease edit your post and fix the above within 24" + \
                    " hours, or else your post will be deleted per the" + \
                    " group rules. Thanks!\n\n(If you think this was a" + \
                    " mistake don't hesitate to message me)"

                previously_commented = False
                comments_query = "SELECT fromid, id, time FROM comment" + \
                                 " WHERE post_id=\"" + str(post_id) + "\""
                comments = graph.fql(comments_query)
                for comment in comments:

                    # Found a comment from the bot
                    if comment['fromid'] == bot_id:
                        log('--Previously warned')
                        log('----caching')
                        previously_commented = True
                        already_warned[post_id] = comment['time']
                        break

                # Comment if no previous comment
                if not previously_commented:
                    graph.put_object(
                        post['post_id'], "comments", message=post_comment)
                    # Save
                    already_warned[post_id] = now_time
                    log('--WARNED', Color.RED)

        # Valid post
        else:
            log('--VALID', Color.GREEN)

            # Remove warning comment if it's valid now
            if post_id in already_warned:
                log('--Removing any warnings')
                comments_query = "SELECT fromid, id FROM comment" + \
                                 " WHERE post_id=\"" + str(post_id) + "\""
                comments = graph.fql(comments_query)
                for comment in comments:
                    if comment['fromid'] == bot_id:
                        # Delete warning comment
                        graph.delete_object(comment['id'])
                        log('--Warning deleted')

                # Remove post from list of warned people
                log('--Removing from cache')
                del already_warned[post_id]

    # Save the updated cache
    log('Saving cache', Color.BOLD)
    with open(db_file, 'r+') as f:
        pickle.dump(already_warned, f)

    save_properties(saved_props)
    notify_mac()


# Main method
if __name__ == "__main__":
    args = sys.argv
    extend_key = False

    # Arg parsing. I know, there's better ways to do this
    if len(args) > 1:
        if "--extend" in args:
            extend_key = True
        elif "setprops" in args:
            set_new_props()
            sys.exit()
        elif "init" in args:
            init_props()
            sys.exit()
        elif "test" in args:
            test()
            sys.exit("Done testing")
        else:
            sys.exit('No valid args specified')

    sub_group()