import telebot
import config
import asyncio
import aioschedule
from random import choice

bot = telebot.TeleBot(config.Token)

class TeleBot:
    def __init__(self, token=config.Token):
        self.bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def message_start(message):
    bot.reply_to(message, 'Привет!')
    bot.send_message(message.chat.id, 'тестовое сообщение')
    bot.send_message(message)

async def beep(chat_id) -> None:
    await bot.send_message(chat_id, text='Биип!')
    aioschedule.clear(chat_id)  


@bot.message_handler(commands=['set'])
async def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        aioschedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        await bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    aioschedule.clean(message.chat.id)


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())

bot.infinity_polling()