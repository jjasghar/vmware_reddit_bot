"Script for running the VMware Reddit Bot"

import time
import os
import sys
import re
import praw

def log(message):
    "Print message in a way that Habitat's Supervisor will ouput"
    print(message)
    sys.stdout.flush()

def bot_login():
    "Perform login"

    return praw.Reddit(username="branding_bot",
                       password=os.environ['PASSWORD'],
                       client_id=os.environ['CLIENT_ID'],
                       client_secret=os.environ['CLIENT_SECRET'],
                       user_agent="<console:branding_bot:0.0.1 (by /u/%s)"
                       % os.environ['REDDIT_USERNAME']
                      )

def handle_rate_limit(message):
    "Determine delay based on rate limit error"
    delay_regex = r"(\d+) (minutes|seconds)?"
    delay = re.search(delay_regex, message)
    log(message)
    if delay.group(2) == "minutes":
        delay_seconds = float(int(delay.group(1)) * 60)
    elif delay.group(2) == "seconds":
        delay_seconds = float(delay.group(1))
    time.sleep(delay_seconds)

def save_comment(comments_replied_to, comment_id):
    "Append comment id to list and save to disk"
    comments_replied_to.append(comment_id)

    with open("comments_replied_to.txt", "a") as comments_file:
        comments_file.write(comment_id + "\n")

    return comments_replied_to

def check_comment(comment, reddit_api, comments_replied_to):
    "Check comment for 'VMWare' misspelling"

    vmware_regex = re.compile(".*VMWare.*")

    is_regex_match = bool(vmware_regex.match(comment.body))
    is_new_comment = comment.id not in comments_replied_to
    is_self = comment.author.name == reddit_api.user.me().name

    return is_regex_match and is_new_comment and not is_self

def get_saved_comments():
    "Load saved comments"
    data_file = os.path.join(os.path.dirname(__file__),
                             "comments_replied_to.txt")
    if not os.path.isfile(data_file):
        raise RuntimeError("Cannot find saved comments")
    else:
        with open(data_file, "r") as comments_file:
            return list(filter(None, comments_file.read().split("\n")))

def run_bot(reddit_api, comments_replied_to):
    "Go through subreddits, load comments, reply if needed"
    for i in os.environ['SUBREDDITS'].split(" "):
        subreddit = reddit_api.subreddit(i)

        log("Obtaining 500 comments in " + i + " at " + time.ctime())
        errors = 0
        new_polling = subreddit.new(limit=500)
        for submission in new_polling:
            for comment in submission.comments.list():
                try:
                    if check_comment(comment, reddit_api, comments_replied_to):
                        comment.reply(os.environ['BOT_REPLY_MESSAGE'])
                        log("Found a \"VMWare\" in the comment " + comment.id)
                        comments_replied_to = save_comment(comments_replied_to,
                                                           comment.id)

                        log("Taking 30 second a rest at " + time.ctime())
                        time.sleep(30)
                except AttributeError:
                    pass
                except praw.exceptions.APIException as exception:
                    if exception.error_type == "RATELIMIT":
                        handle_rate_limit(exception.message)
                        continue
                except RuntimeError as exception:
                    errors += 1
                    if errors > 5:
                        raise exception

def main():
    "Script entry point"
    log("Logging in...")
    reddit_api = bot_login()
    log("Logged in!")
    comments_replied_to = get_saved_comments()
    while True:
        run_bot(reddit_api, comments_replied_to)

if __name__ == "__main__":
    main()
