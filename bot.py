import os
import yt_dlp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ضع التوكن الخاص بك هنا بين علامتي التنصيص
TOKEN = '8575028616:AAG7dopQ2W-gEH0Bb6pWGFJ_NOHuJ_DSnLw'

async def start(update, context):
    await update.message.reply_text('أهلاً! أنا بوت التحميل، أرسل الرابط وسأقوم بتحميله.')

async def handle_message(update, context):
    url = update.message.text
    keyboard = [[InlineKeyboardButton("📥 تحميل", callback_data=url)]]
    await update.message.reply_text('اضغط للتحميل:', reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="⏳ جاري التحميل...")
    
    try:
        url = query.data
        ydl_opts = {
    'outtmpl': 'video.mp4',
    'format': 'best',
    'quiet': True,
    'no_warnings': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await query.message.reply_video(video=open('video.mp4', 'rb'))
        await query.edit_message_text(text="✅ تم الإرسال!")
    except Exception as e:
        await query.edit_message_text(text=f"❌ خطأ: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handlers([CommandHandler("start", start), MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message), CallbackQueryHandler(button_click)])
    app.run_polling()
