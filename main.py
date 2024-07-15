from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from response_generator import generate_response
from gtts import gTTS
import os


def start(update, context):
    update.message.reply_text('Привет! Я Андрей, ваш финансовый советник. Задайте мне вопрос о любом активе.')


def handle_message(update, context):
    text = update.message.text.lower()
    ticker = text.split()[-1].upper()  # Предполагаем, что тикер всегда последнее слово
    response_text = generate_response(ticker)

    # Convert text to speech
    tts = gTTS(response_text, lang='ru')
    audio_path = f"{ticker}_response.ogg"
    tts.save(audio_path)

    # Send voice message
    context.bot.send_voice(chat_id=update.message.chat_id, voice=open(audio_path, 'rb'))

    # Remove the audio file after sending
    os.remove(audio_path)


if __name__ == '__main__':
    # Настройка и запуск Telegram-бота
    updater = Updater('ТВОЙ ТОКЕН', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
