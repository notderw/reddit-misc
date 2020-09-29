import os
from time import sleep
from datetime import datetime

import praw

NAME = os.environ.get("NAME", "")
SUBREDDIT = os.environ.get("SUBREDDIT")

if __name__ == "__main__":
    try:
        r = praw.Reddit(NAME, user_agent='https://github.com/notderw/reddit-misc/edited-after-approved')

        subreddit = r.subreddit(SUBREDDIT)

        print(f'Logged in as /u/{r.user.me()}, watching /r/{subreddit}')

        while True:
            for submission in subreddit.mod.edited(only="submissions", limit=None):
                if submission.approved and submission.edited > submission.approved_at_utc:
                    approved_at = datetime.fromtimestamp(submission.approved_at_utc)
                    edited_at = datetime.fromtimestamp(submission.edited)
                    print(f'{submission.shortlink} approved@{approved_at} editited@{edited_at}')

                    msg = (
                        f'Submission {submission.shortlink}\n\n'
                        f'Was editied {(edited_at-approved_at)} after it was approved @ {approved_at}'
                    )

                    subreddit.message('Submission editied after approval', msg)
                    submission.mod.remove(mod_note="edited after approval")

            sleep(5 * 60)

    except KeyboardInterrupt:
        print("Exiting")
