import os, sys
import praw
import requests
import shutil
from derw import log

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <source> <destination>')
    sys.exit(1)

r = praw.Reddit('RenegadeAI', user_agent='stylesheet swap')
log.debug(f'Successfully logged into reddit as {r.user.me()}')

src_sub = r.subreddit(sys.argv[1])
dest_sub = r.subreddit(sys.argv[2])

log.info(f'Duplicating subreddit style {src_sub.display_name} --> {dest_sub.display_name}')

if not dest_sub.user_is_moderator:
    log.error(f'{r.user.me()} is not a moderator of {dest_sub.display_name}')
    sys.exit(1)

# log.info("Clearing images")
# for image in dest_sub.stylesheet().images:
#     dest_sub.stylesheet.delete_image(image["name"])

# Cache images
log.info("Moving images")
for image in src_sub.stylesheet().images:
    try:
        log.debug(f'Moving image {image["name"]}{os.path.splitext(image["url"])[1]}')
        r = requests.get(image["url"], stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            # PRAW doesn't support raw image uploads so we will do it ourselves
            # https://github.com/praw-dev/praw/blob/a75ebcf934fb49a6966a04d172fa00e957836958/praw/models/reddit/subreddit.py#L1874
            url = praw.const.API_PATH['upload_image'].format(subreddit=dest_sub.display_name)
            dest_sub._reddit.post(url,
                                data={
                                    'name': image["name"],
                                    'upload_type': 'img',
                                    'img_type': os.path.splitext(image["url"])[1].replace(".", "")
                                },
            files={'file': r.raw})

    except Exception as e:
        print(f'Error moving image {image["name"]}: {e}')

log.info("Copying CSS")
dest_sub.stylesheet.update(src_sub.stylesheet().stylesheet)