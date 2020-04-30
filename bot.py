import requests
import time
import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import json
import urllib
from watchlist import Watchlist
from stockinformation import Stockinformation


class Bot():

    def __init__(self, directory, bot_name, watchlist_file):
        super(Bot, self).__init__()
        with open('{}'.format(directory)) as f:
            token = f.readlines()[0]
        self.URL = 'https://api.telegram.org/bot{}/'.format(token)
        self.bot_name = bot_name
        self.w = Watchlist(watchlist_file)
        self.list = self.w.load()
        self.stock = Stockinformation()

    def get_url(self, url):
        try:
            response = requests.get(url)
            content = response.content.decode("utf8")
            return content
        except:
            print('Irgendetwas ist gerade Down')

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        print('jason', js)
        return js

    def get_updates(self, offset=None):
        url = self.URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def send_message(self, text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        chat_id = int(chat_id)
        url = self.URL + \
            "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(
                text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        self.get_url(url)

    def build_keyboard(self, items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def decide(self, updates):
        try:
            for update in updates["result"]:
                chat = str(update["message"]["chat"]["id"])
                text = update["message"]["text"]
                print('decide1', text)
                text = text.split(' ')
                # items = self.list[chat]
                # print(self.list)

                if text[0] == '/rmwl' or text[0] == '/rmwl@{}'.format(self.bot_name):
                    if len(text) == 1:
                        keyboard = self.build_keyboard(self.w.ret(chat))
                        print(keyboard)
                        self.send_message(
                            "Select an item to delete", chat, keyboard)
                    else:
                        for text in text[1:]:
                            print(text)
                            text = text.replace(',', '')
                            self.w.delete(text, chat)
                            message = text + ' was successful deleted'
                            self.send_message(message, chat)
                elif text[0] == '/addwl'or text[0] == '/addwl@{}'.format(self.bot_name):
                    for text in text[1:]:
                        text = text.replace(',', '')
                        self.w.add(text, chat)
                        message = text + ' was successful added'
                        self.send_message(message, chat)
                elif text[0] == '/getwl' or text[0] == '/getwl@{}'.format(self.bot_name):
                    items = self.w.ret(chat)
                    message = json.dumps(items, indent=4)
                    self.send_message(message, chat)
                elif text[0] == '/sp' or text[0] == '/sp@{}'.format(self.bot_name):
                    if len(text) == 1:
                        message = 'Please add the Stocks'
                        self.send_message(message, chat)
                    else:
                        for symbol in text[1:]:
                            symbol = symbol.replace(',', '').upper()
                            price = self.stock.get_stock_price(symbol)
                            message = 'The Price for', symbol, 'is', price
                            self.send_message(price, chat)
                else:
                    continue
        except Exception as e:
            print(e)
