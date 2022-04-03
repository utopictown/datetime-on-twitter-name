from requests_oauthlib import OAuth1Session
import os
from py_dotenv import read_dotenv
from datetime import datetime
from pytz import timezone, all_timezones
from urllib import parse
import sys

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

session = OAuth1Session(
    os.getenv('CLIENT_KEY'),
    client_secret=os.getenv('CLIENT_SECRET'),
    resource_owner_key=os.getenv('ACCESS_TOKEN'),
    resource_owner_secret=os.getenv('ACCESS_TOKEN_SECRET'))

def update_twitter_name(offset_input):
    tz = timezone(offset_input)
    offset = round(tz.utcoffset(datetime.now()).total_seconds() / 3600)
    prepend = "+" if offset >= 0 else ""
    name = parse.quote(f"{datetime.now(tz).strftime('now: %d %B %Y %H:%M')} UTC{prepend}{offset}")
    session.post('https://api.twitter.com/1.1/account/update_profile.json?name=' + name)

offset_input = ""

try:
    sys.argv[1]
except:
    raise Exception('Please provide timezone')

offset_input = sys.argv[1].replace(" ", "")

if len(offset_input):
    if offset_input not in all_timezones:
        raise Exception('Invalid Timezone')
else:
    raise Exception('Please provide timezone')

update_twitter_name(offset_input)