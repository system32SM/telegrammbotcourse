import requests
import json
from config import keys

class APIexception(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIexception(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIexception(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIexception(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIexception(f'Не удалось обработать количество {amount}')

        quote_ticker, base_ticker = keys[quote], keys[base]


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIexception(f"Валюта {base} не найдена!")

        try:
            sym_key = keys[sym.lower()]
        except KeyError:
            raise APIexception(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIexception(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIexception(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"http://data.fixer.io/api/latest?access_key=d1482cf2410f47de0f1bf0ee3bb7ec74&base={base_key}&symbols={sym_key}&format=1")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message