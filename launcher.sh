#!/bin/bash

# getNewsSummariesForUser(user_id, pageNum), logNewsClickForUser(user_id, news_id))
# port 4040
cd backend_server
python service.py&

# getPreferenceForUser(user_id), update model using time decaying method
# port 5050
cd ../news_recommendation_service
python click_log_processor.py&
python recommendation_service.py&

# machine learning model
# port 6060
cd ../news_topic_modeling_service/server
python server.py&

# react and node server
# port 3000
cd ../../web-server/server
npm run dev&

