import telebot 
from config import token
from logic import Pokemon
import requests
from io import BytesIO

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        img_url, info_text = pokemon.get_info()
        
        response = requests.get(img_url)
        photo = BytesIO(response.content)
        photo.name = 'pokemon.png'
        
        bot.send_photo(message.chat.id, photo, caption=info_text)
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
            bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['info'])
def info(message):
    # Если сообщение написано в ответ на чьё-то сообщение
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username

        # Проверяем, есть ли у этого пользователя покемон
        if username in Pokemon.pokemons.keys():
            pok = Pokemon.pokemons[username]
            img_url = pok.img_url
            info_text = pok.info()

            # отправляем фото и инфу
            if img_url:
                response = requests.get(img_url)
                photo = BytesIO(response.content)
                photo.name = 'pokemon.png'
                bot.send_photo(message.chat.id, photo, caption=info_text)
            else:
                bot.send_message(message.chat.id, info_text)
        else:
            bot.reply_to(message, f"У @{username} ещё нет покемона!")

    # Если не ответ — показываем информацию о своём покемоне
    else:
        username = message.from_user.username
        if username in Pokemon.pokemons.keys():
            pok = Pokemon.pokemons[username]
            img_url = pok.img_url
            info_text = pok.info()

            if img_url:
                response = requests.get(img_url)
                photo = BytesIO(response.content)
                photo.name = 'pokemon.png'
                bot.send_photo(message.chat.id, photo, caption=info_text)
            else:
                bot.send_message(message.chat.id, info_text)
        else:
            bot.reply_to(message, "У тебя ещё нет покемона! Создай его с помощью команды /go")


bot.infinity_polling(none_stop=True)