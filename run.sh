#!/bin/bash

# 1. Start the Telegram Bot in the background
echo "🚀 Starting Telegram Bot..."
#python app.py &

# 2. Start the Streamlit Dashboard
# We bind it to port 10000 so Render can find it
echo "📈 Starting Streamlit Dashboard..."
streamlit run dashboard.py --server.port 10000 --server.address 0.0.0.0