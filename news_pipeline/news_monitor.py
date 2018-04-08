# " coding utf-8 " 

import datetime
import hashlib
import os
import redis
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

import config_client
config = config_client.get_config('../config/config_news_pipeline.yaml')
REDIS_HOST = config['news_monitor']['REDIS_HOST']
REDIS_PORT = config['news_monitor']['REDIS_PORT']
SCRAPE_NEWS_TASK_QUEUE_URL = config['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_NAME']
SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

NEWS_SOURCES = [
    'abc-news',
    'bbc-news',
    'bbc-sports',
    'bleacher-report',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'usa-today'
]

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            
            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print ('Fetched %d new news.' % num_of_new_news)
    
    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)