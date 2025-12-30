#!/bin/bash

echo "=========================================="
echo "📦 Installing Dependencies"
echo "=========================================="

cd /root/tg-mitm-system

echo "[1] Updating pip..."
python3 -m pip install --upgrade pip

echo "[2] Installing packages..."
pip install aiogram mitmproxy aiohttp requests

echo "[3] Verifying installation..."
python3 -c "
try:
    import aiogram, mitmproxy, requests
    print('✅ All dependencies installed!')
    print(f'   aiogram: {aiogram.__version__}')
    print(f'   requests: {requests.__version__}')
except ImportError as e:
    print(f'❌ Error: {e}')
"

echo "=========================================="
echo "✅ Installation complete!"
echo "Run: ./start.sh <BOT_TOKEN> <ADMIN_ID>"
echo "=========================================="
