import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Ambil Config dari Railway Variables ---
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
ADMIN_ID = 1788047490 # GANTI dengan ID kamu (dari @userinfobot)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pastikan hanya kamu yang bisa pakai
    if update.effective_user.id != ADMIN_ID:
        return 

    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Sedang memproses video Wan 2.1... (Saldo $10 Oke)")

    try:
        # JALUR MODEL TERBARU & BENAR
        handler = await fal_client.submit_async(
            "fal-ai/wan-video/v2.1/t2v-14b", 
            arguments={
                "prompt": prompt,
                "aspect_ratio": "9:16", # Sesuai keinginanmu untuk Shorts/TikTok
                "num_frames": 81
            }
        )
        
        result = await handler.get()
        video_url = result['video']['url']

        await update.message.reply_video(
            video=video_url, 
            caption=f"✅ Video Celia Selesai!\nPrompt: {prompt}"
        )
        await status_msg.delete()

    except Exception as e:
        await update.message.reply_text(f"❌ Error Detail: {str(e)}")

def main():
    app = Application.builder().token(TOKEN_TELEGRAM).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Wan 2.1 Aktif & Terkunci...")
    # Menghapus pesan lama agar tidak terjadi Conflict lagi
    app.run_polling(drop_pending_updates=True) 

if __name__ == "__main__":
    main()

