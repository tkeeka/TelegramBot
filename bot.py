import os
import asyncio
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

# Konfigurasi logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Ganti dengan daftar ID admin grup Anda
ADMIN_IDS = [7545312621, 1795847740, 6477737453, 1684445011, 5664152176]
TARGET_GROUP = -1002404016137

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Gunakan @crew untuk melaporkan sesuatu kepada staf grup.")

# Fungsi untuk menangani laporan @crew
async def crew_command(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.message.chat

    if user.id in ADMIN_IDS:
        await update.message.reply_text("⚠️ Perintah @crew tidak dapat digunakan oleh admin.")
        return

    report_message = (
        f"🚨 <b>Laporan Baru!</b>\n\n"
        f"<b>Pengguna:</b> {user.mention_html()}\n"
        f"<b>Grup:</b> {chat.title}\n"
        f"<b>ID Grup:</b> {chat.id}\n"
        f"\nPesan: {update.message.text}"
    )

    await context.bot.send_message(
        chat_id=TARGET_GROUP,
        text=report_message,
        parse_mode=ParseMode.HTML
    )

    await update.message.reply_text(
        "✅ Laporan Anda telah dikirim kepada staf. Mohon tunggu respon mereka."
    )

async def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("Token bot tidak ditemukan di .env")

    application = (
        Application.builder()
        .token(TOKEN)
        .read_timeout(120)
        .connect_timeout(120)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Regex(r"@crew"),
            crew_command
        )
    )

    logging.info("Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    from asyncio import get_event_loop

    # Terapkan nest_asyncio untuk menghindari konflik event loop
    nest_asyncio.apply()

    try:
        # Gunakan loop aktif jika ada
        loop = get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logging.warning("Bot dihentikan oleh pengguna.")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
