import telebot
from config import currencies, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def help(message: telebot.types.Message):
	text = 'Введите команду в формате:\n\
<имя валюты> <в какую перевести> <количество переводимой валюты>\n\
Список доступных валют по команде /values'
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
	text = 'Доступные валюты:'
	for key in currencies.keys():
		text = '\n'.join((text, key))
	bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
	try:
		values = message.text.split(' ')

		if len(values) > 3:
			raise APIException('Слишком много параметров')

		if len(values) < 3:
			raise APIException('Слишком мало параметров')

		quote, base, amount = values

		cost = CurrencyConverter.get_price(quote, base, amount)
	except APIException as e:
		bot.reply_to(message, f'Ошибка пользователя\n{e}')
	except Exception as e:
		bot.reply_to(message, f'Не удалось обработать команду\n{e}')
	else:
		text = f'Цена {amount} {quote} в {base} = {cost}'
		bot.send_message(message.chat.id, text)

bot.polling()
