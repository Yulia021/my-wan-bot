import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Ambil Config dari Railway Variables
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
# Pastikan ADMIN_ID adalah angka di Variables Railway
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return 

    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Memproses video Celia (Wan 2.1)...")

    try:
        # Jalur model yang benar untuk versi 14B
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

        await update.message.reply_video(video=video_url, caption=f"✅ Selesai!\nPrompt: {prompt}")
        await status_msg.delete()

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    if not TOKEN_TELEGRAM or not FAL_KEY:
        print("Error: Variabel di Railway belum lengkap!")
        return

    # Inisialisasi dengan drop_pending_updates untuk menghindari Conflict kembali
    app = Application.builder().token(TOKEN_TELEGRAM).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Wan 2.1 Aktif & Terkunci...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
