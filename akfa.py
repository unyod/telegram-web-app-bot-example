import telebot
from telebot import types

TOKEN = "8728441274:AAHKR9r4rfi3HT6MYXBc6defb6BM1kvgDOU"
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("🚪 Eshik", callback_data="eshik")
    btn2 = types.InlineKeyboardButton("🪟 Oyna", callback_data="oyna")
    btn3 = types.InlineKeyboardButton("📏 Jaluzi", callback_data="jaluzi")

    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(
        message.chat.id,
        "Nimani hisoblamoqchisiz?",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_data[call.from_user.id] = call.data

    bot.send_message(
        call.message.chat.id,
        f"{call.data.title()} uchun:\n\n"
        "eni boyi 1m²_narxi\n\n"
        "Misol:\n"
        "1.5 2 300000"
    )

@bot.message_handler(func=lambda m: True)
def calculate(message):
    try:
        if message.from_user.id not in user_data:
            bot.reply_to(message, "/start ni bosing.")
            return

        turi = user_data[message.from_user.id]

        eni, boyi, narx = map(float, message.text.split())

        maydon = eni * boyi
        jami = maydon * narx

        emoji = {
            "eshik": "🚪",
            "oyna": "🪟",
            "jaluzi": "📏"
        }

        natija = (
            f"{emoji[turi]} {turi.title()}\n\n"
            f"📐 Maydon: {maydon:.2f} m²\n"
            f"💰 Jami narx: {jami:,.0f} so'm"
        )

        bot.reply_to(message, natija)

    except Exception:
        bot.reply_to(
            message,
            "Xato format!\n\nMisol:\n1.5 2 300000"
        )

print("Bot ishga tushdi...")
bot.infinity_polling()
