from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from functools import wraps

 TOKEN = "8982634790:AAFIJpOF3Y3Q5Jc6YsFy5qYo5oapX5quaA8" 

# دالة حماية: تمنع الأعضاء العاديين من استخدام الأوامر الإدارية
def admin_only(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        chat = update.effective_chat
        user_id = update.effective_user.id
        
        # التأكد أن الأمر يُنفذ داخل مجموعة وليس في الخاص
        if chat.type in ["group", "supergroup"]:
            member = await context.bot.get_chat_member(chat_id=chat.id, user_id=user_id)
            # السماح فقط لمالك المجموعة أو المشرفين
            if member.status in ["administrator", "creator"]:
                return await func(update, context, *args, **kwargs)
            else:
                await update.message.reply_text("⚠️ عذراً، هذا الأمر مخصص للمشرفين فقط!")
                return
        else:
            await update.message.reply_text("❌ هذا الأمر يعمل داخل المجموعات فقط.")
            return
    return wrapped

# دالة الترحيب /start (تستقبل أمر إنجليزي فتعمل بدون مشاكل)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك، أنا بوت الإدارة العربي.\nاكتب /الاوامر لمعرفة جميع الأوامر."
    )

# دالة عرض الأوامر
async def الاوامر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 أوامر البوت الإدارية:\n"
        "/رفع - لرفع عضو كمشرف (بالرد)\n"
        "/تنزيل - لتنزيل مشرف لعضو (بالرد)\n"
        "/كتم - لكتم عضو في المجموعة (بالرد)\n"
        "/حظر - لحظر عضو من المجموعة (بالرد)\n"
        "/قفل - لقفل إرسال الميديا والروابط\n"
        "/فتح - لفتح المجموعة للجميع\n"
        "/تنظيف - لحذف آخر 10 رسائل"
    )

# أمر الحظر (يتطلب الرد على رسالة العضو)
@admin_only
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        await update.message.reply_text("🚫 تم حظر العضو بنجاح.")
    else:
        await update.message.reply_text("⚠️ يجب أن ترد على رسالة العضو المراد حظره.")

# أمر الكتم (يتطلب الرد على رسالة العضو)
@admin_only
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user_id, permissions=permissions)
        await update.message.reply_text("🔇 تم كتم العضو بنجاح.")
    else:
        await update.message.reply_text("⚠️ يجب أن ترد على رسالة العضو المراد كتمه.")

# أمر الرفع كمشرف (يتطلب الرد على رسالة العضو)
@admin_only
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id, 
            user_id=user_id,
            can_manage_chat=True,
            can_delete_messages=True,
            can_restrict_members=True
        )
        await update.message.reply_text("👑 تم رفع العضو كمشرف بالصلاحيات الأساسية.")
    else:
        await update.message.reply_text("⚠️ يجب أن ترد على رسالة العضو لرفعه.")

# أمر التنزيل من الإشراف (يتطلب الرد على رسالة المشرف)
@admin_only
async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id, 
            user_id=user_id,
            can_manage_chat=False,
            can_delete_messages=False,
            can_restrict_members=False
        )
        await update.message.reply_text("👤 تم إلغاء صلاحيات الإشراف وعاد العضو لرتبة طبيعية.")
    else:
        await update.message.reply_text("⚠️ يجب أن ترد على رسالة المشرف لتنزيله.")

# أمر قفل الميديا والروابط
@admin_only
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permissions = ChatPermissions(
        can_send_messages=True, 
        can_send_media_messages=False, 
        can_send_other_messages=False, 
        can_add_web_page_previews=False
    )
    await context.bot.set_chat_permissions(chat_id=update.effective_chat.id, permissions=permissions)
    await update.message.reply_text("🔒 تم قفل إرسال الوسائط والروابط للأعضاء العاديين.")

# أمر فتح المجموعة للجميع
@admin_only
async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permissions = ChatPermissions(
        can_send_messages=True, 
        can_send_media_messages=True, 
        can_send_other_messages=True, 
        can_add_web_page_previews=True
    )
    await context.bot.set_chat_permissions(chat_id=update.effective_chat.id, permissions=permissions)
    await update.message.reply_text("🔓 تم فتح المجموعة بالكامل لجميع الأعضاء.")

# أمر تنظيف الرسائل القديمة
@admin_only
async def clean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.message_id
    deleted_count = 0
    for i in range(11):
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id - i)
            deleted_count += 1
        except Exception:
            continue
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🧹 تم تنظيف الرسائل بنجاح.")

# إعداد التطبيق والموجهات
app = Application.builder().token(TOKEN).build()

# دالة start تعمل كأمر عادي لأنه بالإنجليزية
app.add_handler(CommandHandler("start", start))

# تم استبدال CommandHandler بـ MessageHandler مضاف له فلاتر ذكية لقراءة الكلمات العربية بوجود / أو بدونه
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?الاوامر$"), الاوامر))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?رفع$"), promote))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?تنزيل$"), demote))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?كتم$"), mute))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?حظر$"), ban))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?قفل$"), lock))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?فتح$"), unlock))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/?تنظيف$"), clean))

print("البوت يعمل الآن بنجاح وبدون أي أخطاء...")
app.run_polling()
