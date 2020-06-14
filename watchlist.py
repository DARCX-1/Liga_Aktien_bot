import json
from stockinformation import Stockinformation

stock = Stockinformation()

KEY_SYMBOL = 'symbol'
KEY_PRICE = 'last price'
KEY_NEW_PRICE = 'actual price'
KEY_TARGET_BUY = 'target buy price'
KEY_TARGET_SELL = 'target sell price'
KEY_REPORT_BUY = 'Report Buy'
KEY_REPORT_SELL = 'Report Sell'

KEYS = {KEY_SYMBOL: 'None', KEY_PRICE: 0.0, KEY_NEW_PRICE: 0.0, KEY_TARGET_BUY: 0.0,
        KEY_REPORT_BUY: False, KEY_TARGET_SELL: 0.0, KEY_REPORT_SELL: False}


class Watchlist:

    def __init__(self, file):
        self.file = file

    def length(self):
        return len(data)

    def temp_dict(self, item, target_buy, target_sell):
        temp_dict = {}
        temp_dict[KEY_SYMBOL] = item
        temp_dict[KEY_NEW_PRICE] = stock.get_stock_price(item)
        temp_dict[KEY_PRICE] = 'None'
        temp_dict[KEY_TARGET_BUY] = target_buy
        temp_dict[KEY_REPORT_BUY] = False
        temp_dict[KEY_TARGET_SELL] = target_sell
        temp_dict[KEY_REPORT_SELL] = False
        return temp_dict

    def add(self, item, target_buy, target_sell, chat):
        data = self.load()
        if chat in data:
            if item in [v[KEY_SYMBOL] for v in data[chat]]:
                for v in data[chat]:
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
                print('break2')
                data[chat].append(self.temp_dict(
                    item, target_buy, target_sell))
                self.save(data)
                return [' was successful added']
        else:
            print('break1')
            values = []
            values.append(self.temp_dict(item, target_buy, target_sell))
            data[chat] = values
        self.save(data)
        return data

    def delete(self, item, chat):
        data = self.load()
        for v in data[chat]:
            if v[KEY_SYMBOL] == item:
                data[chat].remove(v)
            else:
                pass
        self.save(data)
        return data[chat]

    def update(self, item, target_buy, target_sell, chat):
        self.delete(item, chat)
        data = self.load()
        data[chat].append(self.temp_dict(item, target_buy, target_sell))
        self.save(data)
        return data[chat]

    def load(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        return data

    def save(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=True)

    def ret(self, chat):
        values = []
        data = self.load()
        for v in data[chat]:
            ret_dict = {}
            ret_dict[KEY_SYMBOL] = v[KEY_SYMBOL]
            # ret_dict[KEY_SYMBOL] = data[chat][v][KEY_SYMBOL]
            ret_dict[KEY_NEW_PRICE] = stock.get_stock_price(v[KEY_SYMBOL])
            ret_dict[KEY_PRICE] = v[KEY_NEW_PRICE]
            ret_dict[KEY_TARGET_BUY] = v[KEY_TARGET_BUY]
            ret_dict[KEY_REPORT_BUY] = v[KEY_REPORT_BUY]
            ret_dict[KEY_TARGET_SELL] = v[KEY_TARGET_SELL]
            ret_dict[KEY_REPORT_SELL] = v[KEY_REPORT_SELL]
            values.append(ret_dict)
        data[chat] = values
        self.save(data)
        return data[chat]

    def upgrade(self):
        c = 0
        data = self.load()
        for chat in data:
            for i in data[chat]:
                for key in KEYS:
                    if key not in data[chat][i]:
                        data[chat][i][key] = KEYS[key]
                        c += 1
        self.save(data)
        return c

    def compare(self, chat):
        message = []
        data = self.load()
        for v in data[chat]:
            if stock.get_stock_price(v[KEY_SYMBOL]) <= v[KEY_TARGET_BUY] and v[KEY_REPORT_BUY] == False:
                message.append('The actual price for {} is less then your target buy price'.format(v[
                    KEY_SYMBOL]))
                v[KEY_REPORT_BUY] = True
            elif stock.get_stock_price(v[KEY_SYMBOL]) > v[KEY_TARGET_BUY] and v[KEY_REPORT_BUY] == True:
                v[KEY_REPORT_BUY] = False
            else:
                continue
            if stock.get_stock_price(v[KEY_SYMBOL]) >= v[KEY_TARGET_SELL] and v[KEY_REPORT_SELL] == False:
                message.append('The actual price for {} is higher then your target sell price'.format(v[
                    KEY_SYMBOL]))
            elif stock.get_stock_price(v[KEY_SYMBOL]) < v[KEY_TARGET_SELL] and v[KEY_REPORT_SELL] == True:
                v[KEY_REPORT_SELL] = False
            else:
                continue
        self.save(data)
        return message
