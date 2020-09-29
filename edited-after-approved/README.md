# editied-after approved

notify a subreddit when a post was editied after a mod approved it

## setup

Create a "script" app [here](https://old.reddit.com/prefs/apps/)

User [this tool](https://not-an-aardvark.github.io/reddit-oauth-helper/) to generate your oauth tokens

Create a `praw.ini` file as described [here](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html), specifically [this section](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#defining-additional-sites)

Rename `.env.example` to `.env` and fill the "site name" from your `praw.ini` for `NAME` and the target subreddit.

Install [Python 3.8](https://www.python.org/downloads/release/python-385/)

Install [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)

Run the following commands in the same folder as `bot.py`

```bash
pipenv install
```

## run

```bash
pipenv run python bot.py
```
