# for DBHelper
import sqlite3

# for Bot
import requests
import time
import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import json
import urllib

class DBHelper:

    def __init__(self, dbname="Watchlist.sqlite"):
        dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner= (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]

####################################################################
# BOT Class
####################################################################


class bot(DBHelper):
    # DBHelper=DBHelper()
    def __init__(self, directory, bot_name):
        super(bot, self).__init__()
        with open('{}'.format(directory)) as f:
            token = f.readlines()[0]
        self.URL = 'https://api.telegram.org/bot{}/'.format(token)
        self.bot_name = bot_name
        # DBHelper()


    def get_url(self, url):
        try:
            response = requests.get(url)
            content = response.content.decode("utf8")
            print('get_url',content)
            return content
        except:
            print('Irgendetwas ist gerade Down')

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
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

    def get_stock(self, symbol):
        # yf.pdr_override()
        try:
            stock = pdr.get_data_yahoo(symbol,  start="2020-04-20",
                                       end=datetime.date.today())
            price = (stock["Close"][0]).round(3)
            price = str(price)
            price = "Current price for " + symbol + " is " + price
            price = str(price.encode('utf-8', 'ignore'), errors='ignore')
            return price
        except KeyError:
            return 'wrong symbol or no actual price'
        except Exception as e:
            return e

    def decide(self, updates):
        try:
            for update in updates["result"]:
                Chat_type = update["message"]["chat"]["type"]
                chat = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                text = text.split(' ')
                print(text)
                items = DBHelper.get_items(self,chat)
                print(items)
                if text[0] == '/delete_watchlist' or text[0] == '/delete_watchlist@{}'.format(self.bot_name):
                    if len(text[1:]) == 0:
                        keyboard = self.build_keyboard(items)
                        print(keyboard)
                        self.send_message(
                            "Select an item to delete", chat, keyboard)
                    else:
                        for text in text[1:]:
                            text = text.replace(',', '')
                            DBHelper.delete_item(self,text, chat)
                            items = DBHelper.get_items(self,chat)
                            message = "\n".join(items)
                            self.send_message(message, chat)
                elif text[0] == '/add_watchlist'or text[0] == '/add_watchlist@{}'.format(self.bot_name):
                    for text in text[1:]:
                        text = text.replace(',', '')
                        if text in items:
                            message = text + ' is already in List'
                        else:
                            DBHelper.add_item(self,text, chat)
                            items = DBHelper.get_items(self,chat)
                            message = "\n".join(items)
                        self.send_message(message, chat)
                elif text[0] == '/get_watchlist' or text[0] == '/get_watchlist@{}'.format(self.bot_name):
                    items = DBHelper.get_items(self,chat)
                    message = "\n".join(items)
                    self.send_message(message, chat)
                elif text[0] == '/get_stock_price' or text[0] == '/get_stock_price@{}'.format(self.bot_name):
                    if len(text) == 1 or text[1].lower() == 'watchlist':
                        items = DBHelper.get_items(self,chat)
                        for i in items:
                            price = self.get_stock(i.upper())
                            self.send_message(price, chat)
                    else:
                        for symbol in text[1:]:
                            symbol = symbol.replace(',', '').upper()    
                            price = self.get_stock(symbol)
                            self.send_message(price, chat)
                else:
                    continue
        except Exception as e:
            print(e)
