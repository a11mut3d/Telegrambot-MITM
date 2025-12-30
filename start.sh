#!/bin/bash

cd /root/tg-mitm-system

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <BOT_TOKEN> <ADMIN_ID>"
    echo ""
    echo "Example:"
    echo "  $0 '1234567890:ABCdefGHIjklMnOpQRstuVWXyz123456' 123456789"
    echo ""
    echo "Get token from @BotFather"
    echo "Get ID from @userinfobot"
    exit 1
fi

TOKEN=$1
ADMIN_ID=$2

# Проверка токена
if [[ ! "$TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    echo "ERROR: Invalid token format!"
    exit 1
fi

echo "=========================================="
echo "🤖 Starting MITM System"
echo "=========================================="
echo "Admin ID: $ADMIN_ID"
echo "Bot Token: ${TOKEN:0:10}..."
echo "MITM Port: 8082"
echo "=========================================="

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

sudo fuser -k 8082/tcp 2>/dev/null
sleep 2

# Запускаем
python3 run.py "$TOKEN" "$ADMIN_ID"
