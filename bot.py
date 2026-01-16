import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Ambil Config dari Railway Variables
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
# Pastikan ADMIN_ID adalah angka, bukan teks
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Filter agar hanya kamu yang bisa pakai
    if update.effective_user.id != ADMIN_ID:
        return 

    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Sedang memproses video Wan 2.1... (Saldo $10 Oke)")

    try:
        # Gunakan jalur model yang benar
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
        await update.message.reply_text(f"❌ Error saat proses: {str(e)}")

def main():
    if not TOKEN_TELEGRAM or not FAL_KEY:
        print("Error: Variabel TELEGRAM_TOKEN atau FAL_KEY kosong!")
        return

    # Inisialisasi bot dengan drop_pending_updates agar tidak antre pesan lama
    app = Application.builder().token(TOKEN_TELEGRAM).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Wan 2.1 Online & Menunggu Prompt...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
