#!/usr/bin/env python3
"""添加每日定时任务"""
import subprocess
from pathlib import Path

script_path = Path(__file__).parent / "run.sh"
cron_line = f"0 9 * * * bash {script_path}"

# 读取现有cron
result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
existing = result.stdout if result.returncode == 0 else ""

if str(script_path) in existing:
    print("✅ 定时任务已存在，无需重复添加")
else:
    new_cron = existing.rstrip() + "\n" + cron_line + "\n"
    proc = subprocess.run(["crontab", "-"], input=new_cron, text=True)
    if proc.returncode == 0:
        print(f"✅ 已添加每日9点自动运行任务")
        print(f"   {cron_line}")
    else:
        print("❌ 添加失败，请手动执行: crontab -e")
        print(f"   添加这行: {cron_line}")

print("\n查看当前定时任务: crontab -l")
