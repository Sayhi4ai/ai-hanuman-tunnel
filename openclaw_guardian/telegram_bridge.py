import asyncio
import yaml
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "telegram-openclaw-guardian.yaml"

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

BOT_TOKEN = cfg["telegram"]["bot_token"]
CHAT_ID = cfg["telegram"]["chat"]["id"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OpenClawGuardian is listening. Send me a task.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = f"You said: {text}\n(Guardian will later route this to Gemma4/OpenClaw.)"
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
