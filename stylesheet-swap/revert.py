import os, sys
import glob
import praw
from derw import log

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <backup>')
    sys.exit(1)

r = praw.Reddit('RenegadeAI', user_agent='stylesheet swap')
log.debug(f'Successfully logged into reddit as {r.user.me()}')

for backup in os.listdir('backup'):
    if sys.argv[1] in backup:
        sub = r.subreddit(backup.split("_")[0])

        if not sub.user_is_moderator:
            log.error(f'{r.user.me()} is not a moderator of {sub.display_name}')
            sys.exit(1)

        log.info(f'Restoring {sub.display_name}')

        log.info("Clearing images")
        for image in sub.stylesheet().images:
            sub.stylesheet.delete_image(image["name"])
            log.debug(f'[{sub.display_name}] - {image["name"]}')

        log.info("Uploading images")
        img = f'backup/{backup}/images/'
        for image in os.listdir(img):
            sub.stylesheet.upload(os.path.splitext(image)[0], img + image)
            log.debug(f'[{sub.display_name}] - {image}')

        with open(f'backup/{backup}/stylesheet.css', 'r', encoding='utf-8') as file:
            sub.stylesheet.update(file.read())
            log.debug(f'[{sub.display_name}] - Updated CSS')
