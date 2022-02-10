import requests
import json
from config import currencies, TOKEN_CRYPTO

class APIException(Exception):
	pass

class CurrencyConverter:
	@staticmethod
	def get_price(quote: str, base: str, amount: str):
		if quote == base:
			raise APIException(f'Не удалось перевести валюту {quote} в себя же')

		try:
			quote_ticker = currencies[quote]
		except KeyError:
			raise APIException(f'Не удалось обработать валюту {quote}')

		try:
			base_ticker = currencies[base]
		except KeyError:
			raise APIException(f'Не удалось обработать валюту {base}')

		try:
			amount = float(amount)
		except ValueError:
			raise APIException(f'Не удалось обработать количество {amount}')

		r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}&api_key={TOKEN_CRYPTO}')
		price = json.loads(r.content)[currencies[base]]
		cost = price * amount
		
		return cost
