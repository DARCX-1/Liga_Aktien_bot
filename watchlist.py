import json
from stockinformation import Stockinformation

stock = Stockinformation()

KEY_SYMBOL = 'symbol'
KEY_PRICE = 'last price'
KEY_NEW_PRICE = 'actual price'
KEY_TARGET_BUY = 'target buy price'
KEY_TARGET_SELL = 'target sell price'


class Watchlist:

    def __init__(self, file):
        self.file = file
        self.data = {}

    def length(self):
        return len(self.data)

    def temp_dict(self, item, target_buy, target_sell):
        temp_dict = {}
        temp_dict[KEY_SYMBOL] = item
        temp_dict[KEY_NEW_PRICE] = stock.get_stock_price(item)
        temp_dict[KEY_PRICE] = 'None'
        temp_dict[KEY_TARGET_BUY] = target_buy
        temp_dict[KEY_TARGET_SELL] = target_sell
        return temp_dict

    def add(self, item, target_buy, target_sell, chat):

        if chat in self.data.keys():
            if item in [v[KEY_SYMBOL] for v in self.data[chat]]:
                for v in self.data[chat]:
                    if item in v[KEY_SYMBOL] and target_buy == v[KEY_TARGET_BUY]and target_sell == v[KEY_TARGET_SELL]:
                        return [' already in list']
                    elif item in v[KEY_SYMBOL] and target_buy != v[KEY_TARGET_BUY] and target_sell == v[KEY_TARGET_SELL]:
                        self.update(item, target_buy, target_sell, chat)
                        return [' {} updated'.format(KEY_TARGET_BUY)]
                    elif item in v[KEY_SYMBOL] and target_buy == v[KEY_TARGET_BUY] and target_sell != v[KEY_TARGET_SELL]:
                        self.update(item, target_buy, target_sell, chat)
                        return [' {} updated'.format(KEY_TARGET_SELL)]
                    elif item in v[KEY_SYMBOL] and target_buy != v[KEY_TARGET_BUY] and target_sell != v[KEY_TARGET_SELL]:
                        self.update(item, target_buy, target_sell, chat)
                        return [' {} and {} updated'.format(KEY_TARGET_SELL, KEY_TARGET_BUY)]
                    else:
                        continue
            else:
                self.data[chat].append(self.temp_dict(
                    item, target_buy, target_sell))
                self.save()
                return [' was successful added']
        else:
            values = []
            values.append(self.temp_dict(item, target_buy, target_sell))
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

    def update(self, item, target_buy, target_sell, chat):
        self.delete(item, chat)
        self.data[chat].append(self.temp_dict(item, target_buy, target_sell))
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
            ret_dict[KEY_TARGET_BUY] = v[KEY_TARGET_BUY]
            ret_dict[KEY_TARGET_SELL] = v[KEY_TARGET_SELL]
            values.append(ret_dict)
        self.data[chat] = values
        self.save()
        return self.data[chat]

    def compare(self, chat):
        message = []
        self.load()
        for v in self.data[chat]:
            if stock.get_stock_price(v[KEY_SYMBOL]) <= v[KEY_TARGET_BUY]:
                message.append('The actual price for {} is less then your target buy price'.format(v[
                    KEY_SYMBOL]))
            else:
                continue
            if stock.get_stock_price(v[KEY_SYMBOL]) >= v[KEY_TARGET_SELL]:
                message.append('The actual price for {} is higher then your target sell price'.format(v[
                    KEY_SYMBOL]))
            else:
                continue
        return message
