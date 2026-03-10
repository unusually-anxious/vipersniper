#!/data/data/com.termux/files/usr/bin/bash
pkill -f "redis-server" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
pkill -f "http.server 3000" 2>/dev/null
pkill -f "loop_crawler.sh" 2>/dev/null
pkill -f "crawler.agents.scheduler" 2>/dev/null

echo "Starting Redis..."
redis-server > ~/vipersniper/redis.log 2>&1 &

sleep 2

echo "Starting Backend API..."
cd ~/vipersniper && nohup uvicorn api:app --host 0.0.0.0 --port 8000 > ~/vipersniper/backend.log 2>&1 &

echo "Starting Frontend..."
cd ~/vipersniper/frontend && nohup python3 -m http.server 3000 > ~/vipersniper/frontend.log 2>&1 &

echo "Starting Auto Crawler..."
cd ~/vipersniper && nohup ~/vipersniper/loop_crawler.sh > ~/vipersniper/loop.log 2>&1 &

sleep 3
echo ""
echo "VIPERSNIPER RUNNING"
echo "Dashboard: http://127.0.0.1:3000"
echo "Hunter:    http://127.0.0.1:3000/hunter.html"
echo "API:       http://127.0.0.1:8000/listings"
echo ""
echo "Logs:"
echo "tail -f ~/vipersniper/crawler.log"
