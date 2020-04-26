#https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
#https://codeburst.io/indian-stock-market-price-notifier-bot-telegram-92e376b0c33a

import requests
import time
import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import json 
import urllib
from Watchlist import DBHelper


db = DBHelper()

with open ('../Token/Token_Liga_bot.txt') as f:
    TOKEN = f.readlines()[0] 
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

def get_url(url):
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
    except:
        print('Irgendetwas ist gerade Down')


def get_json_from_url(url):
    content = get_url(url)
    print(content)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

# def handle_updates(updates):
#     for update in updates["result"]:
#         # try:
#         text = update["message"]["text"]
#         chat = update["message"]["chat"]["id"]
#         items = db.get_items(chat)
#         if text == "/delete":
#             keyboard = build_keyboard(items)
#             send_message("Select an item to delete", chat, keyboard)
#         elif text == "/start":
#             send_message("Welcome to the Watchlist. Send any text to me and I'll store it as an item. Send /delete to remove items", chat)
#         elif text.startswith("/"):
#             continue
#         elif text in items:
#             db.delete_item(text, chat)
#             items = db.get_items(chat)
#             keyboard = build_keyboard(items)
#             send_message("Select an item to delete", chat, keyboard)
#         else:
#             db.add_item(text, chat)
#             items = db.get_items(chat)
#             message = "\n".join(items)
#             send_message(message, chat)
#         # except KeyError:
#         #     pass

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
  
def getStock(Symbol):
    # yf.pdr_override()
    try:
        aapl=pdr.get_data_yahoo(Symbol,  start="2020-04-20", 
                             end=datetime.date.today())
        price=(aapl["Close"][0]).round(3)
        price=str(price)
        price="Current price for "+Symbol+ " is "+price
        price=str(price.encode('utf-8','ignore'),errors='ignore')
        return price
    except KeyError:
        return 'Falsches Symbol oder kein aktueller Wert'
    except Exception as e:  
        print(e)
        return e

# def echo_all(updates):
#     for update in updates["result"]:
#         try:
#             Chat_type = update["message"]["chat"]["type"]
#             Symbol = update["message"]["text"]
#             if Chat_type == 'group':
#                 Symbol = Symbol.split(' ')[-1]
#             else:
#                 Symbol = Symbol
#             chat = update["message"]["chat"]["id"]
#             price = getStock(Symbol)
#             send_message(price, chat)   
#         except Exception as e:
#             print(e)

def decide(updates):
    try:
        for update in updates["result"]:
            Chat_type = update["message"]["chat"]["type"]
            text = update["message"]["text"]
            text = text.split(' ')
            print(text)
            print(text[0])
            print(text[1:])
            chat = update["message"]["chat"]["id"]
            items = db.get_items(chat)
            if text[0] == '/delete_watchlist' or text[0] == '/delete_watchlist@Liga_Aktien_bot':
                if len(text[1:]) == 0:
                    keyboard = build_keyboard(items)
                    send_message("Select an item to delete", chat, keyboard)
                else:
                    for text in text[1:]:
                        text=text.replace(',','')
                        db.delete_item(text, chat)
                        items = db.get_items(chat)
                        message = "\n".join(items)
                        send_message(message, chat)
            elif text[0] == '/add_watchlist'or text[0] == '/add_watchlist@Liga_Aktien_bot':
                for text in text[1:]:
                    text = text.replace(',','')
                    if text in items:
                        message= text + ' is already in List'
                    else:
                        db.add_item(text, chat)
                        items = db.get_items(chat)
                        message = "\n".join(items)
                    send_message(message, chat)
            elif text[0] == '/get_watchlist' or text[0] == '/get_watchlist@Liga_Aktien_bot':
                items = db.get_items(chat)
                message = "\n".join(items)
                send_message(message, chat)
            elif text[0] == '/get_stock_price' or text[0] == '/get_stock_price@Liga_Aktien_bot':
                for Symbol in text[1:]:
                    Symbol = Symbol.replace(',','')
                    try:
                        price = getStock(Symbol)
                        send_message(price, chat) 
                    except Exception as e:
                        print(e) 
            else:
                continue
    except Exception as e:
         print(e) 

def main():
    db.setup()
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            decide(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

