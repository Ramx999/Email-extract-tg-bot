import re
import telebot

API_TOKEN = 'Your bot token'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def extract_credentials(message):
    text = message.text

    pattern = r'([a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com)):(\S+)|Email\s*:\s*([a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com))\s*Password\s*:\s*(\S+)'
    matches = re.findall(pattern, text)

    response = []
    for index, match in enumerate(matches, start=1):
        if match[0]:  # email:password format
            email, provider, password = match[0], match[1], match[2]
            response.append(f"{index}. Email: <code>{email}</code> \nPassword: <code>{password}</code>")
        elif match[3] and match[4]:  # direct email and password format
            email, password = match[3], match[4]
            response.append(f"{index}. Email: <code>{email}</code> \nPassword: <code>{password}</code>")

    if response:
        bot.reply_to(message, "\n\n".join(response), parse_mode='HTML')
    else:
        bot.reply_to(message, "No emails and passwords found.")

bot.polling()
