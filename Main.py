import os
import time
import logging
import requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ============= CONFIG =============
BOT_TOKEN = os.getenv("BOT_TOKEN")  # set this in Render
YOUR_TELEGRAM_ID = 7778390732

# Filters (you can adjust later)
FILTERS = {
    "liquidity": 10000,
    "market_cap": 16000,
    "holders": 100,
    "fees_paid": 1
}

# ==================================
logging.basicConfig(level=logging.INFO)
seen_tokens = set()

# ============= PLACEHOLDER for your data fetching =============
def get_new_tokens():
    """
    👇 TODO:
    Replace this function later with Pump.fun API fetching logic.
    For now, it just returns example data.
    """
    return [
        {
            "name": "TestCoin",
            "symbol": "TST",
            "liquidity": 12000,
            "market_cap": 18000,
            "holders": 130,
            "fees_paid": 1.2,
            "contract": "0xExampleCA12345",
            "pumpfun_link": "https://pump.fun/coin/0xExampleCA12345",
            "socials": {
                "twitter": "https://twitter.com/example",
                "telegram": "https://t.me/example"
            }
        }
    ]
# ===============================================================

def check_and_alert(bot: Bot):
    new_tokens = get_new_tokens()
    for token in new_tokens:
        ca = token["contract"]
        if ca in seen_tokens:
            continue

        if (
            token["liquidity"] >= FILTERS["liquidity"]
            and token["market_cap"] >= FILTERS["market_cap"]
            and token["holders"] >= FILTERS["holders"]
            and token["fees_paid"] >= FILTERS["fees_paid"]
        ):
            send_alert(bot, token)
            seen_tokens.add(ca)

def send_alert(bot: Bot, token):
    name = token["name"]
    symbol = token["symbol"]
    text = (
        f"🚀 <b>New Token Found!</b>\n\n"
        f"💰 <b>Name:</b> ${symbol} ({name})\n"
        f"💧 <b>Liquidity:</b> ${token['liquidity']}\n"
        f"📈 <b>Market Cap:</b> ${token['market_cap']}\n"
        f"👥 <b>Holders:</b> {token['holders']}\n"
        f"⚙️ <b>Fees Paid:</b> {token['fees_paid']} SOL\n\n"
        f"🔗 <b>Contract:</b> <code>{token['contract']}</code>"
    )

    keyboard = [
        [
            InlineKeyboardButton("🌐 Pump.fun", url=token["pumpfun_link"]),
            InlineKeyboardButton("📊 Chart", url="https://dexscreener.com"),
            InlineKeyboardButton("🛒 Buy", url="https://jup.ag/")
        ]
    ]
    if token["socials"]:
        for name, link in token["socials"].items():
            keyboard.append([InlineKeyboardButton(f"{name.title()}", url=link)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=YOUR_TELEGRAM_ID,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

def status(update: Update, context: CallbackContext):
    status_text = (
        "<b>🔍 Current Filters:</b>\n"
        f"💧 Liquidity > ${FILTERS['liquidity']}\n"
        f"📈 Market Cap > ${FILTERS['market_cap']}\n"
        f"👥 Holders > {FILTERS['holders']}\n"
        f"⚙️ Fees Paid > {FILTERS['fees_paid']} SOL"
    )
    update.message.reply_text(status_text, parse_mode="HTML")

def main():
    bot = Bot(token=BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    logging.info("Bot started...")

    while True:
        check_and_alert(bot)
        time.sleep(15)  # check every 15 seconds

if __name__ == "__main__":
    main()
