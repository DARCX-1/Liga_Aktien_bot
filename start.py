# https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://codeburst.io/indian-stock-market-price-notifier-bot-telegram-92e376b0c33a


from functions import DBHelper
from functions import bot
from watchlist import Watchlist
import time
import sys

TOKEN = ''
BOT_NAME = 'stocks_bot'
WATCHLIST_FILE = 'watchlist.json'

# db = DBHelper()
# bot = bot(TOKEN, BOT_NAME)
w = Watchlist(WATCHLIST_FILE)


def main():
    # watchlist = w.watchlist_load(WATCHLIST_FILE)
    test = w.add(5, 3)
    print(test)
    test1 = w.add(5, 6)
    print(test1)
    test2 = w.add(6, 3)
    print(test2)
    test3 = w.delete(5, 3)
    print(test3)
    test4 = w.delete(4, 4)
    print(test4)
    w.save(test2)

    test5 = w.load()
    print(test5)
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
