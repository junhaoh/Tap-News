# !/bin/bash

brew services restart mongodb
brew services restart redis

# pip install -r requirements.txt

cd /Users/junhao/Downloads/Project/Tap-News/news_pipeline
python news_monitor.py &
python news_fetcher.py &
python news_deduper.py &

