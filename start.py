# https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://codeburst.io/indian-stock-market-price-notifier-bot-telegram-92e376b0c33a

from bot import Bot
import time
import sys

TOKEN = '../Token/Token_Liga_bot.txt'
BOT_NAME = 'stocks_bot'
WATCHLIST_FILE = 'watchlist.json'


bot = Bot(TOKEN, BOT_NAME, WATCHLIST_FILE)


def main():
    # bot.init_watchlist(watchlist)
    last_update_id = None
    while True:
        bot.check_target()
        print("getting updates")
        updates = bot.get_updates(last_update_id)
        # insert watchlist here
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            bot.decide(updates)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
