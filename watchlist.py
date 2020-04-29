import json
from calculations import Calculation

calc = Calculation()

KEY_SYMBOL = 'symbol'
KEY_CHAT = 'chat'
KEY_ID = 'id'
KEY_PRICE = 'price'

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

    def add(self, item, chat):
        if chat in self.data.keys():
            print([v[KEY_SYMBOL] for v in self.data[chat]])
            print(item)
            if item in [v[KEY_SYMBOL] for v in self.data[chat]]:
                pass
            else:
                temp_dict = {}
                temp_dict[KEY_SYMBOL] = item
                temp_dict[KEY_PRICE] = calc.get_stock(item)
                self.data[chat].append(temp_dict)
        else:
            values = []
            temp_dict = {}
            temp_dict[KEY_SYMBOL] = item
            temp_dict[KEY_PRICE] = calc.get_stock(item)
            values.append(temp_dict)
            self.data[chat] = values
        return self.data

    def delete(self, item, chat):
        try:
            for v in self.data[chat]:
                if v[KEY_SYMBOL] == item:
                    self.data[chat].remove(v)
        except Exception as e:
            print(e)
        return self.data

    def load(self):
        with open(self.file) as json_file:
            data = json.load(json_file, object_hook=lambda d: {int(
                k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
        return data

    def save(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=True)
