import requests
import telebot
import os

bot = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))
STRIPE_KEY = os.environ.get("STRIPE_TEST_KEY")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Send card like 4242424242424242|12|34|123")

@bot.message_handler(func=lambda m: True)
def card(m):
    try:
        num, mm, yy, cvv = m.text.strip().split("|")
        r = requests.post("https://api.stripe.com/v1/tokens", data={
            "card[number]": num,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv,
            "key": STRIPE_KEY
        })
        j = r.json()
        if "id" in j:
            bot.reply_to(m, f"✅ Token: `{j['id']}`", parse_mode="Markdown")
        else:
            bot.reply_to(m, f"❌ Error: {j.get('error', {}).get('message', 'Unknown')}")
    except:
        bot.reply_to(m, "❌ Format error. Use: `card|mm|yy|cvv`")

bot.polling()
