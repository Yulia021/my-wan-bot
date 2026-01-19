import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Ambil Config dari Railway Variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
# Ambil ADMIN_ID sebagai integer, berikan default 0 jika kosong
ADMIN_ID_STR = os.getenv("ADMIN_ID", "0")
ADMIN_ID = int(ADMIN_ID_STR) if ADMIN_ID_STR.isdigit() else 0

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Filter ADMIN_ID
    if update.effective_user.id != ADMIN_ID:
        return 

    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Sedang memproses video Celia di Wan 2.1... (Saldo $10 Oke)")

    try:
        # Jalur model yang sudah kamu perbaiki di GitHub (image_074b20.png)
        handler = await fal_client.submit_async(
            "fal-ai/wan-video/v2.1/t2v-14b",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "9:16",
                "num_frames": 81
            }
        )
        
        result = await handler.get()
        video_url = result['video']['url']

        await update.message.reply_video(video=video_url, caption=f"✅ Berhasil!\nPrompt: {prompt}")
        await status_msg.delete()

    except Exception as e:
        await update.message.reply_text(f"❌ Error Fal.ai: {str(e)}")

def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_TOKEN tidak ditemukan di Variables Railway!")
        return

    # Inisialisasi bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Celia Online...")
    # Gunakan drop_pending_updates agar tidak Conflict lagi
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
