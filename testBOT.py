import telebot
from telebot import types
import io
import random


TOKEN = "5399350051:AAEemaHyed5a_BwaDyHqAnn3YTy1L0nwrPM"

words = []
helpwords = []

bot = telebot.TeleBot(TOKEN,parse_mode=None)

@bot.message_handler(commands='start')
def send_welcome(message):
	bot.reply_to(message, "You've started the bot")
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	
	itembthelp = types.KeyboardButton('/help')
	
	markup.row(itembthelp)
	
	bot.send_message(message.chat.id, "Choose one option:")

# @bot.message_handler(commands='stop')
# def stop_bot(message):
# 	bot.reply_to(message,"You've stopped the bot")
# 	bot.stop_bot()

@bot.message_handler(commands='help')
def help_bot(message):
	bot.send_message(chat_id=message.chat.id,text=f'''/start - Start the bot
/story - Create a story with database of words (min 100 unique words required)
/add - Add list of words (which were read) to database (Automatically add when length is over 512 words) 
/count - Show count of words in database
/database - Sends a db.txt with all words in db''')


@bot.message_handler(commands='count')
def count_word_bot(message):
	count = 0
	with io.open('db.txt','r',encoding="utf-8") as f:
			lines = f.readlines()			
			allLinesInText = str(lines).__str__().replace('[','').replace(']','').replace(',','').replace('"','').replace("'",'')
			allLinesInText.replace("\r"," ").replace("\n"," ")
			allLinesInText.strip()
			newWords = allLinesInText.split(" ")
			if newWords[0] == "" or newWords[0] == " " :
				count=0
			else:
				count = len(newWords)
			f.close()
	bot.send_message(chat_id=message.chat.id,text = f'{count}')

@bot.message_handler(commands="add")
def add_db_bot(message):
	

	with io.open('db.txt','r', encoding="utf-8") as f:
		lines = f.readlines()
		
		allLinesInText = str(lines).__str__().replace('[','').replace(']','').replace(',','').replace('"','').replace("'",'')
		allLinesInText.replace("\r"," ").replace("\n"," ")
		allLinesInText.strip()
		newWords = allLinesInText.split(" ")

		helpNewWords = str(newWords).__str__().replace('[','').replace(']','').replace(',','').replace('"','').replace("'",'')

		finalText=f'{helpNewWords} '

		for i in range(0,len(words)):
			if words[i] not in newWords:
				finalText+= f"{words[i]} "
		finalText = finalText.strip()
		with io.open("db.txt",'w',encoding="utf-8") as f:
				f.write(f"{finalText}")
				f.close()	
	words.clear()


@bot.message_handler(commands="database")
def db_bot(message):
	length = []
	with io.open("db.txt","r") as file:
		length = file.readlines()
		file.close()

	with open("db.txt", "rb") as file:
		if (length[0][0]==""):
			bot.send_message(chat_id=message.chat.id,text="База слов пустая")
			file.close()
		else:
			bot.send_document(chat_id=message.chat.id, document=file)
			bot.send_message(chat_id=message.chat.id,text="База слов успешно скинута")
			file.close()
	
	



@bot.message_handler(commands='clearBASErnBTWjustDOitMC')
def clear_db(message):

	

	with io.open('db.txt','a') as f:
		with io.open('db.txt','w') as f:
			f.write(f'')
	f.close()
	bot.send_message(chat_id=message.chat.id,text=f'База слов удалена успешно')

@bot.message_handler(commands='story')
def story_bot(message):
	minNum = 100
	count = 0
	story = ""
	with io.open('db.txt','r',encoding="utf-8") as f:
		lines = f.readlines()
		
		allLinesInText = str(lines).__str__().replace('[','').replace(']','').replace(',','').replace('"','').replace("'",'')
		allLinesInText.replace("\r"," ").replace("\n"," ")
		allLinesInText.strip()
		newWords = allLinesInText.split(" ")
		count = len(newWords)
		
		if count <= minNum:
			bot.send_message(chat_id=message.chat.id,text=f'База слов достаточно мала ({count} < {minNum+1})')
		else:
			for i in range (0,random.randint(10,(40)*(random.randint(1,3)))):
				if i%2 != 0:
					while True:
						word = str(newWords[random.randint(0,count-1)])
						if (len(word)<5):
							story+=f'{word} '
							break
				else:
					while True:
						word = str(newWords[random.randint(0,count-1)])
						if len(word)>5:
							story+=f'{word} '
							break
		f.close()
	
		bot.send_message(chat_id=message.chat.id,text=f'{story}')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	try:
		newString = message.text
		helpnewString = newString.replace("\n","").replace("\r","").replace("}","").replace("{","").replace("@","").replace(",","").replace(".","").replace("!","").replace("?","").replace("/","").replace(";","").replace("'","").replace('"',"").replace(':',"").replace('%',"").replace('^',"").replace('*',"").replace('-',"").replace('=',"").replace('+',"").replace('_',"").replace('(',"").replace(')',"").replace("\\","")
		helpnewString.strip()
		arr = helpnewString.split(" ")			
		for i in range (0,len(arr)):
			if(arr[i] not in words):
				if len(arr[i]<10):
					words.append(arr[i])	


		if len(words) >=200:
				with io.open('db.txt','r', encoding="utf-8") as f:
					lines = f.readlines()
					
					allLinesInText = str(lines).__str__().replace('[','').replace(']','').replace(',','').replace('"','').replace("'",'')
					allLinesInText.replace("\r"," ").replace("\n"," ")
					allLinesInText.strip()
					newWords = allLinesInText.split(" ")

					helpNewWords = str(newWords).__str__().replace('[','').replace(']','').replace(',','').replace('"','').replace("'",'')

					finalText=f'{helpNewWords} '

					for i in range(0,len(words)):
						if words[i] not in newWords:
							finalText+= f"{words[i]} "
					finalText = finalText.strip()
					with io.open("db.txt",'w',encoding="utf-8") as f:
							f.write(f"{finalText}")
							f.close()	
				words.clear()
	except:
		pass



		
		
bot.infinity_polling()