import os
import asyncio
import fal_client
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    
    prompt = update.message.text
    status = await update.message.reply_text("🚀 Sedang memproses video Celia (Wan 2.1)...")

    try:
        handler = await fal_client.submit_async(
            "fal-ai/wan-video/v2.1/t2v-14b",
            arguments={"prompt": prompt, "aspect_ratio": "9:16", "num_frames": 81}
        )
        result = await handler.get()
        await update.message.reply_video(video=result['video']['url'], caption=f"✅ Selesai!\nPrompt: {prompt}")
        await status.delete()
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    # Menggunakan koneksi yang lebih 'galak' untuk mengusir Conflict
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot Celia Online...")
    # 'drop_pending_updates' membuang pesan lama, 'close_loop' memastikan sesi bersih
    app.run_polling(drop_pending_updates=True, close_loop=True)

if __name__ == "__main__":
    main()
