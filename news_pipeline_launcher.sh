#!/bin/bash

# sudo mongod
# cd /Users/junhaohuang/Downloads/Software/redis-4.0.8
# src/redis-server

# pip install -r requirements.txt

cd /Users/junhaohuang/Downloads/Projects/Tap-News/news_pipeline
python news_monitor.py &
python news_fetcher.py &
python news_deduper.py &

