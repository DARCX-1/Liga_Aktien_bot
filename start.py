# https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://codeburst.io/indian-stock-market-price-notifier-bot-telegram-92e376b0c33a

from stockinformation import Stockinformation
from bot import Bot
from watchlist import Watchlist
import time
import sys

TOKEN = '../Token/Token_Liga_bot.txt'
BOT_NAME = 'stocks_bot'
WATCHLIST_FILE = 'watchlist.json'

# db = DBHelper()
# bot = Bot(TOKEN, BOT_NAME)
stock = Stockinformation()
w = Watchlist(WATCHLIST_FILE)


def main():
    # watchlist = w.watchlist_load(WATCHLIST_FILE)
    # test = w.add('LIN.DE', 3)
    # print(test)
    # test1 = w.add('D7G.F', 6)
    # print(test1)
    # test1 = w.add('LIN.DE', 6)
    # test1 = w.add('LIN.DE', 6)
    # w.save(w.add('LIN.DE', 3))
    # w.save(w.add('D7G.F', 3))
    # w.save(w.add('D7G.F', 6))
    # w.save(w.add('LIN.DE', 6))
    w.add('LIN.DE', 3)
    w.add('D7G.F', 3)
    w.add('test', 3)
    w.add('D7G.F', 6)
    w.add('LIN.DE', 6)
    print(w.load(3))

    # test5 = w.load(6)
    # test6 = w.add('test', 6)
    # w.add('item', 3)
    # w.save(test6)
    # print(w.load(6))
    # test7 = w.ret(6)
    # print(test7)
    # eee = w.load(3)
    # test8 = w.add('test', 3)
    # print(test8)
    # db.setup()
    # bot.init_watchlist(watchlist)
    # last_update_id = None
    # while True:
    #     print("getting updates")
    #     updates = bot.get_updates(last_update_id)
    #     # insert watchlist here
    #     if len(updates["result"]) > 0:
    #         last_update_id = bot.get_last_update_id(updates) + 1
    #         bot.decide(updates)
    #     time.sleep(0.5)


if __name__ == '__main__':
    main()
