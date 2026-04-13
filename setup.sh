#!/bin/bash
# 一键安装 & 配置
cd "$(dirname "$0")"

echo "📦 安装依赖..."
pip3 install -r requirements.txt

echo ""
echo "⚙️  配置API Key..."
if [ ! -f .env ]; then
    read -p "请输入你的 ANTHROPIC_API_KEY: " key
    echo "ANTHROPIC_API_KEY=$key" > .env
    echo "✅ 已保存到 .env"
else
    echo "✅ .env 已存在"
fi

echo ""
echo "🎉 安装完成！运行方式："
echo "   cd $(pwd)"
echo "   source .env && export ANTHROPIC_API_KEY && python3 finder.py"
echo ""
echo "如需每天自动运行，执行："
echo "   python3 setup_cron.py"
