import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIG ---
BOT_TOKEN = "8360637093:AAHCab3qG9I0GGS6dM40ssBDwGlpk29tMKE"

# सिर्फ admins के IDs यहाँ डालो
ADMINS = [6135948216, 7607010245]  

LINKS_FILE = "links.json"


# --- LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# --- LINKS STORAGE SYSTEM ---
def load_links():
    try:
        with open(LINKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_links(links):
    with open(LINKS_FILE, "w") as f:
        json.dump(links, f)


# --- COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    links = load_links()

    if not links:
        await update.message.reply_text("⚠️ अभी कोई channel/group links सेट नहीं हैं।")
        return

    # Inline buttons
    keyboard = [[InlineKeyboardButton(f"📌 Link {i+1}", url=link)] for i, link in enumerate(links)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\n👉 नीचे दिए गए links को join करें:",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("❌ You are not allowed to use this command.")
        return

    await update.message.reply_text(
        "🛠 *Admin Commands:*\n\n"
        "/setlinks link1 link2 ... → Links सेट करो (max 5)\n"
        "/sendlinks → सबको links भेजो\n"
        "/help → ये help menu",
        parse_mode="Markdown"
    )


async def setlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("❌ You are not allowed to use this command.")
        return

    links = context.args
    if not links:
        await update.message.reply_text("⚠️ Usage: `/setlinks link1 link2 ...`", parse_mode="Markdown")
        return

    if len(links) > 5:
        await update.message.reply_text("❌ सिर्फ़ 5 links ही allow हैं।")
        return

    save_links(links)
    await update.message.reply_text("✅ Links successfully updated!")


async def sendlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("❌ You are not allowed to use this command.")
        return

    links = load_links()
    if not links:
        await update.message.reply_text("⚠️ अभी कोई links सेट नहीं हैं।")
        return

    keyboard = [[InlineKeyboardButton(f"📌 Link {i+1}", url=link)] for i, link in enumerate(links)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📢 Please join our channels/groups:",
        reply_markup=reply_markup,
    )


# --- MAIN ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setlinks", setlinks))
    app.add_handler(CommandHandler("sendlinks", sendlinks))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
