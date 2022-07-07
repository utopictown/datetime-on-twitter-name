import random
from requests_oauthlib import OAuth1Session
import os
from py_dotenv import read_dotenv
from datetime import datetime
from pytz import timezone, all_timezones
from urllib import parse
import sys
import requests
from bs4 import BeautifulSoup, Tag

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

session = OAuth1Session(
    os.getenv('CLIENT_KEY'),
    client_secret=os.getenv('CLIENT_SECRET'),
    resource_owner_key=os.getenv('ACCESS_TOKEN'),
    resource_owner_secret=os.getenv('ACCESS_TOKEN_SECRET'))

def get_data(sg_section: Tag):
    for i, child in enumerate(sg_section.children):
            text = child.get_text(strip=True)
            if text != '' or i % 2 == 0:
                if i == 1:
                    if text == 'SINGAPORE':
                        region = 'SG'
                    if text == 'HONGKONG':
                        region = 'HK'
                    if text == 'SYDNEY':
                        region = 'SDY'
                if i == 3:
                    date = text
                if i == 5:
                    value = text
                    
    res = {
        'region': region,
        'date': date,
        'value': value
    }
                    
    return res

def update_twitter_name(offset_input, type='date'):
    if type == 'togel':
        r = requests.get('http://167.71.203.197/')
        soup = BeautifulSoup(r.content, 'html.parser')    
        td = soup.select_one('.resulttogellive')
        sdy_section = td.select_one('tr:nth-child(2)')
        res_sdy = get_data(sdy_section)
        sg_section = td.select_one('tr:nth-child(4)')
        res_sg = get_data(sg_section)
        hk_section = td.select_one('tr:nth-child(6)')
        res_hk = get_data(hk_section)
        name = parse.quote(f"{res_sg['region']}: {res_sg['value']} {res_hk['region']}: {res_hk['value']} {res_sdy['region']}: {res_sdy['value']}")
    if type == 'btc':
        r = requests.get('https://indodax.com/api/btc_idr/ticker')
        btcidr = r.json()['ticker']['buy']
        name = parse.quote(f"BTC-IDR: Rp {btcidr}")
    if type == 'eth':
        r = requests.get('https://indodax.com/api/eth_idr/ticker')
        ethidr = r.json()['ticker']['buy']
        name = parse.quote(f"ETH-IDR: Rp {ethidr}")
    if type == 'kobo':
        r = requests.get('https://kobo-kanaeru.vercel.app/api/kobo')
        kobosub = r.json()['youtube']['subscriberCount']
        name = parse.quote(f"Kobo YT Subs: {kobosub}")
    else:
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

mode_list = os.getenv('MODE').split(',')

index = random.randint(0, len(mode_list) - 1)

update_twitter_name(offset_input, mode_list[index])