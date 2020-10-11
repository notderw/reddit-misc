import os, sys
import praw
import requests
import shutil
from derw import log

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <subreddit1> <subreddit2>')
    sys.exit(1)

r = praw.Reddit('RenegadeAI', user_agent='stylesheet swap')
log.debug(f'Successfully logged into reddit as {r.user.me()}')

subreddits = {}

# Check if user is mod on both subs
for s in sys.argv[1:]:
    subreddits[s] = {}
    subreddits[s]["subreddit"] = sub = r.subreddit(s)

    if not sub.user_is_moderator:
        log.error(f'{r.user.me()} is not a moderator of {sub.display_name}')
        sys.exit(1)

# Cache shit
for name, data in subreddits.items():
    sub = data["subreddit"]
    log.info(f'Caching {name}')

    # Cache css
    subreddits[name]["css"] = sub.stylesheet().stylesheet

    # Cache images
    subreddits[name]["images"] = {}
    for image in sub.stylesheet().images:
        r = requests.get(image["url"], stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            subreddits[name]["images"][f'{image["name"]}{os.path.splitext(image["url"])[1]}'] = r

def set_style(sub, data):
    log.info(f'{"="*32}')
    log.info(f'Setting style {sub.display_name}')
    log.info(f'{"="*32}')

    log.debug(f'[{sub.display_name}] Removing images')
    for image in sub.stylesheet().images:
        sub.stylesheet.delete_image(image["name"])
        log.debug(f'[{sub.display_name}] - {image["name"]}')

    log.debug(f'[{sub.display_name}] Uploading images')
    for name, image in data["images"].items():
        url = praw.const.API_PATH['upload_image'].format(subreddit=sub.display_name)
        img_name, img_type = os.path.splitext(name)
        req = sub._reddit.post(url,
                        data={
                            'name': img_name,
                            'upload_type': 'img',
                            'img_type': img_type.replace(".", "")
                        },
        files={'file': image.raw})
        log.debug(f'[{sub.display_name}] - {name} {", ".join(req["errors"])}')

    sub.stylesheet.update(data["css"])
    log.debug(f'[{sub.display_name}] Uploaded CSS')

sub1 = subreddits[list(subreddits.keys())[0]]
sub2 = subreddits[list(subreddits.keys())[1]]

log.info(f'Swapping subreddit style {sub1["subreddit"].display_name} <-> {sub2["subreddit"].display_name}')

set_style(sub1["subreddit"], sub2)
set_style(sub2["subreddit"], sub1)