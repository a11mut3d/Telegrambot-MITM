#!/bin/bash

echo "🔍 Checking system permissions..."

cd /root/tg-mitm-system

echo "[1] Checking data.json..."
if [ -f "data.json" ]; then
    ls -la data.json
    echo "File content (first 10 lines):"
    head -10 data.json
else
    echo "data.json does not exist"
fi

echo -e "\n[2] Testing Python imports..."
python3 -c "
try:
    from storage import storage
    print('✅ storage imports ok')

    wallets = storage.get_all_wallets()
    print(f'✅ Got {len(wallets)} wallets')

    for coin, addr in wallets.items():
        print(f'   {coin}: {addr[:20]}...')

except Exception as e:
    print(f'❌ Error: {e}')
"

echo -e "\n[3] Testing file write..."
python3 -c "
import json
try:
    with open('test_write.json', 'w') as f:
        json.dump({'test': 'data'}, f)
    print('✅ Can write to files')
    import os
    os.remove('test_write.json')
except Exception as e:
    print(f'❌ Cannot write: {e}')
"
