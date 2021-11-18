import telebot
from telebot import types
bot = telebot.TeleBot('BOT_TOKEN')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	msg = message.text
	id = message.from_user.id
	idstr=str(id)
	langu='RU'
	g=open(idstr+'.data', 'r')
	adata = g.read()
	if msg=="/start":
		g = open(idstr+'.data', 'w')
		g.write('00000001')
		g.close()
		keyboard = types.InlineKeyboardMarkup()
		key_en = types.InlineKeyboardButton(text='EN', callback_data='en')
		keyboard.add(key_en)
		key_ru = types.InlineKeyboardButton(text='RU', callback_data='ru')
		keyboard.add(key_ru)
		bot.send_message(message.from_user.id, text="Choose your language:", reply_markup=keyboard)
	if msg=='/bal' or msg=='/money':
		g=open(idstr+'.data', 'a')
		g.close()
		g=open(idstr+'.data', 'r')
		data = g.read()
		bal = data[:8]
		g.close()
		mes='Ваш текущий баланс: '+bal
		if data[8:] == 'EN':
			 mes='Your current balance: '+bal
		bot.send_message(id, mes)
	if msg=='/id':
		g=open(idstr+'.data', 'r')
		data = g.read()
		mes='Ваш GCN ID: '+idstr
		if data[8:] == 'EN':
			 mes='Your GCN ID: '+idstr
		bot.send_message(id, mes)
	if msg=='/lang':
		keyboard = types.InlineKeyboardMarkup()
		key_eng = types.InlineKeyboardButton(text='EN', callback_data='eng')
		keyboard.add(key_eng)
		key_rus = types.InlineKeyboardButton(text='RU', callback_data='rus')
		keyboard.add(key_rus)
		bot.send_message(message.from_user.id, text="Choose your language:", reply_markup=keyboard)
	if msg.find('/pay')!=-1:
		pay=msg[5:]
		g=open(idstr+'.data', 'r')
		data = g.read()
		g.close()
		i=0
		while pay[i]!=' ':
			i=i+1
		minus=len(pay)-i;
		if int(data[:8])<int(pay[:-minus]):
			mes='У вас не хватает монет для транзакции.'
			if data[8:] == 'EN':
				 mes='You don\'t have enouth coins for transaction'
			bot.send_message(id, mes)
		else:
			gcn=open('gcn.data', 'a')
			gcn.close()
			gcn=open('gcn.data', 'r')
			ids=gcn.read()
			ii=i+1
			if ids.find(pay[ii:]+' ')==-1:
				mes='Не найдено данного GCN ID в базе.'
				if data[8:] == 'EN':
					mes='Not founded this GCN ID in base.'
				bot.send_message(id, mes)
			else:
				payid=pay[ii:]
				sender=int(data[:8])
				sender=sender-int(pay[:-minus])
				sendstr=str(sender)
				sendstr=sendstr.rjust(8, '0')
				sendstr=sendstr+data[8:]
				g=open(idstr+'.data', 'w')
				g.write(sendstr)
				g.close()
				g=open(payid+'.data', 'r')
				recdata=g.read()
				g.close()
				recbal=int(recdata[:8])
				recbal=recbal+int(pay[:-minus])
				recstr=str(recbal)
				recstr = recstr.rjust(8, '0')
				recstr = recstr+recdata[8:]
				g=open(payid+'.data', 'w')
				g.write(recstr)
				g.close()
				mes="Успешно переведено "+pay[:-minus]+" GCN пользователю с GCN ID "+payid+". Спасибо за использование GCN!"
				if data[8:] == 'EN':
					mes='Successfully payed '+pay[:-minus]+' GCN to user with GCN ID '+payid+'. Thank you about using GCN!'
				bot.send_message(id, mes)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	idcall = call.message.chat.id
	idcallstr = str(idcall)
	if call.data == 'en':
		bot.send_message(idcall, 'Selected English language. Your GCN ID: '+idcallstr)
		f = open(idcallstr+'.data', 'a')
		f.write('EN')
		f.close
		gcn=open('gcn.data', 'a')
		gcn.write(idcallstr+' ')
		gcn.close()
	if call.data == 'ru':
		bot.send_message(idcall, "Выбран русский язык. Ваш GCN ID: "+idcallstr)
		f = open(idcallstr+'.data', 'a')
		f.write(' RU')
		f.close
		gcn=open('gcn.data', 'a')
		gcn.write(idcallstr+' ')
		gcn.close()
	if call.data == 'eng':
		bot.send_message(idcall, 'Selected English language.')
		g = open(idcallstr+'.data', 'r')
		oldata=g.read()
		oldata=oldata[:8]+'EN'
		g.close()
		g=open(idcallstr+'.data', 'w')
		g.write(oldata)
		g.close()
	if call.data == 'rus':
		bot.send_message(idcall, 'Выбран русский язык.')
		g = open(idcallstr+'.data', 'r')
		oldata=g.read()
		oldata=oldata[:8]+'RU'
		g.close()
		g=open(idcallstr+'.data', 'w')
		g.write(oldata)
		g.close()
bot.polling(none_stop=True, interval=0)