import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Ambil token dari sistem (untuk keamanan saat di cloud)
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")

# Fungsi saat user klik /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Saya adalah Bot Wan 2.1.\n\n"
        "Kirimkan prompt teks apa saja, dan saya akan buatkan videonya."
    )

# Fungsi untuk memproses video
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    
    # Kirim pesan awal agar user tahu bot sedang bekerja
    status_msg = await update.message.reply_text("⏳ Sedang memproses video Wan 2.1... (Biasanya 30-60 detik)")

    try:
        # Panggil API Fal.ai
        # Kita pakai model wan/v2.1/t2v (Text to Video)
        handler = await fal_client.submit_async(
            "fal-ai/wan/v2.1/t2v",
            arguments={
                "prompt": prompt,
                "aspect_ratio": "16:9", # Kamu bisa ganti ke 9:16 untuk TikTok
                "num_frames": 81        # Standar durasi Wan 2.1
            }
        )
        
        result = await handler.get()
        video_url = result['video']['url']

        # Kirim video ke user
        await update.message.reply_video(
            video=video_url, 
            caption=f"✅ Berhasil!\nPrompt: {prompt}"
        )
        
        # Hapus pesan status "sedang memproses"
        await status_msg.delete()

    except Exception as e:
        await update.message.reply_text(f"❌ Maaf, terjadi kesalahan: {str(e)}")

def main():
    # Cek apakah token sudah diisi
    if not TOKEN_TELEGRAM or not FAL_KEY:
        print("Error: TOKEN_TELEGRAM atau FAL_KEY belum diatur di Environment Variables!")
        return

    # Jalankan Bot
    app = Application.builder().token(TOKEN_TELEGRAM).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Wan 2.1 menyala...")
    app.run_polling()

if __name__ == "__main__":
    main()
