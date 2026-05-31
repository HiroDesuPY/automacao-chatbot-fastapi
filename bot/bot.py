from telebot.async_telebot import AsyncTeleBot
from config import TELEGRAMBOT_API
from services.pergunta_ia import IA
import asyncio

bot = AsyncTeleBot(TELEGRAMBOT_API)







@bot.message_handler(func=lambda message: True)
async def echo(message):
    sessions_id = message.chat.id
    pergunta = message.text

    ia = IA(sessions_id=str(sessions_id))

    await ia.prompt(pergunta)
    resposta = await ia.answer()

    await bot.send_message(message.chat.id, resposta)





def start_bot():
    print("Bot iniciado...")
    asyncio.run(bot.infinity_polling())