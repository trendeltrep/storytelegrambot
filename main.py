import os
from cgitb import text
import telebot
from telebot import types
import io
import random
from random import randint
import requests
import json
import data, tools

with open("config.json", 'r') as file:
    cfg = json.load(file)

TOKEN = cfg["token"]
api_key = cfg["api_key"]

words = []
helpwords = []

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands='start')
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_btn_help = types.KeyboardButton('/help')
    markup.row(item_btn_help)


# @bot.message_handler(commands='stop')
# def stop_bot(message):
# 	bot.reply_to(message,"You've stopped the bot")
# 	bot.stop_bot()

@bot.message_handler(commands='request')
def request_bot(message):
    text = "ФІвлрпвпиівта"
    r = requests.get(
        f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang=ru-en&text={text}")
    answer = r.json()["def"][0]["pos"]
    bot.send_message(chat_id=message.chat.id, text=str(answer))


@bot.message_handler(commands='help')
def help_bot(message):
    bot.send_message(chat_id=message.chat.id, text=data.help_message)


@bot.message_handler(commands='count')
def count_word_bot(message):
    with open('db.txt', 'r') as f:
        lines = f.read()
    words = tools.more_replace(lines, ["\n", "\r"], " ").strip().split(" ")
    # Остаються вопросы, но я пожалуй это трогать не буду))))
    if words[0] == "" or words[0] == " ":
        count = 0
    else:
        count = len(newWords)
    bot.send_message(chat_id=message.chat.id, text=f'{count}')


@bot.message_handler(commands="add")
def add_db_bot(message):
    global words
    with open("db.txt", 'wr') as file:
        saved_words = file.read().split()
        saved_words += list(filter(lambda w: w not in words, words))
        file.write(" ".join(saved_words))
    words.clear()


@bot.message_handler(commands="database")
def db_bot(message):
    with open("db.txt", "r") as file:
        length = file.read()
        if len(length) == 0:
            bot.send_message(chat_id=message.chat.id, text="База слов пустая")
        else:
            bot.send_document(chat_id=message.chat.id, document=file)
            bot.send_message(chat_id=message.chat.id, text="База слов успешно скинута")


@bot.message_handler(commands='clearBASErnBTWjustDOitMC')
def clear_db(message):
    os.remove("db.txt")
    bot.send_message(chat_id=message.chat.id, text=f'База слов удалена успешно')


@bot.message_handler(commands='story')
def story_bot(message):
    minNum = 100
    with open('db.txt', 'r') as f:
        words = f.read().split()
    if len(words) <= minNum:
        bot.send_message(chat_id=message.chat.id, text=f'База слов достаточно мала ({len(words)} < {minNum + 1})')
        return

    message_len = range(10, randint(20, 30 * randint(1, 3)))
    short = list(filter(lambda w: len(w) < 5, words))
    long = list(filter(lambda w: len(w) > 5, words))
    story = ""
    for i in message_len:
        if i % 2 != 0:
            story += random.choice(short)
        else:
            story += random.choice(long)

    bot.send_message(chat_id=message.chat.id, text=story)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        newString = message.text.lower()
        # Переписать на генерацию символов из ascii
        helpnewString = tools.more_replace(newString,
                            ["\n", "\r", "}", "{", "@", ",", ".", "!","?", "/", ";",
                             "'", '"', ":", "%", "^", "*", "-", "=", "+", "_", "(", ".com", "https", ")", "\\"],
                                           "")
        helpnewString.strip()
        arr = helpnewString.split(" ")
        for i in range(0, len(arr)):
            if (arr[i] not in words and len(arr[i]) < 15):
                r = requests.get(
                    f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang=ru-en&text={arr[i]}")
                answer = r.json()
                if len(answer["def"]) != 0:
                    if "pos" in answer["def"][0]:
                        words.append([arr[i], answer["def"][0]["pos"]])

                    # words.append(arr[i])
        if len(words) >= 50:
            with io.open('db.txt', 'r', encoding="utf-8") as f:
                lines = f.readlines()
                allLinesInText = str(lines).__str__().replace('[', '').replace(']', '').replace(',', ';').replace('"',
                                                                                                                  '').replace(
                    "'", '')
                allLinesInText.replace("\r", " ").replace("\n", " ")
                allLinesInText.strip()
                newWords = allLinesInText.split(" ")
                helpNewWords = str(newWords).__str__().replace('[', '').replace(']', '').replace(',', ';').replace('"',
                                                                                                                   '').replace(
                    "'", '')
                finalText = f'{helpNewWords} '
                for i in range(0, len(words)):
                    if words[i][0] not in newWords:
                        finalText += f"{words[i][0]};{words[i][1]} "
                finalText = finalText.strip()
                with io.open("db.txt", 'w', encoding="utf-8") as f:
                    f.write(f"{finalText}")
                    f.close()
            words.clear()
    except:
        pass


bot.infinity_polling()
