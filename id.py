


import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot API tokeningizni shu yerga kiriting
API_KEY = "5807873479:AAE9vuSJG-ju79uauqOGAJCsTvPkQKxr6TE"
ADMIN_ID = 5376652018  # Adminning Telegram ID'sini shu yerga kiriting

# Logging sozlamalari
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Foydalanuvchi ma'lumotlarini saqlash
user_data = {}

async def start(update: Update, context: CallbackContext):
    """ /start buyrug'iga javob beruvchi funksiya """
    user = update.effective_user
    user_data[user.id] = {"phone": None}

    keyboard = [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "📲 Iltimos, murojaat yuborish uchun telefon raqamingizni yuboring.",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: CallbackContext):
    """ Foydalanuvchi telefon raqamini yuborganda ishlaydi """
    user = update.effective_user
    contact = update.message.contact

    if contact and contact.user_id == user.id:
        user_data[user.id]["phone"] = contact.phone_number

        await update.message.reply_text(
            "✅ Raqamingiz qabul qilindi!\n\n"
            "📩 Endi o‘z murojaatingizni yozib yuborishingiz mumkin."
        )
    else:
        await update.message.reply_text("❌ Iltimos, o‘zingizning telefon raqamingizni yuboring.")

async def handle_message(update: Update, context: CallbackContext):
    """ Foydalanuvchi murojaatini qabul qiladi va adminga yuboradi """
    user = update.effective_user
    user_id = user.id

    if user_id not in user_data or not user_data[user_id]["phone"]:
        keyboard = [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        await update.message.reply_text(
            "❌ Murojaat yuborishdan oldin telefon raqamingizni yuboring.",
            reply_markup=reply_markup
        )
        return

    message_text = update.message.text
    phone_number = user_data[user_id]["phone"]

    admin_message = (
        f"📩 <b>Yangi murojaat</b>\n"
        f"👤 <b>Foydalanuvchi:</b> {user.full_name}\n"
        f"📞 <b>Telefon raqami:</b> {phone_number}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n\n"
        f"💬 <b>Murojaat:</b>\n{message_text}"
    )

    # Adminga yuborish
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="HTML")

    await update.message.reply_text("✅ Murojaatingiz qabul qilindi. Rahmat!")

def main():
    """ Botni ishga tushirish """
    app = Application.builder().token(API_KEY).build()

    # Buyruqlarni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
