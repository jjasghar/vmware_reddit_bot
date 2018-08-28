import praw
import time
import os
import re

def bot_login():
    print("Logging in...")
    r = praw.Reddit(username = "branding_bot",
                    password = os.environ['PASSWORD'],
                    client_id = os.environ['CLIENT_ID'],
                    client_secret = os.environ['CLIENT_SECRET'],
                    user_agent = '<console:branding_bot:0.0.1 (by /u/jjasghar)'
                    )
    print("Logged in!")

    return r

def run_bot(r, comments_replied_to):

    subreddits = ['sysadmin','devops','vmware','homelab','selfhosted']

    for i in subreddits:
        subreddit = r.subreddit(i)

        print("Obtaining 500 comments in " + i + " at " + time.ctime())


        new_polling = subreddit.new(limit=500)


        for submission in new_polling:
            comments = submission.comments.list()

            for comment in comments:
                vmware = re.compile(".*VMWare.*")
                try:
                    if vmware.match(comment.body) and comment.id not in comments_replied_to and comment.author != r.user.me():
                        comment.reply("A friendly note, the official branding of [VMware](https://www.vmware.com/) is without a capital 'W'. Take a look [here](https://www.vmware.com/brand/our-brand.html) if you'd like more details. _Beep Boop I'm a bot if you have questions or suggestions please message /u/jjasghar about it_.")
                        print("Found a \"VMWare\" in the comment " + comment.id)
                        comments_replied_to = list(comments_replied_to)
                        comments_replied_to.append(comment.id)

                        with open ("comments_replied_to.txt", "a") as f:
                            f.write(comment.id + "\n")
                        print("Taking 30 second a rest at " + time.ctime())
                        time.sleep(30)
                except AttributeError:
                    pass
                except praw.exceptions.APIException as e:
                    if (e.error_type == "RATELIMIT"):
                        delay = re.search("(\d+) minutes?", e.message)

                        print(e.message)

                        if delay:
                            delay_seconds = float(int(delay.group(1)) * 60)
                            time.sleep(delay_seconds)
                            continue
                        else:
                            delay = re.search("(\d+) seconds?", e.message)
                            delay_seconds = float(delay.group(1))
                            time.sleep(delay_seconds)
                            continue
                except:
                    errors = error + 1
                    if (errors > 5):
                        print("Something is REALLY wrong at " + time.ctime())
                        exit(1)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)

    return comments_replied_to


r = bot_login()
comments_replied_to = get_saved_comments()
while True:
    run_bot(r, comments_replied_to)
