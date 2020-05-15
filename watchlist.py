import json
from stockinformation import Stockinformation

stock = Stockinformation()

KEY_SYMBOL = 'symbol'
KEY_PRICE = 'last price'
KEY_NEW_PRICE = 'actual price'
KEY_TARGET = 'target price'


class Watchlist:

    def __init__(self, file):
        self.file = file
        self.data = {}

    def length(self):
        return len(self.data)

    def temp_dict(self, item):
        temp_dict = {}
        temp_dict[KEY_SYMBOL] = item
        temp_dict[KEY_NEW_PRICE] = stock.get_stock_price(item)
        temp_dict[KEY_PRICE] = 'None'
        return temp_dict

    def add(self, item, chat):
        if chat in self.data.keys():
            if item in [v[KEY_SYMBOL] for v in self.data[chat]]:
                return ['Already in List']
            else:
                self.data[chat].append(self.temp_dict(item))
        else:
            values = []
            values.append(self.temp_dict(item))
            self.data[chat] = values
        self.save()
        return self.data

    def delete(self, item, chat):
        for v in self.data[chat]:
            if v[KEY_SYMBOL] == item:
                self.data[chat].remove(v)
            else:
                pass
        self.save()
        return self.data[chat]

    def load(self):
        with open(self.file) as json_file:
            self.data = json.load(json_file)
        return self.data

    def save(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.data, outfile, ensure_ascii=True)

    def ret(self, chat):
        values = []
        self.load()
        for v in self.data[chat]:
            ret_dict = {}
            ret_dict[KEY_SYMBOL] = v[KEY_SYMBOL]
            ret_dict[KEY_NEW_PRICE] = stock.get_stock_price(v[KEY_SYMBOL])
            ret_dict[KEY_PRICE] = v[KEY_NEW_PRICE]
            values.append(ret_dict)
        self.data[chat] = values
        self.save()
        return self.data[chat]
