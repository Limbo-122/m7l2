import telebot
from config import TOKEN, API_KEY, SECRET_KEY
from logic import Text2ImageAPI, text2img
from random import randint

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для генерации картинок. Напиши мне команду /prompt < текст запроса>")


@bot.message_handler(commands=['prompt'])
def make_img(message):
    prompt_text = telebot.util.extract_arguments(message.text)
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt_text, model_id)
    images = api.check_generation(uuid)[0]

    file_path = f'image_{randint(1000000, 10000000)}.jpg'
    img = text2img(images, file_path)
    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.infinity_polling()
