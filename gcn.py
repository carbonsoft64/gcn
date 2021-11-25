import telebot
from telebot import types
bot = telebot.TeleBot('[token]')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	msg = message.text
	id = message.from_user.id
	idstr=str(id)
	langu='RU'
	g=open(idstr+'.data', 'a')
	g.close()
	g=open(idstr+'.data', 'r')
	adata = g.read()
	li = 0
	if len(adata)!=0:
		while adata[li]!='L' and li<len(adata):
			li+=1
	g.close()
	if msg=="/start":
		g = open(idstr+'.data', 'w')
		g.write('1')
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
		bal = data[:li]
		g.close()
		mes='Ваш текущий баланс: '+bal
		if data.find('EN')!=-1:
			 mes='Your current balance: '+bal
		mes += ' GCN'
		bot.send_message(id, mes)
	if msg=='/id':
		g=open(idstr+'.data', 'r')
		data = g.read()
		mes='Ваш GCN ID: '+idstr
		if data.find('EN')!=-1:
			 mes='Your GCN ID: '+idstr
		bot.send_message(id, mes)
	if msg=='/lang':
		keyboard = types.InlineKeyboardMarkup()
		key_eng = types.InlineKeyboardButton(text='EN', callback_data='eng')
		keyboard.add(key_eng)
		key_rus = types.InlineKeyboardButton(text='RU', callback_data='rus')
		keyboard.add(key_rus)
		bot.send_message(message.from_user.id, text="Choose your language:", reply_markup=keyboard)
	if msg=='/list':
		listfile=open('gcn.data', 'r')
		listmes=listfile.read()
		listfile.close()
		bot.send_message(id, 'list: '+listmes)
	if msg.find('/pay')!=-1 and len(msg)<11:
		bot.send_message(id, 'FAILED: ERROR GR1')
		msg = ''
	if msg.find('/pay')!=-1:
		pay=msg[5:]
		g=open(idstr+'.data', 'r')
		data = g.read()
		g.close()
		i=0
		while pay[i]!=' ':
			i=i+1
		minus=len(pay)-i;
		if int(data[:li])<int(pay[:-minus]):
			mes='У вас не хватает монет для транзакции.'
			if data.find('EN')!=-1:
				 mes='You have no coins for this transaction'
			bot.send_message(id, mes)
		else:
			gcn=open('gcn.data', 'a')
			gcn.close()
			gcn=open('gcn.data', 'r')
			ids=gcn.read()
			ii=i+1
			if ids.find(pay[ii:]+' ')==-1:
				mes='Не найдено данного GCN ID в базе.'
				if data.find('EN')!=-1:
					mes='Not founded this GCN ID in base.'
				bot.send_message(id, mes)
			else:
				payid=pay[ii:]
				sender=int(data[:li])
				sender=sender-int(pay[:-minus])
				sendstr=str(sender)
				#sendstr=sendstr.rjust(8, '0')
				sendstr=sendstr+data[li:]
				g=open(idstr+'.data', 'w')
				g.write(sendstr)
				g.close()
				g=open(payid+'.data', 'r')
				recdata=g.read()
				g.close()
				recbal=int(recdata[:-3])
				recbal=recbal+int(pay[:-minus])
				recstr=str(recbal)
				#recstr = recstr.rjust(8, '0')
				recstr = recstr+recdata[-3:]
				g=open(payid+'.data', 'w')
				g.write(recstr)
				g.close()
				mes="Успешно переведено "+pay[:-minus]+" GCN пользователю с GCN ID "+payid+". Спасибо за использование GCN!"
				if data.find('EN')!=-1:
					mes='Successfully payed '+pay[:-minus]+' GCN to user with GCN ID '+payid+'. Thank you about using GCN!'
				bot.send_message(id, mes)
				
				mes="Получено "+pay[:-minus]+" GCN от пользователя с GCN ID "+idstr+". Спасибо за использование GCN!"
				if recstr.find('EN')!=-1:
					mes='Received '+pay[:-minus]+' GCN from user with GCN ID '+idstr+'. Thank you about using GCN!'
				bot.send_message(payid, mes)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	idcall = call.message.chat.id
	idcallstr = str(idcall)
	if call.data == 'en':
		bot.send_message(idcall, 'Selected English language. Your GCN ID: '+idcallstr)
		f = open(idcallstr+'.data', 'a')
		f.write('LEN')
		f.close
		gcn=open('gcn.data', 'a')
		gcn.write(idcallstr+' ')
		gcn.close()
	if call.data == 'ru':
		bot.send_message(idcall, "Выбран русский язык. Ваш GCN ID: "+idcallstr)
		f = open(idcallstr+'.data', 'a')
		f.write('LRU')
		f.close
		gcn=open('gcn.data', 'a')
		gcn.write(idcallstr+' ')
		gcn.close()
	if call.data == 'eng':
		bot.send_message(idcall, 'Selected English language.')
		g = open(idcallstr+'.data', 'r')
		oldata=g.read()
		oldata=oldata[:li]+'LEN'
		g.close()
		g=open(idcallstr+'.data', 'w')
		g.write(oldata)
		g.close()
	if call.data == 'rus':
		bot.send_message(idcall, 'Выбран русский язык.')
		g = open(idcallstr+'.data', 'r')
		oldata=g.read()
		oldata=oldata[:li]+'LRU'
		g.close()
		g=open(idcallstr+'.data', 'w')
		g.write(oldata)
		g.close()
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)
bot.polling(none_stop=True, interval=0)
