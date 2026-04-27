#!/bin/bash
export DEV_HUB_ADMIN_TOKEN="$(cat /home/hn3t/dev_hub/.devhub_token)"
cd /home/hn3t/dev_hub
nohup python3 app.py > /home/hn3t/logs/dev_hub_8099.log 2>&1 &
