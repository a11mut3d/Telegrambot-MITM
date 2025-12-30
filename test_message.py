#!/usr/bin/env python3
import sys

test_message = '''
💰 ТЕСТОВОЕ СООБЩЕНИЕ ДЛЯ MITM

Крипто-кошельки:
Bitcoin (BTC): bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq
Ethereum (ETH): 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
USDT TRC20: TNDzfER7vL1hJ5sZ7v8w9x0y1z2a3b4c5d6e7f8g9h0
USDT ERC20: 0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B
TON: UQB6Z4RwcBqA3L8Z8-7lP5sN4nLx5j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8
Solana: So11111111111111111111111111111111111111112
BNB: bnb1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq

Крипто-чек:
https://t.me/CryptoTestBot/send?start=CHECK_123456789_ABC_DEF_GHI

Отправьте это сообщение через прокси 8082
'''

if len(sys.argv) > 1 and sys.argv[1] == "short":
    print("BTC: bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq")
    print("Check: https://t.me/test/send?start=TEST_CHECK_123")
else:
    print(test_message)
