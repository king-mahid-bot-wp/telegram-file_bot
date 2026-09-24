import logging
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("8797201665:AAGVaveNjuI3jHt32PJWJMrHryAQNvgEyac")
ADMIN_ID = int(os.getenv("7602828824"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================
# START MENU
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📤 Upload File", callback_data="upload")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
    ]

    await update.message.reply_text(
        "🤖 *Premium File Upload Bot*\n\n"
        "📁 Photo, Video অথবা Document পাঠাতে পারো।\n"
        "📤 Upload করতে নিচের button ব্যবহার করো.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "upload":
        await query.message.reply_text(
            "📤 এখন Photo / Video / Document পাঠাও।\n\n"
            "আমি সেটা Admin-এর কাছে পাঠিয়ে দেব।"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ *Help*\n\n"
            "• Photo পাঠানো যাবে\n"
            "• Video পাঠানো যাবে\n"
            "• Document/File পাঠানো যাবে\n\n"
            "Upload শেষে confirmation পাবে।",
            parse_mode="Markdown",
        )


# =========================
# FILE HANDLER
# =========================
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    try:
        user = update.effective_user
        user_name = user.full_name if user else "Unknown User"

        caption = f"📥 *New Upload*\n👤 User: {user_name}"

        # Photo
        if message.photo:
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=message.photo[-1].file_id,
                caption=caption,
                parse_mode="Markdown",
            )

        # Video
        elif message.video:
            name = message.video.file_name or "Video"
            await context.bot.send_video(
                chat_id=ADMIN_ID,
                video=message.video.file_id,
                caption=f"{caption}\n🎬 File: {name}",
                parse_mode="Markdown",
            )

        # Document
        elif message.document:
            name = message.document.file_name or "Unknown File"
            await context.bot.send_document(
                chat_id=ADMIN_ID,
                document=message.document.file_id,
                caption=f"{caption}\n📁 File: {name}",
                parse_mode="Markdown",
            )

        else:
            await message.reply_text("❌ এই ধরনের file support করে না।")
            return

        await message.reply_text(
            "✅ *Upload Successful!*\n\n"
            "তোমার file Admin-এর কাছে পাঠানো হয়েছে।",
            parse_mode="Markdown",
        )

    except Exception:
        logging.exception("Upload error")
        await message.reply_text("❌ Upload failed. আবার চেষ্টা করো।")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling update:", exc_info=context.error)


def main():
    if BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("BOT_TOKEN সেট করো।")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.VIDEO | filters.Document.ALL,
            handle_file,
        )
    )
    app.add_error_handler(error_handler)

    print("🤖 Premium File Upload Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
