#https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
#https://codeburst.io/indian-stock-market-price-notifier-bot-telegram-92e376b0c33a

import requests
import time
import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import json 
import urllib

TOKEN ='1087183328:AAG_qSnMIT-ZWU4cigYiqUmYz5ywZdjB33I'
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

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

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

def echo_all(updates):
    for update in updates["result"]:
        try:
            Chat_type = update["message"]["chat"]["type"]
            Symbol = update["message"]["text"]
            if Chat_type == 'group':
                Symbol = Symbol.split(' ')[-1]
            else:
                Symbol = Symbol
            chat = update["message"]["chat"]["id"]
            price = getStock(Symbol)
            send_message(price, chat)   
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

