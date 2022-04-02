from requests_oauthlib import OAuth1Session
import os
from py_dotenv import read_dotenv
import schedule
import time
from datetime import datetime
from pytz import timezone

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

twitter = OAuth1Session(
    os.getenv('CLIENT_KEY'),
    client_secret=os.getenv('CLIENT_SECRET'),
    resource_owner_key=os.getenv('ACCESS_TOKEN'),
    resource_owner_secret=os.getenv('ACCESS_TOKEN_SECRET'))

def update_twitter_name():
    tz = timezone('Asia/Jakarta')
    name = datetime.now(tz).strftime('now%%3A %d %B %Y %H%%3A%M')
    twitter.post('https://api.twitter.com/1.1/account/update_profile.json?name=' + name)

update_twitter_name()
  
schedule.every(5).seconds.do(update_twitter_name)
  
while True:
    schedule.run_pending()
    time.sleep(1)