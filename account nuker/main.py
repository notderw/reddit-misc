import praw
import time
import warnings

warnings.filterwarnings('ignore')

user_agent = "NUKER /u/RenegadeAI"
r = praw.Reddit(user_agent=user_agent)
r.login("<redacted>", "<redacted>")

print("Enter user:")
user_name = input();
user = r.get_redditor(user_name)

submit = user.get_submitted(limit=None)
comment = user.get_comments(limit=None)

for s in submit:
    try:
        s = r.get_submission(submission_id=s.id)
        s.remove(spam=True)
        print("REMOVED: " + s.title)
    except:
        print("ERROR REMOVING: " + s.title)

for c in comment:
    try:
        c.remove(spam=True)
        try:
            print("REMOVED: " + str(c) + "\n")
        except:
            print("Error encoding comment")
    except:
        try:
            print("\033[93mERROR REMOVING: " + str(c) + "\n")
        except:
            print("Error encoding comment")

wait = input("PRESS ENTER TO CONTINUE.")