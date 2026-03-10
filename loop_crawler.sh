#!/data/data/com.termux/files/usr/bin/bash
while true; do
  echo "[$(date)] running crawler..."
  cd ~/vipersniper && python -m crawler.agents.scheduler >> ~/vipersniper/crawler.log 2>&1
  echo "[$(date)] sleeping 300s..."
  sleep 300
done
