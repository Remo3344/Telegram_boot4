from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "ضع_توكن_البوت_هنا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك، أنا بوت الإدارة العربي.\nاكتب /الاوامر لمعرفة جميع الأوامر."
    )

async def الاوامر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 أوامر البوت:\n"
        "/رفع\n"
        "/تنزيل\n"
        "/كتم\n"
        "/حظر\n"
        "/قفل\n"
        "/فتح\n"
        "/تنظيف"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("الاوامر", الاوامر))

print("البوت يعمل...")
app.run_polling()
