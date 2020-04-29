import json
from stockinformation import Stockinformation

stock = Stockinformation()

KEY_SYMBOL = 'symbol'
KEY_CHAT = 'chat'
KEY_ID = 'id'
KEY_PRICE = 'last price'
KEY_NEW_PRICE = 'actual price'

# fragen, wie bekomme ich es hin, dass ich jetzt noch das stehen habe dass vorne die chat id steht und hinten die symbole?
# wie speichere ich die Keys bei json.dump als int
# wie bekomme ich jetzt den bot mit der def get stock price von functions  hier rein? über import, oder geht das besser, weil wir den im Mainskript aufrufen?
# also könnte man die bot klasse in der init noch mit übergeben?


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
                pass
            else:
                self.data[chat].append(self.temp_dict(item))
        else:
            values = []
            values.append(self.temp_dict(item))
            self.data[chat] = values
        return self.data

    def delete(self, item, chat):
        for v in self.data[chat]:
            if v[KEY_SYMBOL] == item:
                self.data[chat].remove(v)
            else:
                pass
        return self.data

    def load(self, chat):
        with open(self.file) as json_file:
            data = json.load(json_file, object_hook=lambda d: {int(
                k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
            data = self.data[chat]
        return data

    def save(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=True)

    def ret(self, chat):
        values = []
        for v in self.load(chat):
            ret_dict = {}
            ret_dict[KEY_SYMBOL] = v[KEY_SYMBOL]
            ret_dict[KEY_NEW_PRICE] = stock.get_stock_price(v[KEY_SYMBOL])
            ret_dict[KEY_PRICE] = v[KEY_NEW_PRICE]
            values.append(ret_dict)
        self.data[chat] = values
        self.save(self.data)
        return self.data
