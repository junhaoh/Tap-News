import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

import config_client
config = config_client.get_config('../config/config_news_pipeline.yaml')
SCRAPE_NEWS_TASK_QUEUE_URL = config['news_fetcher']['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['news_fetcher']['SCRAPE_NEWS_TASK_QUEUE_NAME']
DEDUPE_NEWS_TASK_QUEUE_URL = config['news_fetcher']['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['news_fetcher']['DEDUPE_NEWS_TASK_QUEUE_NAME']
SLEEP_TIME_IN_SECONDS = config['news_fetcher']['SLEEP_TIME_IN_SECONDS']

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print ('message is broken')
        return
    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text.encode('utf-8')

    dedupe_news_queue_client.sendMessage(task)

while True:
    # Fetch message from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print (e)
                pass
        
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)