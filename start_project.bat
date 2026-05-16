@echo off
title Fraud Detection System Launcher
echo 🚀 Starting Real-Time Fraud Detection System...

:: 1. Start Docker Infrastructure
echo 🐋 Starting Kafka in Docker...
docker-compose up -d

:: Give Kafka a solid 15 seconds to finish its internal booting cycle
echo ⏳ Waiting for Kafka broker ports to open...
timeout /t 15 /nobreak > nul



:: 3. Start Consumer (in a new window)
echo 📥 Starting Consumer...
start cmd /k "python stream_consumer.py"

:: 4. Start Dashboard (in a new window)
echo 📊 Starting Streamlit Dashboard...
start cmd /k "streamlit run dashboard.py"

:: 5. Start Producer (in new window)
echo Starting Transaction Producer...
start "Kafka Producer" cmd /k "python stream_producer.py"

echo 📤 Starting Transaction Producer...
echo --------------------------------------------------
echo SYSTEM IS LIVE. Close this window to stop producing.
echo --------------------------------------------------


pause