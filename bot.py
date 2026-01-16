import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- KONFIGURASI ---
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
# GANTI angka di bawah ini dengan User ID kamu dari @userinfobot
ADMIN_ID = 1788047490 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah yang klik start itu kamu atau orang asing
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Akses ditolak. Bot ini hanya untuk pemilik.")
        return
        
    await update.message.reply_text(
        "👋 Halo! Bot Wan 2.1 untuk Celia AI siap digunakan.\n\n"
        "Kirimkan prompt untuk membuat video."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gembok keamanan agar saldo API aman
    if update.effective_user.id != ADMIN_ID:
        return 

    prompt = update.message.text
    status_msg = await update.message.reply_text("⏳ Sedang memproses video Wan 2.1... (30-60 detik)")

    try:
        # Panggil API Fal.ai
            handler = await fal_client.submit_async(
            "fal-ai/wan-video/v2.1/t2v-14b", # Jalur model Wan 2.1 terbaru
            arguments={
                "prompt": prompt,
                "aspect_ratio": "16:9", # Sesuaikan jika ingin 9:16 untuk YouTube Shorts
                "num_frames": 81
            }
        )
        
        result = await handler.get()
        video_url = result['video']['url']

        await update.message.reply_video(
            video=video_url, 
            caption=f"✅ Selesai!\nPrompt: {prompt}"
        )
        await status_msg.delete()

    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan: {str(e)}")

def main():
    if not TOKEN_TELEGRAM or not FAL_KEY:
        print("Error: Variabel lingkungan belum diatur!")
        return

    app = Application.builder().token(TOKEN_TELEGRAM).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Wan 2.1 menyala dan terkunci untuk satu user...")
    app.run_polling()

if __name__ == "__main__":
    main()


