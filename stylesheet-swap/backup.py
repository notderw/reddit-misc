import os, sys
import praw
import requests
import shutil
from datetime import datetime
from derw import log

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <backup>')
    sys.exit(1)

r = praw.Reddit('RenegadeAI', user_agent='stylesheet swap')
log.debug(f'Successfully logged into reddit as {r.user.me()}')

backup_name = f'{input("Name your backup:")}_{int(datetime.now().timestamp())}'

for s in sys.argv[1:]:
    sub = r.subreddit(s)

    log.info(f'Backing up {sub.display_name}')

    backup_dir = f'backup/{sub}_{backup_name}'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        os.makedirs(backup_dir + '/images')

    with open(f'{backup_dir}/stylesheet.css', 'w', encoding='utf-8') as css:
        css.write(f'{sub.stylesheet().stylesheet}')

    for image in sub.stylesheet().images:
        req = requests.get(image["url"], stream=True)
        if req.status_code == 200:
            with open(f'{backup_dir}/images/{image["name"]}{os.path.splitext(image["url"])[1]}', 'wb') as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)
