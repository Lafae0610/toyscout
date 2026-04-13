#!/bin/bash
# 每日运行脚本（cron调用这个）
cd "$(dirname "$0")"
source .env 2>/dev/null
export ANTHROPIC_API_KEY
python3 finder.py >> "output/run_$(date +%Y%m%d).log" 2>&1
