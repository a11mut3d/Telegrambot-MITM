import re

class CryptoPatterns:
    BTC = re.compile(r'\b(bc1[a-z0-9]{25,59}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b', re.IGNORECASE)
    ETH = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
    USDT_TRC20 = re.compile(r'\bT[A-Za-z1-9]{33}\b')
    USDT_ERC20 = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
    TON = re.compile(r'\b(?:UQ|EQ)[A-Za-z0-9_\-]{43,48}\b')
    SOL = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
    BNB = re.compile(r'\bbnb1[a-z0-9]{25,59}\b', re.IGNORECASE)

    CRYPTO_CHECKS = [
        re.compile(r'https?://t\.me/[a-zA-Z0-9_]+/send\?start=[A-Za-z0-9_\-]+'),
        re.compile(r't\.me/[a-zA-Z0-9_]+/send\?start=[A-Za-z0-9_\-]+'),
        re.compile(r'send\?start=[A-Za-z0-9_\-]{10,50}'),
        re.compile(r'start=[A-Za-z0-9_\-]{10,50}')
    ]

    @classmethod
    def get_all_patterns(cls):
        return {
            "BTC": cls.BTC,
            "ETH": cls.ETH,
            "USDT_TRC20": cls.USDT_TRC20,
            "USDT_ERC20": cls.USDT_ERC20,
            "TON": cls.TON,
            "SOL": cls.SOL,
            "BNB": cls.BNB
        }

    @classmethod
    def get_wallet_types(cls):
        return ["BTC", "ETH", "USDT_TRC20", "USDT_ERC20", "TON", "SOL", "BNB"]

    @classmethod
    def detect_wallet_type(cls, text: str) -> str:
        for coin_type, pattern in cls.get_all_patterns().items():
            if pattern.search(text):
                return coin_type
        return None

    @classmethod
    def find_all_wallets(cls, text: str) -> dict:
        wallets = {}
        for coin_type, pattern in cls.get_all_patterns().items():
            matches = pattern.findall(text)
            if matches:
                wallets[coin_type] = matches
        return wallets
