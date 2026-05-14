@echo off
title Fraud Detection System Launcher
echo 🚀 Starting Real-Time Fraud Detection System...

:: 1. Start Docker Infrastructure
echo 🐋 Starting Kafka in Docker...
docker-compose up -d
timeout /t 10 /nobreak > nul

:: 2. Create Kafka Topic (just in case)
echo 🛣️ Creating Kafka Topic...
docker exec kafka_broker kafka-topics --create --topic transactions --bootstrap-server localhost:9092 --if-not-exists

:: 3. Train Model
echo Training Model...
python train.py

:: 4. Start Consumer (in a new window)
echo  Starting Consumer...
start cmd /k "python stream_consumer.py"

:: 5. Start Dashboard (in a new window)
echo  Starting Streamlit Dashboard...
start cmd /k "streamlit run dashboard.py"

:: 6. Start Producer (in this window)
echo Starting Transaction Producer...
echo --------------------------------------------------
echo SYSTEM IS LIVE. Close this window to stop producing.
echo --------------------------------------------------
python stream_producer.py

pause