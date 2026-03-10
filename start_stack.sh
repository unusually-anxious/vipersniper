#!/data/data/com.termux/files/usr/bin/bash
source ~/.bashrc 2>/dev/null
pkill -f "uvicorn api:app" 2>/dev/null
pkill -f "uvicorn api.main:app" 2>/dev/null
pkill -f "http.server 3000" 2>/dev/null
pkill -f "crawler.agents.scheduler" 2>/dev/null
cd ~/vipersniper && nohup uvicorn api:app --host 0.0.0.0 --port 8000 > ~/vipersniper/backend.log 2>&1 &
cd ~/vipersniper/frontend && nohup python3 -m http.server 3000 > ~/vipersniper/frontend.log 2>&1 &
cd ~/vipersniper && nohup python3 -m crawler.agents.scheduler > ~/vipersniper/crawler.log 2>&1 &
sleep 4
echo "BACKEND:" && curl -s http://127.0.0.1:8000/health ; echo
echo "LISTINGS:" && curl -s http://127.0.0.1:8000/listings ; echo
echo "FRONTEND: http://127.0.0.1:3000"
