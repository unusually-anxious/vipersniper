#!/data/data/com.termux/files/usr/bin/bash
source ~/.bashrc

pkill -f "uvicorn api.main:app" 2>/dev/null
pkill -f "http.server 3000" 2>/dev/null

cd ~/vipersniper/backend && nohup uvicorn api.main:app --host 0.0.0.0 --port 8000 > ~/vipersniper/backend.log 2>&1 &
cd ~/vipersniper/frontend && nohup python3 -m http.server 3000 > ~/vipersniper/frontend.log 2>&1 &

sleep 3
echo "BACKEND TEST:"
curl -s http://127.0.0.1:8000/health
echo
echo "FRONTEND: http://127.0.0.1:3000"
