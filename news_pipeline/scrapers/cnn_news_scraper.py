import requests
import os
import random
from lxml import html

GET_CNN_NEWS_XPATH =  "//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])

random.shuffle(USER_AGENTS)


def getHeader():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection": "close",
        "User-Agent": ua
    }
    return headers


def extract_news(news_url):
    # Fetch html
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeader())

    news = {}

    try:
        # Parse html
        tree = html.fromstring(response.content)
        # Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print 
        return {}
    return news

    
    
    return None